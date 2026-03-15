# Team Coordination (Pattern B) — Shared Reference

## Detecting Team Context

| Tool | How to detect |
|------|---------------|
| Claude Code | `team_name` parameter present, or assigned via `TaskList`/`TaskUpdate` |
| Other | Check for equivalent task assignment mechanism in your tool |

## Team Coordination

| Action | Claude Code | Other |
|--------|-------------|-------|
| Detect team context | `team_name` parameter present, or assigned via `TaskList`/`TaskUpdate` | Check for equivalent task assignment mechanism |
| Check teammate activity | Read `TaskList` | Check equivalent task list |
