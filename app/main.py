from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.ingest import router as ingest_router
from app.query import router as query_router
from app.chat import router as chat_router
from app.chat_stream import router as chat_stream_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest_router)
app.include_router(query_router)
app.include_router(chat_router)
app.include_router(chat_stream_router)