from fastapi import Header, HTTPException, status
from .firebase_verify import verify_firebase_token
import logging

logger = logging.getLogger(__name__)

async def get_current_user(Authorization: str = Header(None)):
    if not Authorization:
        logger.error("Missing Authorization header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header"
        )

    if not Authorization.startswith("Bearer "):
        logger.error("Invalid Authorization header format")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format"
        )

    token = Authorization.split(" ", 1)[1]
    return verify_firebase_token(token)
