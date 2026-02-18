import json
import os
import requests

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.utils import query_documents
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/chat", tags=["chat"], strict_slashes=False)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3")

class ChatStreamRequest(BaseModel):
    message: str
    n_results: int = 5

@router.post("/stream")
async def chat_stream(payload: ChatStreamRequest, user: dict = Depends(get_current_user)) -> StreamingResponse:
    """
    Accepts a user query, retrieves relevant chunks from Chroma,
    and generates a streaming response using the local Ollama model.
    Uses Server-Sent Events (SSE) for streaming.
    """
    
    # Retrieve the relevant documents from ChromaDB
    payload_data = payload.model_dump()
    message = payload_data["message"]
    n_results = payload_data["n_results"]
    
    # Retrieve relevant documents
    results = query_documents(message, n_results)
    
    context_blocks = []
    for doc, meta in zip(results["documents"], results["metadatas"]):
        context_blocks.append(f"Source: {meta.get('source')}\nContent: {doc}")
    
    context_text = "\n\n".join(context_blocks)
    
    # Prepare the prompt for Ollama
    prompt = f"""
You are an assistant that answers questions using ONLY the provided context.
If the answer is not in the context, say you don't know.

Context:
{context_text}

User question:
{payload.message}

Answer:
"""

    def stream_generator():
        # Call Ollama API with streaming enabled
        
        with requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": True
            },
            stream=True
        ) as r:
            r.raise_for_status()
            
            for line in r.iter_lines():
                if not line:
                    continue
                
                try:
                    data = json.loads(line.decode('utf-8'))
                    token = data.get("response", "")
                    
                    if token:
                        yield f"data: {token}\n\n"
                    
                    if data.get("done", False):
                        break
                    
                except Exception as e:
                    continue
                
        # Send retrieval metadata as final JSON event        
        metadata_event = {
            "context_used": {
                "documents": results["documents"],
                "metadatas": results["metadatas"],
                "distances": results.get("distances")
            }
        }
        
        yield f"data: {json.dumps(metadata_event)}\n\n"
        
        # End of stream
        
        yield "data: [DONE]\n\n"
        
    return StreamingResponse(stream_generator(), media_type="text/event-stream")
    