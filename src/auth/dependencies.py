# Auth for admin endpoints
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
import os

API_KEY_NAME = "Admin-API-Key"
API_KEY = os.getenv("API_KEY")

api_key_header = APIKeyHeader(
    name=API_KEY_NAME,
    auto_error=False
)

def require_api_key(api_key: str = Security(api_key_header)):
    if not api_key or api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API key"
        )
