# Environment-Specific Commands

## Prerequisites

All Guild skills require the following tools to be installed and available on
`PATH`.

| Tool | Minimum version | Purpose |
|------|----------------|---------|
| `git` | 2.20+ | Worktree management, branching, commits |
| `gh` | 2.0+ | GitHub issue/PR operations (create, edit, list, comment, merge) |

### Verification

```bash
git --version
gh --version
gh auth status
```

`gh auth status` must show an authenticated session with sufficient repository
permissions (read/write access to Issues and Pull Requests). Authentication
methods vary — classic PATs use the `repo` scope, fine-grained PATs and GitHub
App tokens use granular permissions instead.

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

### Detecting Team Context

| Tool | How to detect |
|------|---------------|
| Claude Code | `team_name` parameter present, or assigned via `TaskList`/`TaskUpdate` |
| Other | Check for equivalent task assignment mechanism in your tool |

### Team Coordination

| Action | Claude Code | Other |
|--------|-------------|-------|
| Detect team context | `team_name` parameter present, or assigned via `TaskList`/`TaskUpdate` | Check for equivalent task assignment mechanism |
| Check teammate activity | Read `TaskList` | Check equivalent task list |

**Skill-specific actions:**

| Action | Claude Code | Other |
|--------|-------------|-------|
| Send plan for approval | `SendMessage` to Team Lead | Use available messaging tool |
| Notify PR ready | `SendMessage` to Team Lead with PR URL | Use available messaging tool |
