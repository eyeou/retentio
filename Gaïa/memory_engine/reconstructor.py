"""AI-assisted memory reconstruction logic for the Retentio MVP."""

from __future__ import annotations

import json
import os
from textwrap import dedent

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None  # type: ignore[assignment]

from memory_engine.models import MemoryTrace, ReconstructedMemory

SYSTEM_PROMPT = """
You are Retentio, an emotionally careful autobiographical memory reconstruction assistant.
You receive fragmented traces from a person's life and help infer a grounded, cinematic timeline.
Never claim certainty where the evidence is incomplete. Use phrases like "perhaps", "likely", and
"this may have been" when reconstructing missing pieces. Keep the tone intimate, modern, and humane.
Return only valid JSON matching this schema:
{
  "title": "short evocative title",
  "emotional_summary": "one paragraph",
  "contextual_summary": "one paragraph",
  "timeline": [{"moment": "short label", "description": "cinematic but grounded description"}],
  "sensory_details": ["detail"],
  "open_questions": ["question"]
}
""".strip()


def reconstruct_memory(
    traces: list[MemoryTrace],
    retrieved_context: list[dict[str, str]],
    user_context: str = "",
) -> ReconstructedMemory:
    """Generate a reconstructed memory from traces and retrieved context."""
    if os.getenv("OPENAI_API_KEY") and OpenAI is not None:
        return _reconstruct_with_openai(traces, retrieved_context, user_context)
    return _fallback_reconstruction(traces, retrieved_context, user_context)


def _reconstruct_with_openai(
    traces: list[MemoryTrace],
    retrieved_context: list[dict[str, str]],
    user_context: str,
) -> ReconstructedMemory:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    payload = {
        "user_context": user_context,
        "traces": [trace.__dict__ for trace in traces],
        "retrieved_context": retrieved_context,
    }

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=True)},
        ],
        response_format={"type": "json_object"},
        temperature=0.75,
    )

    content = response.choices[0].message.content or "{}"
    data = json.loads(content)
    return ReconstructedMemory(
        title=data.get("title", "A memory returning in fragments"),
        emotional_summary=data.get("emotional_summary", ""),
        contextual_summary=data.get("contextual_summary", ""),
        timeline=data.get("timeline", []),
        sensory_details=data.get("sensory_details", []),
        open_questions=data.get("open_questions", []),
        tavily_context=retrieved_context,
    )


def _fallback_reconstruction(
    traces: list[MemoryTrace],
    retrieved_context: list[dict[str, str]],
    user_context: str,
) -> ReconstructedMemory:
    text_fragments = [trace.content for trace in traces if trace.content]
    first_fragment = text_fragments[0] if text_fragments else "a few traces waiting to be understood"
    context_line = user_context or "The exact time and place are still soft around the edges."

    timeline = [
        {
            "moment": "The first trace",
            "description": f"The reconstruction begins with {first_fragment[:180].strip()}. It feels like the opening shot of a memory returning slowly, with the available evidence held gently rather than forced into certainty.",
        },
        {
            "moment": "A surrounding world",
            "description": f"Context suggests: {context_line[:220].strip()} The memory may belong to a moment where place, mood, and small sensory details mattered more than exact chronology.",
        },
        {
            "moment": "What remains",
            "description": "The fragments point toward an emotionally meaningful scene, but the missing pieces are still useful. They show where the user may want to look next: people present, weather, music, objects, or the reason this moment stayed half-lit in memory.",
        },
    ]

    return ReconstructedMemory(
        title="A Memory Returning In Fragments",
        emotional_summary="This looks like a memory with tenderness around it: incomplete, but not empty. The fragments suggest a moment that may have been ordinary at the time and emotionally charged in retrospect.",
        contextual_summary=dedent(
            f"""
            Retentio is running in local fallback mode because no OpenAI API key is configured.
            The reconstruction uses the uploaded traces and any user-provided context, but it does not hallucinate external facts.
            """
        ).strip(),
        timeline=timeline,
        sensory_details=[
            "Light, weather, or room tone may help locate the scene.",
            "Names, clothing, music, and repeated phrases are strong autobiographical anchors.",
            "Photos and voice notes often carry mood before they carry facts.",
        ],
        open_questions=[
            "Who else might have been nearby?",
            "What happened immediately before or after this fragment?",
            "Which detail feels emotionally true even if the date is uncertain?",
        ],
        tavily_context=retrieved_context,
    )
