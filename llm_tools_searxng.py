import os

import httpx
import llm


@llm.hookimpl
def register_tools(register):
    register(searxng_search)


def searxng_search(query: str, max_results: int = 8) -> str:
    """Search the web via self-hosted SearXNG. Returns top results as markdown.

    Args:
        query: Search query string
        max_results: Max number of results to return (default 8)
    """
    base = os.environ.get("LLM_SEARXNG_URL")
    if not base:
        raise RuntimeError(
            "LLM_SEARXNG_URL environment variable must be set to your SearXNG instance URL"
        )
    r = httpx.get(
        f"{base}/search",
        params={"q": query, "format": "json"},
        timeout=15,
    )
    r.raise_for_status()
    data = r.json()
    results = data.get("results", [])[:max_results]
    if not results:
        return f"No results for: {query}"
    out = []
    for i, res in enumerate(results, 1):
        title = res.get("title", "").strip()
        url = res.get("url", "")
        content = res.get("content", "").strip()
        out.append(f"[{i}] {title}\n  {url}\n  {content}\n")
    return "\n".join(out)
