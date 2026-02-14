import requests
from jose import jwt
from fastapi import HTTPException, status

from .firebase_config import (
    FIREBASE_PROJECT_ID,
    FIREBASE_ISSUER,
    FIREBASE_JWKS_URL,
)

JWKS_CACHE = {}

def get_firebase_public_keys():
    global JWKS_CACHE
    if not JWKS_CACHE:
        response = requests.get(FIREBASE_JWKS_URL)
        response.raise_for_status()
        JWKS_CACHE = response.json()
    return JWKS_CACHE

def verify_firebase_token(token: str):
    try:
        header = jwt.get_unverified_header(token)
        kid = header.get("kid")
        
        if not kid:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token header")

        public_keys = get_firebase_public_keys()
        
        if kid not in public_keys:
            JWKS_CACHE.clear()  # Clear cache and try again
            public_keys = get_firebase_public_keys()
            
            if kid not in public_keys:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token key")
        
        public_key = public_keys[kid]

        decoded_token = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=FIREBASE_PROJECT_ID,
            issuer=FIREBASE_ISSUER,
        )
        return decoded_token
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=f"Invalid Firebase token: {str(e)}",
        )