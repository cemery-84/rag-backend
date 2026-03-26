from .firestore import db
from uuid import uuid4
from datetime import datetime, timezone

# Messages are stored in Firestore under the path: users/{user_id}/conversations/{conversation_id}/messages/{message_id}

# Create a new message in a conversation
def create_message_db(conversation_id: str, user_id: str, role: str, content: str):
    message_id = str(uuid4())
    message = {
        "role": role,
        "content": content,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    db.collection("users") \
        .document(user_id) \
        .collection("conversations") \
        .document(conversation_id) \
        .collection("messages") \
        .document(message_id) \
        .set(message)
    
    return {"id": message_id, **message}

# List all messages in a conversation, ordered by created_at ascending
def list_messages_db(conversation_id: str, user_id: str):
    docs = db.collection("users") \
            .document(user_id) \
            .collection("conversations") \
            .document(conversation_id) \
            .collection("messages") \
            .order_by("created_at") \
            .stream()
            
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]