from fastapi import Header


async def dependency(key: str = Header(..., alias="Idempotency-Key")) -> str:
    return key
