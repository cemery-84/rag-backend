from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.db.conversations import create_conversation_db, list_conversations_db, delete_conversation_db
from app.db.messages import create_message_db, list_messages_db
from app.db.users import ensure_user_exists
from app.models.conversations import ConversationCreate, MessageCreate

router = APIRouter(prefix="/conversations", tags=["conversations"], strict_slashes=False)

@router.get("/")
def get_conversations_route(user: dict = Depends(get_current_user)):
    return list_conversations_db(user_id=user["user_id"])

@router.post("/")
def create_conversation_route(body: ConversationCreate, user: dict = Depends(get_current_user)):
    ensure_user_exists(user_id=user["user_id"], email=user.get("email"))
    return create_conversation_db(user_id=user["user_id"], title=body.title)

@router.delete("/{conversation_id}")
def delete_conversation_route(conversation_id: str, user: dict = Depends(get_current_user)):
    delete_conversation_db(conversation_id=conversation_id, user_id=user["user_id"])
    return {"status": "deleted"}

@router.get("/{conversation_id}/messages")
def get_conversation_messages_route(conversation_id: str, user: dict = Depends(get_current_user)):
    return list_messages_db(conversation_id=conversation_id)

@router.post("/{conversation_id}/messages")
def create_conversation_message_route(conversation_id: str, body: MessageCreate, user: dict = Depends(get_current_user)):
    return create_message_db(conversation_id=conversation_id, user_id=user["user_id"], role=body.role, content=body.content)