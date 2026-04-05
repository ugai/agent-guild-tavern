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

## Plan Approval (Pattern A)

Present the issue list and request user approval before posting anything.

| Tool | How |
|------|-----|
| Claude Code | `EnterPlanMode` |
| Other | Output the list as text and ask the user to confirm |

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
| Send issue list for approval | `SendMessage` to Team Lead | Use available messaging tool |
| Report posted issues | `SendMessage` to Team Lead | Use available messaging tool |

## Writing and Deleting Temp Files

Write the issue body to `issue_body_<N>.tmp.md`, then delete it after each issue.

Prefer your native file-write tool for reliability. Fall back to shell
commands if no native tool is available.
