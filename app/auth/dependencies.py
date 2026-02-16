from fastapi import Header, HTTPException, status
from .firebase_verify import verify_firebase_token

import logging
logger = logging.getLogger(__name__)

async def get_current_user(authorization: str = Header(...)):
    if not authorization:
        logger.error("Missing authorization header")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization header")
    
    scheme, _, token = authorization.partition(" ")
    
    if scheme.lower() != "bearer" or not token:
        logger.error("Invalid authorization header format")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header")
    
    return verify_firebase_token(token)
