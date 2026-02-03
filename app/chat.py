import os
import requests

from fastapi import APIRouter
from pydantic import BaseModel

from app.utils import query_documents

router = APIRouter()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3")

class ChatRequest(BaseModel):
    message: str
    n_results: int = 5

@router.post("/chat")
async def chat_endpoint(payload: ChatRequest) -> dict:
    """
    Accepts a user query, retrieves relevant chunks from Chroma,
    and generates a response using the local Ollama model.
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
    
    # Call the Ollama API to generate a response
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )
    
    response.raise_for_status()
    data = response.json()
    
    answer = data.get("response", "")
    
    return {
        "answer": answer,
        "context_used": results
    }