# Development Guide

Rules for agents (and humans) contributing to this repository.

## Shared Snippets

Reusable documentation fragments live in `snippets/`. Each snippet is inlined
verbatim into the skill `ENV.md` files that need it — heading levels may be
adjusted to fit the target document, but the content must stay identical.

**When editing a snippet:**

1. Edit the source file in `snippets/`
2. Copy the updated content into every target `ENV.md` listed in
   `tests/test_snippet_sync.py::SNIPPET_TARGETS`
3. Run `uv run pytest tests/test_snippet_sync.py` to verify consistency

The snippet sync test is also wired as a pre-commit hook.

## Pre-commit Hooks

Install with:

```bash
uv tool install pre-commit   # or: pip install pre-commit
pre-commit install
```

Hooks run automatically on commit. To run manually:

```bash
pre-commit run --all-files
```

## Testing

```bash
uv run pytest
```
