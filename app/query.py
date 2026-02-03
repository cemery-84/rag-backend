from fastapi import APIRouter
from pydantic import BaseModel

from app.utils import query_documents

router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    n_results: int = 5
    
@router.post("/query")
async def query_endpoint(payload: QueryRequest) -> dict:
    """
    Accepts a user query, retrieves relevant chunks from Chroma,
    and returns them to the caller.
    """
    results = query_documents(
        query=payload.query,
        n_results=payload.n_results
    )
    
    return results