from fastapi import APIRouter

from . import health, transcribe

router = APIRouter(prefix="/api/v1")
router.include_router(health.router)
router.include_router(transcribe.router)

__all__ = ["router"]
