from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer

from app.routes.ingest import router as ingest_router
from app.routes.query import router as query_router
from app.routes.chat import router as chat_router
from app.routes.chat_stream import router as chat_stream_router
from app.routes.conversations import router as conversations_router

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)

security = HTTPBearer()

load_dotenv()

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
app.include_router(conversations_router)