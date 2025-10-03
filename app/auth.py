from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from app.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_admin_key(api_key: str = Security(api_key_header)):
    if not api_key or api_key != settings.admin_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing admin API key"
        )
    return api_key


async def verify_ai_key(api_key: str = Security(api_key_header)):
    if not api_key or api_key != settings.ai_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing AI API key"
        )
    return api_key
