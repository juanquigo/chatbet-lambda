from fastapi import APIRouter

from . import digitain

router = APIRouter(prefix="/provider")
router.include_router(digitain.router, prefix="/digitain", tags=["digitain"])
