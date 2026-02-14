from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.utils import query_documents
from app.auth.dependencies import get_current_user

router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    n_results: int = 5
    
@router.post("/query")
async def query_endpoint(payload: QueryRequest, user: dict = Depends(get_current_user)) -> dict:
    """
    Accepts a user query, retrieves relevant chunks from Chroma,
    and returns them to the caller.
    """
    results = query_documents(
        query=payload.query,
        n_results=payload.n_results
    )
    
    return results