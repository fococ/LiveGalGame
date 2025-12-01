from __future__ import annotations

import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.concurrency import run_in_threadpool

from ....services import get_transcription_service
from ....schemas.transcription import TranscriptionResponse

router = APIRouter(prefix="/transcribe", tags=["transcription"])


async def _persist_upload(upload: UploadFile) -> Path:
    suffix = Path(upload.filename or "audio").suffix
    if not suffix:
        suffix = ".webm"

    with NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        while True:
            chunk = await upload.read(1024 * 1024)
            if not chunk:
                break
            tmp_file.write(chunk)
        tmp_path = Path(tmp_file.name)

    await upload.close()
    return tmp_path


@router.post("", response_model=TranscriptionResponse)
async def transcribe_audio(
    file: UploadFile = File(..., description="音频文件，推荐 16-bit PCM wav/webm"),
    language: str | None = Form(default=None, description="可选，指定语言代码，例如 zh 或 en"),
) -> TranscriptionResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="缺少文件名")

    if file.content_type and not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=415, detail="仅支持音频文件上传")

    tmp_path = await _persist_upload(file)
    service = get_transcription_service()

    try:
        result = await run_in_threadpool(service.transcribe, tmp_path, language)
    except Exception as exc:  # pylint: disable=broad-except
        raise HTTPException(status_code=500, detail=f"转写失败: {exc}") from exc
    finally:
        try:
            os.unlink(tmp_path)
        except FileNotFoundError:
            pass

    return result
