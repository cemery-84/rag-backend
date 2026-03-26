import firebase_admin
from firebase_admin import auth, credentials
from fastapi import HTTPException, status
import logging

from app.auth.firebase_config import FIREBASE_STORAGE_BUCKET

logger = logging.getLogger(__name__)

# Load the service account JSON file
cred = credentials.ApplicationDefault()

# Initialize the Firebase app
firebase_admin.initialize_app(cred, {
    "storageBucket": FIREBASE_STORAGE_BUCKET
})

def verify_firebase_token(token: str):
    try:
        # Verify the token and decode it
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        logger.error("Invalid Firebase token")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Firebase token: {str(e)}")