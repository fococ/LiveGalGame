from functools import lru_cache
from typing import Literal

from pydantic import BaseModel, Field


class Settings(BaseModel):
    """应用配置."""

    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4.1-mini", alias="OPENAI_MODEL")
    service_port: int = Field(default=8080, alias="SERVICE_PORT")
    memory_backend: Literal["in-memory", "mem0", "graphti"] = Field(
        default="in-memory", alias="MEMORY_BACKEND"
    )

    class Config:
        populate_by_name = True
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
