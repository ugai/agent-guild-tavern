"""Verify that shared snippets are inlined verbatim in skill ENV.md files.

Heading levels may differ (snippets use H1/H2; ENV.md embeds at H2/H3), so
comparison tries multiple heading offsets to find a match.
"""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SNIPPETS_DIR = ROOT / "snippets"
SKILLS_DIR = ROOT / "plugins" / "guild-tavern" / "skills"

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
        "quality-finisher",
    ],
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _strip_h1(text: str) -> str:
    """Remove the leading H1 title line from snippet content."""
    lines = text.strip().splitlines()
    if lines and lines[0].startswith("# "):
        return "\n".join(lines[1:]).strip()
    return text.strip()


def _shift_headings(text: str, offset: int) -> str:
    """Shift all Markdown headings by offset levels (positive = deeper)."""
    if offset == 0:
        return text

    def _shift(m: re.Match) -> str:
        current = len(m.group(1))
        new_level = min(6, max(1, current + offset))
        return "#" * new_level + " "

    return re.sub(r"^(#{1,6}) ", _shift, text, flags=re.MULTILINE)


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

    snippet_body = _strip_h1(_read(snippet_path))
    env_content = _read(env_path)

    # Try heading offsets 0..+3 to account for nesting depth differences
    for offset in range(4):
        shifted = _shift_headings(snippet_body, offset)
        if shifted in env_content:
            return

    pytest.fail(
        f"Snippet '{snippet_name}' content not found in {skill_name}/ENV.md "
        f"(tried heading offsets 0..+3).\n"
        f"Update the ENV.md to match the snippet, or update the snippet if "
        f"the content has intentionally changed."
    )


def test_snippet_targets_complete():
    """Ensure every snippet in snippets/ is listed in SNIPPET_TARGETS."""
    snippet_files = {p.name for p in SNIPPETS_DIR.glob("*.md")}
    registered = set(SNIPPET_TARGETS.keys())
    missing = snippet_files - registered
    assert not missing, (
        f"Snippet files not registered in SNIPPET_TARGETS: {missing}\n"
        f"Add them to SNIPPET_TARGETS with their target skill list."
    )
