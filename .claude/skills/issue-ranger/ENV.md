# Environment-Specific Commands

**Prerequisites**: see [shared/PREREQUISITES.md](../shared/PREREQUISITES.md).

## Plan Approval (Pattern A)

Present the issue list and request user approval before posting anything.

| Tool | How |
|------|-----|
| Claude Code | `EnterPlanMode` |
| Other | Output the list as text and ask the user to confirm |

## Team Coordination (Pattern B)

See [shared/TEAM.md](../shared/TEAM.md) for detecting team context and base
coordination commands.

**Skill-specific actions:**

| Action | Claude Code | Other |
|--------|-------------|-------|
| Send issue list for approval | `SendMessage` to Team Lead | Use available messaging tool |
| Report posted issues | `SendMessage` to Team Lead | Use available messaging tool |

## Writing and Deleting Temp Files

Write the issue body to `issue_body_<N>.md`, then delete it after each issue.

Prefer your native file-write tool for reliability. Fall back to shell
commands if no native tool is available.
