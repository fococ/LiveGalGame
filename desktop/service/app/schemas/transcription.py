from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class TranscriptionSegment(BaseModel):
    id: int = Field(..., description="Segment index")
    start: float = Field(..., description="Start time in seconds")
    end: float = Field(..., description="End time in seconds")
    text: str = Field(..., description="Recognized text")
    confidence: float | None = Field(
        default=None, description="Optional confidence score provided by the model"
    )


class TranscriptionResponse(BaseModel):
    segments: List[TranscriptionSegment] = Field(default_factory=list)
    language: str | None = Field(default=None, description="Detected or specified language")
    duration: float | None = Field(default=None, description="Estimated audio duration in seconds")
    final: bool = Field(default=True, description="Indicates whether the result is final or partial")
