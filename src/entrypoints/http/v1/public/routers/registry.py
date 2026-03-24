from fastapi import APIRouter

from . import payments


router = APIRouter()

router.include_router(payments.router)
