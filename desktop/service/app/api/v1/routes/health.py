from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", summary="服务存活检查")
def read_health() -> dict[str, str]:
    return {"status": "ok"}
