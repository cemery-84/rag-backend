import os

from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer
from typing import List ,Dict, Any

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CHROMA_DIR = os.path.join(BASE_DIR, "data", "chroma")
COLLECTION_NAME = "documents"

# Setup the chromadb client and collection
client = PersistentClient(path=CHROMA_DIR)
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"} # cosine similarity is standard for text embeddings
)

# Initialize the SentenceTransformer model for embeddings
embedder = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(texts: List[str]) -> List[List[float]]:
    """
    Given a list of strings, returns a list of embedding vectors from the local SentenceTransformer model.
    """
    raw_embeddings = embedder.encode(texts, convert_to_numpy=False)
    
    cleaned = []
    for emb in raw_embeddings:
        # If it's a tensor, convert to list
        if hasattr(emb, 'tolist'):
            cleaned.append(emb.tolist())
        else:
            cleaned.append(emb)
            
    return cleaned


def add_documents(
    ids: List[str],
    texts: List[str],
    metadatas: List[Dict[str, Any]] | None = None
) -> None:
    """
    Adds documents to the ChromaDB collection with their embeddings.
    Each document should be a dict with 'id', 'text', and optional 'metadata'.
    """
    if metadatas is None:
        metadatas = [{} for _ in texts]
    
    embeddings = embed_text(texts)
    
    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )
    
    
def query_documents(
    query: str,
    n_results: int = 5
) -> Dict[str, Any]:
    """
    Given a user query, embed it and search the Chroma collection.
    Returns the raw Chroma query result.
    """
    query_embedding = embed_text([query])[0]
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    return {
        "ids": results["ids"][0],
        "documents": results["documents"][0],
        "metadatas": results["metadatas"][0],
        "distances": results["distances"][0]
    }
        