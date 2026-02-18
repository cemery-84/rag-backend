from .cosmos import conversations_container, messages_container
from uuid import uuid4
from datetime import datetime, timezone

def create_conversation_db(user_id: str, title: str | None = None):
    conversation = {
        "id": str(uuid4()),
        "user_id": user_id,
        "title": title or "New Conversation",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    conversations_container.create_item(conversation)
    return conversation

def list_conversations_db(user_id: str):
    query = "SELECT * FROM c WHERE c.user_id = @user_id ORDER BY c.updated_at DESC"
    parameters = [{"name": "@user_id", "value": user_id}]
    return list(conversations_container.query_items(query=query, parameters=parameters, enable_cross_partition_query=True))

def delete_conversation_db(conversation_id: str, user_id: str):
    conversations_container.delete_item(item=conversation_id, partition_key=user_id)