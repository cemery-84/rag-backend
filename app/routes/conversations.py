from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.db.conversations import create_conversation, list_conversations, delete_conversation
from app.db.messages import create_message, list_messages
from app.db.users import ensure_user_exists
from app.models import ConversationCreate, MessageCreate

router = APIRouter(prefix="/conversations", tags=["conversations"])

@router.post("/")
def create_conv(body: ConversationCreate, user: dict = Depends(get_current_user)):
    ensure_user_exists(user_id=user["user_id"], email=user.get("email"))
    return create_conversation(user_id=user["user_id"], title=body.title)

@router.get("/")
def get_convs(user: dict = Depends(get_current_user)):
    return list_conversations(user_id=user["user_id"])

@router.delete("/{conversation_id}")
def delete_conv(conversation_id: str, user: dict = Depends(get_current_user)):
    delete_conversation(conversation_id=conversation_id, user_id=user["user_id"])
    return {"status": "deleted"}

@router.get("/{conversation_id}/messages")
def get_conv_messages(conversation_id: str, user: dict = Depends(get_current_user)):
    return list_messages(conversation_id=conversation_id)

@router.post("/{conversation_id}/messages")
def create_conv_message(conversation_id: str, body: MessageCreate, user: dict = Depends(get_current_user)):
    return create_message(conversation_id=conversation_id, user_id=user["user_id"], role=body.role, content=body.content)