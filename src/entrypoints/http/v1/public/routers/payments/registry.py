from fastapi import APIRouter

from . import create
from . import get


router = APIRouter()

router.include_router(create.router)
router.include_router(get.router)
