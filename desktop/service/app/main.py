from dotenv import load_dotenv
from fastapi import FastAPI

from .core import get_settings
from .api.v1.routes import router as api_router

load_dotenv()
settings = get_settings()

app = FastAPI(
    title="LiveGalGame Desktop Service",
    version="0.1.0",
    description="FastAPI 服务，负责语音转写、记忆与 LLM 建议",
)

app.include_router(api_router)


@app.get("/", summary="根路由说明")
def root() -> dict[str, str]:
    return {"service": app.title, "status": "ready"}
