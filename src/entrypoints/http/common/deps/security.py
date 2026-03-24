from fastapi import Header
from fastapi import HTTPException
from fastapi import status

from src.configuration import settings


async def dependency(key: str = Header(..., alias="X-API-Key")) -> None:
    if key != settings.API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
