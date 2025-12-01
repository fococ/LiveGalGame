from __future__ import annotations

import math
from functools import lru_cache
from pathlib import Path
from typing import Optional

from faster_whisper import WhisperModel

from ..core import get_settings
from ..schemas.transcription import TranscriptionResponse, TranscriptionSegment


class FasterWhisperService:
    """Wrapper around faster-whisper for offline/edge ASR."""

    def __init__(self) -> None:
        self._settings = get_settings()
        self._model = WhisperModel(
            self._settings.whisper_model_id,
            device=self._settings.whisper_device,
            compute_type=self._settings.whisper_compute_type,
        )

    def transcribe(self, audio_path: Path, language: Optional[str] = None) -> TranscriptionResponse:
        segments_iter, info = self._model.transcribe(
            str(audio_path),
            language=language,
            beam_size=5,
            vad_filter=True,
        )

        segments: list[TranscriptionSegment] = []
        for idx, segment in enumerate(segments_iter):
            confidence: float | None = None
            if segment.avg_logprob is not None:
                confidence = float(math.exp(segment.avg_logprob))
            segments.append(
                TranscriptionSegment(
                    id=idx,
                    start=float(segment.start),
                    end=float(segment.end),
                    text=segment.text.strip(),
                    confidence=confidence,
                )
            )

        return TranscriptionResponse(
            segments=segments,
            language=getattr(info, "language", language),
            duration=getattr(info, "duration", None),
            final=True,
        )


@lru_cache
def get_transcription_service() -> FasterWhisperService:
    return FasterWhisperService()
