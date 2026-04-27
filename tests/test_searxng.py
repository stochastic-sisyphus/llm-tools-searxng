import os
import pytest
import llm
from unittest.mock import patch, MagicMock


def test_tool_registered():
    """searxng_search is registered as an llm tool."""
    tools = {t.name: t for t in llm.get_tools()}
    assert "searxng_search" in tools, (
        "searxng_search not found in llm.get_tools() — "
        "check the [project.entry-points.llm] entry in pyproject.toml"
    )


def test_unset_url_raises(monkeypatch):
    """searxng_search raises RuntimeError when LLM_SEARXNG_URL is not set."""
    from llm_tools_searxng import searxng_search

    monkeypatch.delenv("LLM_SEARXNG_URL", raising=False)

    with pytest.raises(RuntimeError, match="LLM_SEARXNG_URL environment variable must be set"):
        searxng_search("test query")


def test_searxng_search_returns_markdown(monkeypatch):
    """searxng_search formats results as numbered markdown list."""
    from llm_tools_searxng import searxng_search

    monkeypatch.setenv("LLM_SEARXNG_URL", "https://your-searxng.example.com")

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "results": [
            {
                "title": "SearXNG — the privacy-respecting metasearch engine",
                "url": "https://searxng.org",
                "content": "SearXNG is a free internet metasearch engine.",
            },
            {
                "title": "GitHub: searxng/searxng",
                "url": "https://github.com/searxng/searxng",
                "content": "Source code for SearXNG.",
            },
        ]
    }
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.get", return_value=mock_response) as mock_get:
        result = searxng_search("searxng", max_results=2)

    mock_get.assert_called_once()
    call_kwargs = mock_get.call_args
    assert call_kwargs[0][0].endswith("/search")
    assert call_kwargs[1]["params"]["q"] == "searxng"
    assert call_kwargs[1]["params"]["format"] == "json"

    assert "[1]" in result
    assert "[2]" in result
    assert "SearXNG" in result
    assert "https://searxng.org" in result


def test_searxng_search_no_results(monkeypatch):
    """searxng_search returns a helpful message when no results come back."""
    from llm_tools_searxng import searxng_search

    monkeypatch.setenv("LLM_SEARXNG_URL", "https://your-searxng.example.com")

    mock_response = MagicMock()
    mock_response.json.return_value = {"results": []}
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.get", return_value=mock_response):
        result = searxng_search("xyzzy_nonexistent_query_12345")

    assert "No results" in result


def test_custom_base_url(monkeypatch):
    """LLM_SEARXNG_URL env var sets the endpoint."""
    from llm_tools_searxng import searxng_search

    monkeypatch.setenv("LLM_SEARXNG_URL", "https://my-searxng.example.com")

    mock_response = MagicMock()
    mock_response.json.return_value = {"results": []}
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.get", return_value=mock_response) as mock_get:
        searxng_search("test")

    called_url = mock_get.call_args[0][0]
    assert called_url.startswith("https://my-searxng.example.com")
