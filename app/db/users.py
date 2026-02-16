from .cosmos import users_container
from datetime import datetime

import logging
logger = logging.getLogger(__name__)

def ensure_user_exists(user_id: str, email: str = None):
    try:
        # Try to read the user, if it doesn't exist an exception will be thrown
        return users_container.read_item(item=user_id, partition_key=user_id)
    except Exception:
        logger.info(f"User {user_id} not found, creating new user.")
        
        # Create the user if it doesn't exist
        user = {
            "id": user_id,
            "email": email,
            "created_at": datetime.now(datetime.timezone.utc)
        }
        users_container.create_item(user)
        return user