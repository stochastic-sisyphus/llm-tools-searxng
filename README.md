# llm-tools-searxng-md

An [llm](https://llm.datasette.io/) plugin that exposes a `searxng_search_md` tool backed by a self-hosted [SearXNG](https://searxng.org/) instance.

## Why markdown output

LLMs work best with markdown. JSON-formatted search results waste tokens on syntax characters and require the model to mentally parse structure before it can reason about content. This plugin returns clean numbered lists — title, URL, and snippet — directly consumable by the model. Fewer tokens, less noise, faster answers.

It also uses `llm keys set` for URL management (no environment variable juggling required) and defaults to POST for better compatibility with most SearXNG instances.

## Installation

```bash
llm install llm-tools-searxng-md
```

Or in editable mode from source:

```bash
llm install -e /path/to/llm-tools-searxng-md
```

## Configuration

### Recommended: llm keys

```bash
llm keys set searxng_url
# paste your SearXNG instance URL when prompted
```

### Alternative: environment variable

```bash
export SEARXNG_URL=https://your-searxng.example.com
```

The URL is resolved in order: `llm keys set searxng_url` → `SEARXNG_URL` env var. **One of these is required** — there is no default.

The endpoint used is `$SEARXNG_URL/search` with `format=json` — your instance must have the JSON output format enabled in its settings.

### HTTP method

By default the plugin uses **POST** (better compatibility with most SearXNG instances). To force GET:

```bash
export SEARXNG_METHOD=GET
```

## Public SearXNG instances

If you don't run your own instance, several public ones are available. Check the [SearXNG instance list](https://searx.space/) for uptime and privacy policies before using one. A few commonly cited options:

- `https://paulgo.io`
- `https://search.brave4u.com`
- `https://searx.be`

Note: public instances may rate-limit or restrict the JSON API. Self-hosting is recommended for reliable tool use.

## Usage

After installing, the tool is automatically available to any model that supports tool calling:

```bash
llm prompt -T searxng_search_md "what is searxng"
```

Specify a model explicitly if your default does not support tools:

```bash
llm prompt -m gpt-4o -T searxng_search_md "latest news on llm tool plugins"
```

Verify the tool is registered:

```bash
llm tools
# should list: searxng_search_md
```

## Tool signature

```python
def searxng_search_md(query: str, max_results: int = 8) -> str
```

Returns the top `max_results` results as a numbered markdown list with title, URL, and snippet for each result.

## Running tests

```bash
pip install -e '.[test]'
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

## Related

- [SearXNG](https://searxng.org/) — the self-hosted metasearch engine this plugin connects to
- [llm](https://llm.datasette.io/) — the CLI and Python library this plugin extends

## License

Apache-2.0
