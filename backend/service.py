"""Backend orchestration for the Retentio MVP."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from memory_engine.context_retriever import retrieve_context
from memory_engine.models import MemoryTrace, ReconstructedMemory
from memory_engine.reconstructor import reconstruct_memory
from memory_engine.transcription import transcribe_voice_note


def reconstruct_from_inputs(
    text_fragments: str,
    photo_files: Iterable[str] | None,
    voice_note: str | None,
    user_context: str,
) -> ReconstructedMemory:
    """Convert raw UI inputs into memory traces and reconstruct a timeline."""
    traces = _build_traces(text_fragments, photo_files, voice_note)
    tavily_query = _build_context_query(traces, user_context)
    retrieved_context = retrieve_context(tavily_query)
    return reconstruct_memory(traces, retrieved_context, user_context=user_context)


def _build_traces(
    text_fragments: str,
    photo_files: Iterable[str] | None,
    voice_note: str | None,
) -> list[MemoryTrace]:
    traces: list[MemoryTrace] = []

    for index, fragment in enumerate(_split_fragments(text_fragments), start=1):
        traces.append(
            MemoryTrace(
                trace_type="text",
                content=fragment,
                source_name=f"text fragment {index}",
            )
        )

    for path in photo_files or []:
        file_path = Path(path)
        traces.append(
            MemoryTrace(
                trace_type="photo",
                content=f"Uploaded photo: {file_path.name}",
                source_name=file_path.name,
                metadata={"path": str(file_path)},
            )
        )

    transcript = transcribe_voice_note(voice_note)
    if transcript:
        traces.append(
            MemoryTrace(
                trace_type="voice_note",
                content=transcript,
                source_name=Path(voice_note).name if voice_note else "voice note",
            )
        )

    if not traces:
        traces.append(
            MemoryTrace(
                trace_type="empty_prompt",
                content="The user has not added traces yet.",
                source_name="system",
            )
        )

    return traces


def _split_fragments(text: str) -> list[str]:
    if not text.strip():
        return []
    parts = [part.strip(" -\n\t") for part in text.replace("\r", "").split("\n")]
    return [part for part in parts if part]


def _build_context_query(traces: list[MemoryTrace], user_context: str) -> str:
    trace_text = " ".join(trace.content for trace in traces if trace.trace_type != "photo")
    combined = f"{user_context} {trace_text}".strip()
    if not combined:
        return "autobiographical memory reconstruction emotional context"
    return f"historical local cultural context for autobiographical memory fragments: {combined[:400]}"
