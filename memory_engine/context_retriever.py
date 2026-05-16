"""Context retrieval for Retentio using Tavily when available."""

from __future__ import annotations

import os

try:
    from tavily import TavilyClient
except ImportError:  # pragma: no cover - lets the app boot before dependencies are installed.
    TavilyClient = None  # type: ignore[assignment]


def retrieve_context(query: str, max_results: int = 4) -> list[dict[str, str]]:
    """Retrieve compact contextual references for a memory reconstruction."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key or not query.strip() or TavilyClient is None:
        return []

    client = TavilyClient(api_key=api_key)
    response = client.search(
        query=query,
        search_depth="basic",
        max_results=max_results,
        include_answer=True,
    )

    results: list[dict[str, str]] = []
    if response.get("answer"):
        results.append(
            {
                "title": "Tavily synthesis",
                "url": "https://tavily.com",
                "content": response["answer"],
            }
        )

    for item in response.get("results", [])[:max_results]:
        results.append(
            {
                "title": item.get("title", "Context source"),
                "url": item.get("url", ""),
                "content": item.get("content", "")[:600],
            }
        )

    return results[:max_results]
