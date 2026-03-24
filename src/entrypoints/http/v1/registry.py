from fastapi import APIRouter

from . import public


router = APIRouter(prefix="/v1")

router.include_router(public.router)
