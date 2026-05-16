"""Lightweight data models used by the Retentio MVP."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MemoryTrace:
    trace_type: str
    content: str
    source_name: str = "manual"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ReconstructedMemory:
    title: str
    emotional_summary: str
    contextual_summary: str
    timeline: list[dict[str, str]]
    sensory_details: list[str]
    open_questions: list[str]
    tavily_context: list[dict[str, str]]

    def to_markdown(self) -> str:
        timeline_md = "\n".join(
            f"### {item.get('moment', 'A remembered moment')}\n{item.get('description', '')}"
            for item in self.timeline
        )
        sensory_md = "\n".join(f"- {detail}" for detail in self.sensory_details)
        questions_md = "\n".join(f"- {question}" for question in self.open_questions)
        context_md = "\n".join(
            f"- [{item.get('title', 'Context source')}]({item.get('url', '#')}) - {item.get('content', '')}"
            for item in self.tavily_context
        )

        return f"""
# {self.title}

## Emotional Core
{self.emotional_summary}

## Reconstructed Timeline
{timeline_md or "No timeline could be reconstructed yet."}

## Context
{self.contextual_summary}

## Sensory Anchors
{sensory_md or "- No sensory anchors detected yet."}

## Questions To Keep Exploring
{questions_md or "- What detail still feels just out of reach?"}

## Retrieved Context
{context_md or "No external context retrieved. Add a Tavily API key to enrich this section."}
""".strip()
