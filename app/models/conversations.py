from pydantic import BaseModel

class ConversationCreate(BaseModel):
    title: str | None = None

class MessageCreate(BaseModel):
    role: str
    content: str
