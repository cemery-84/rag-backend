from .firestore import db
from uuid import uuid4
from datetime import datetime, timezone

# Conversations are stored in Firestore under the path: users/{user_id}/conversations/{conversation_id}

# Create a new conversation for a user
def create_conversation_db(user_id: str, title: str | None = None):
    conversation_id = str(uuid4())
    conversation = {
        "title": title or "New Conversation",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    
    db.collection("users") \
        .document(user_id) \
        .collection("conversations") \
        .document(conversation_id) \
        .set(conversation)   
    
    return {"id": conversation_id, **conversation}

# List all conversations for a user, ordered by updated_at descending
def list_conversations_db(user_id: str):
    docs = db.collection("users") \
        .document(user_id) \
        .collection("conversations") \
        .order_by("updated_at", direction="DESCENDING") \
        .stream()
    
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]

# Delete a conversation
def delete_conversation_db(conversation_id: str, user_id: str):
    db.collection("users") \
        .document(user_id) \
        .collection("conversations") \
        .document(conversation_id) \
        .delete()