"""Voice note transcription for Retentio."""

from __future__ import annotations

import os
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None  # type: ignore[assignment]


def transcribe_voice_note(audio_path: str | None) -> str:
    """Transcribe a voice note with OpenAI Whisper-compatible transcription."""
    if not audio_path:
        return ""

    path = Path(audio_path)
    if not path.exists():
        return ""

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or OpenAI is None:
        return f"Voice note uploaded: {path.name}. Add OPENAI_API_KEY to enable transcription."

    client = OpenAI(api_key=api_key)
    with path.open("rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
        )

    return getattr(transcript, "text", "") or ""
