# Environment-Specific Commands

**Prerequisites**: see [shared/PREREQUISITES.md](../shared/PREREQUISITES.md).

## Tool Name

When filling in `<tool-name>` in the claim comment, use the name of the tool you
are currently running under:

| Environment       | Tool name         |
|-------------------|-------------------|
| Claude Code CLI   | `Claude Code`     |
| GitHub Copilot    | `GitHub Copilot`  |
| Gemini CLI        | `Gemini CLI`      |
| Antigravity       | `Antigravity`     |

## Plan Approval (Pattern A)

Present the implementation plan and request user approval before writing code.

| Tool | How |
|------|-----|
| Claude Code | `EnterPlanMode` |
| Other | Output the plan as text and ask the user to confirm |

## Team Coordination (Pattern B)

See [shared/TEAM.md](../shared/TEAM.md) for detecting team context and base
coordination commands.

**Skill-specific actions:**

| Action | Claude Code | Other |
|--------|-------------|-------|
| Send plan for approval | `SendMessage` to Team Lead | Use available messaging tool |
| Notify PR ready | `SendMessage` to Team Lead with PR URL | Use available messaging tool |
