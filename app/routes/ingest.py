import uuid

from fastapi import APIRouter, UploadFile, File, Depends
from pypdf import PdfReader

from app.utils import add_documents
from app.auth.dependencies import get_current_user

router = APIRouter()


def extract_text_from_pdf(file: UploadFile) -> str:
    """
    Extracts text from an uploaded PDF file.
    """
    reader = PdfReader(file.file)
    text = ""
    
    for page in reader.pages:
        text += page.extract_text() or ""
        
    return text


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Splits the input text into chunks of specified size with overlap.
    """
    words = text.split()
    chunks = []
    
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
        
    return chunks


def process_document(text: str, source_name: str, owner_id: str, owner_email: str) -> int:
    """
    Processes the document text by chunking and adding to the vector store.
    """
    chunks = chunk_text(text)
    
    ids = []
    metadatas = []
    
    for i, chunk in enumerate(chunks):
        ids.append(f"{source_name}-{i}-{uuid.uuid4()}")
        metadatas.append({
            "source": source_name,
            "chunk_index": i,
            "owner_id": owner_id,
            "owner_email": owner_email
        })
        
    add_documents(ids=ids, texts=chunks, metadatas=metadatas)
    
    return len(chunks)


@router.post("/ingest")
async def ingest_file(file: UploadFile = File(...), user: dict = Depends(get_current_user)) -> dict:
    """
    Endpoint to ingest a PDF file, extract text, chunk it, and add to vector store.
    Returns the number of chunks added.
    """
    if file.content_type != "application/pdf":
        return {"error": "Only PDF files are supported."}
    
    firebase_uid = user["user_id"]
    email = user.get("email")
    
    text = extract_text_from_pdf(file)
    num_chunks = process_document(text, source_name=file.filename, owner_id=firebase_uid, owner_email=email)
    
    return {"chunks_added": num_chunks}