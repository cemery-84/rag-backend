from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from .firebase_verify import verify_firebase_token

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials    
    return verify_firebase_token(token)
