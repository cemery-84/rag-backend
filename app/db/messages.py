from .cosmos import messages_container
from uuid import uuid4
from datetime import datetime, timezone

def create_message_db(conversation_id: str, user_id: str, role: str, content: str):
    message = {
        "id": str(uuid4()),
        "conversation_id": conversation_id,
        "user_id": user_id,
        "role": role,
        "content": content,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    messages_container.create_item(message)
    return message

def list_messages_db(conversation_id: str):
    query = "SELECT * FROM c WHERE c.conversation_id = @conversation_id ORDER BY c.created_at ASC"
    parameters = [{"name": "@conversation_id", "value": conversation_id}]
    return list(messages_container.query_items(query=query, parameters=parameters, enable_cross_partition_query=True))