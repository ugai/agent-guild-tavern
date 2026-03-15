"""Verify that shared snippets are inlined verbatim in skill ENV.md files.

Heading levels may differ (snippets use H1/H2; ENV.md embeds at H2/H3), so
comparison normalizes all headings to a flat level before matching.
"""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SNIPPETS_DIR = ROOT / "snippets"
SKILLS_DIR = ROOT / "skills"

# Mapping: snippet filename -> list of skill directories that must contain it
SNIPPET_TARGETS: dict[str, list[str]] = {
    "PREREQUISITES.md": [
        "issue-ranger",
        "issue-slayer",
        "quality-finisher",
    ],
    "TEAM.md": [
        "issue-ranger",
        "issue-slayer",
    ],
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _normalize_headings(text: str) -> str:
    """Collapse all Markdown heading prefixes to a single '#'."""
    return re.sub(r"^(#{1,6}) ", "# ", text, flags=re.MULTILINE)


def _snippet_params():
    for snippet_name, skills in SNIPPET_TARGETS.items():
        for skill in skills:
            yield pytest.param(snippet_name, skill, id=f"{skill}/{snippet_name}")


@pytest.mark.parametrize(("snippet_name", "skill_name"), list(_snippet_params()))
def test_snippet_present_in_env(snippet_name: str, skill_name: str):
    snippet_path = SNIPPETS_DIR / snippet_name
    env_path = SKILLS_DIR / skill_name / "ENV.md"

    assert snippet_path.exists(), f"Snippet not found: {snippet_path}"
    assert env_path.exists(), f"ENV.md not found: {env_path}"

    snippet_content = _read(snippet_path).strip()
    env_content = _read(env_path)

    # Strip the H1 title line from the snippet
    lines = snippet_content.splitlines()
    if lines and lines[0].startswith("# "):
        snippet_body = "\n".join(lines[1:]).strip()
    else:
        snippet_body = snippet_content

    normalized_snippet = _normalize_headings(snippet_body)
    normalized_env = _normalize_headings(env_content)

    assert normalized_snippet in normalized_env, (
        f"Snippet '{snippet_name}' content not found in {skill_name}/ENV.md.\n"
        f"Update the ENV.md to match the snippet, or update the snippet if "
        f"the content has intentionally changed."
    )
