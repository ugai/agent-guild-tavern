# Prerequisites

All Guild skills require the following tools to be installed and available on
`PATH`.

| Tool | Minimum version | Purpose |
|------|----------------|---------|
| `git` | 2.20+ | Worktree management, branching, commits |
| `gh` | 2.0+ | GitHub issue/PR operations (create, edit, list, comment, merge) |

## Verification

```bash
git --version
gh --version
gh auth status
```

`gh auth status` must show an authenticated session with sufficient repository
permissions (read/write access to Issues and Pull Requests). Authentication
methods vary — classic PATs use the `repo` scope, fine-grained PATs and GitHub
App tokens use granular permissions instead.
