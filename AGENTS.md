# Development Guide

Rules for agents (and humans) contributing to this repository.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) — Python dependency management and test execution

## Shared Snippets

Reusable documentation fragments live in `snippets/`. Each snippet's body
(everything below the H1 title) is inlined into the skill `ENV.md` files that
need it — heading levels may be adjusted to fit the target document, but the
body content must stay identical.

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

## Rubric Linter

Shared rules (eligibility, priority, label protocol, etc.) from
`skills/reading-guild-rules/SKILL.md` are codified in
`rubrics/shared-rules.yaml`. The test `tests/test_rubric_lint.py` uses
`pytest-llm-rubric` (LLM-as-judge) to verify that each targeted
`SKILL.md` semantically expresses the relevant rules.

```bash
uv run pytest tests/test_rubric_lint.py -v
```

Requires an LLM backend. Configure `llm_rubric_auto_models` in
`pyproject.toml` (Ollama by default; falls back to Anthropic if
`ANTHROPIC_API_KEY` is set). See `pyproject.toml` for the current list.

The rubric lint is also wired as a pre-commit hook (`rubric-lint`),
triggered only when `skills/*/SKILL.md` or `rubrics/` files change.
If no LLM backend is available, skip with `git commit --no-verify`.
