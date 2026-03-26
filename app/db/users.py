from .firestore import db
from datetime import datetime, timezone

# Users are stored in Firestore under the collection: users/{user_id}

# Ensure a user document exists for the given user_id. If it doesn't exist, create it with the provided email.
def ensure_user_exists(user_id: str, email: str = None):
    ref = db.collection("users").document(user_id)
    doc = ref.get()
    
    if doc.exists:
        return {"id": doc.id, **doc.to_dict()}
    
    user_data = {
        "email": email,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    ref.set(user_data)
    return {"id": user_id, **user_data}