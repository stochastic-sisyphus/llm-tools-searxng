# llm-tools-searxng

An [llm](https://llm.datasette.io/) plugin that exposes a `searxng_search` tool backed by a self-hosted [SearXNG](https://searxng.org/) instance.

## Installation

```bash
llm install llm-tools-searxng
```

Or in editable mode from source:

```bash
llm install -e /path/to/llm-tools-searxng
```

## Configuration

Set `LLM_SEARXNG_URL` to point at your SearXNG instance. Defaults to `https://search.schrodingers.lol`.

```bash
export LLM_SEARXNG_URL=https://your-searxng.example.com
```

The endpoint used is `$LLM_SEARXNG_URL/search?q=QUERY&format=json` — your instance must have the JSON output format enabled in its settings.

## Usage

After installing, the tool is automatically available to any model that supports tool calling:

```bash
llm prompt -T searxng_search "what is searxng"
```

Specify a model explicitly if your default does not support tools:

```bash
llm prompt -m gpt-4o -T searxng_search "latest news on llm tool plugins"
```

Verify the tool is registered:

```bash
llm tools
# should list: searxng_search
```

## Tool signature

```python
def searxng_search(query: str, max_results: int = 8) -> str
```

Returns the top `max_results` results as a numbered markdown list with title, URL, and snippet for each result.

## Running tests

```bash
pip install pytest
pytest tests/
```

## Publishing to PyPI

Build and publish with `uv`:

```bash
uv build
uv publish
```

Or with the standard toolchain:

```bash
pip install build twine
python -m build
twine upload dist/*
```

Bump `version` in `pyproject.toml` before each release.

## License

Apache-2.0
