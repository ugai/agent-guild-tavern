"""Verify that shared rules are expressed in each targeted SKILL.md.

Uses pytest-llm-rubric's LLM-as-judge infrastructure to semantically
check whether a SKILL.md document expresses a given rule from the shared
rubric (rubrics/shared-rules.yaml).

Three-pass verification:
  1. Does the skill document itself express the rule (inline)?
  2. If not, does the skill reference the canonical source document?
  3. If so, does that reference document define the rule?
"""

from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
RUBRIC_PATH = ROOT / "rubrics" / "shared-rules.yaml"
SKILLS_DIR = ROOT / "skills"


def _load_rubric() -> dict:
    return yaml.safe_load(RUBRIC_PATH.read_text(encoding="utf-8"))


def _params():
    rubric = _load_rubric()
    for criterion in rubric["criteria"]:
        for skill in criterion["skills"]:
            yield pytest.param(
                criterion["id"],
                criterion["rule"],
                skill,
                rubric["reference_doc"],
                id=f"{skill}/{criterion['id']}",
            )


def _judge(judge_llm, system: str, user: str) -> str:
    return judge_llm.complete([
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ])


SYSTEM_INLINE = (
    "You are a documentation auditor. You will receive a rule and a "
    "skill document. Determine whether the skill document expresses "
    "the given rule — it does not need to use identical wording, but "
    "the semantics must be present. Reply PASS if the rule is "
    "expressed, or FAIL followed by a brief explanation if not."
)

SYSTEM_REFERENCE = (
    "You are a documentation auditor. You will receive a skill document "
    "and a reference document path. Determine whether the skill document "
    "contains a reference (link, path, or mention) to the given reference "
    "document. The reference may use a relative path (e.g., "
    "'../reading-guild-rules/SKILL.md') instead of the full path from the "
    "repository root — treat these as equivalent. "
    "Reply PASS if there is a reference, or FAIL if not."
)

SYSTEM_RULE_IN_REF = (
    "You are a documentation auditor. You will receive a rule and a "
    "reference document. Determine whether the reference document "
    "defines or expresses the given rule. Reply PASS if the rule is "
    "present, or FAIL followed by a brief explanation if not."
)


@pytest.mark.parametrize(
    ("criterion_id", "rule", "skill_name", "reference_doc"),
    list(_params()),
)
def test_shared_rule_expressed(
    criterion_id, rule, skill_name, reference_doc, judge_llm
):
    skill_path = SKILLS_DIR / skill_name / "SKILL.md"
    assert skill_path.exists(), f"SKILL.md not found: {skill_path}"
    skill_content = skill_path.read_text(encoding="utf-8")

    # Pass 1: rule expressed inline?
    inline_response = _judge(
        judge_llm,
        SYSTEM_INLINE,
        f"## Rule\n{rule.strip()}\n\n"
        f"## Skill Document ({skill_name}/SKILL.md)\n{skill_content}",
    )
    if "PASS" in inline_response:
        return  # Rule is expressed inline — done.

    # Pass 2: skill references the canonical document?
    ref_response = _judge(
        judge_llm,
        SYSTEM_REFERENCE,
        f"## Reference Document Path\n{reference_doc}\n\n"
        f"## Skill Document ({skill_name}/SKILL.md)\n{skill_content}",
    )
    assert "PASS" in ref_response, (
        f"Criterion '{criterion_id}' not satisfied in {skill_name}/SKILL.md.\n"
        f"The rule is neither expressed inline nor is there a reference to "
        f"'{reference_doc}'.\n"
        f"Inline judge: {inline_response}\n"
        f"Reference judge: {ref_response}"
    )

    # Pass 3: rule defined in the reference document?
    ref_path = ROOT / reference_doc
    assert ref_path.exists(), f"Reference doc not found: {ref_path}"
    ref_content = ref_path.read_text(encoding="utf-8")

    rule_response = _judge(
        judge_llm,
        SYSTEM_RULE_IN_REF,
        f"## Rule\n{rule.strip()}\n\n"
        f"## Reference Document ({reference_doc})\n{ref_content}",
    )
    assert "PASS" in rule_response, (
        f"Criterion '{criterion_id}': {skill_name}/SKILL.md references "
        f"'{reference_doc}', but the rule is not defined there.\n"
        f"Judge response: {rule_response}"
    )
