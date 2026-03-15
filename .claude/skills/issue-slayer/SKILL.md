---
name: issue-slayer
description: >
  Implements a single GitHub Issue end-to-end inside an isolated git worktree
  and opens a pull request. Use when asked to pick up an issue, implement a
  fix or feature, or deliver a PR. Requires the agent:ready label. NOT for
  discovering issues (use issue-ranger) or running a full sprint (use
  dispatching-guild-expedition). Does NOT merge PRs.
---

# Issue Slayer

Run a complete Issue → PR flow inside an isolated git worktree.

## Execution Mode

**Pattern A (Standalone)**: Present a plan for user approval before writing
code. User drives cleanup decisions.

**Pattern B (Team Member)**: Send plans to the Team Lead for approval before
writing code. Cleanup requires Lead instruction.

Detection: see [ENV.md](ENV.md) for how to detect team context in your tool.

## Issue Selection

**Eligibility** — ALL must be true:

1. Has `agent:ready` label
2. State is `open`
3. Not assigned (`no:assignee`)
4. Does NOT have `pending` label

**Priority**: `bug` > `enhancement`, then `p0` > `p1` > `p2` > `p3`
(no label = p2), then lowest issue number.

**Never** pick without `agent:ready`. **Never** pick an assigned issue.
One agent, one issue — unless working a **Bundle PR** (see `AGENTS.md`).

```bash
gh issue list --label "agent:ready" \
  --search "no:assignee state:open -label:pending" \
  --json number,title,labels --limit 20
```

If the user specifies an issue number, verify eligibility before proceeding.

**Pattern A**: Present the ranked list and let the user choose.
**Pattern B**: Check what teammates have claimed via task list. Pick the
highest-priority unclaimed issue, or use the one assigned to you.

Claim immediately after selection:

```bash
gh issue edit <N> --add-assignee "@me"
gh issue comment <N> --body "Starting work.
Agent: **<agent-name>** | Model: **<model-name>** | Tool: **<tool-name>**"
```

If assignment fails (race condition), pick another issue.

## Worktree Setup

See [WORKTREE.md](WORKTREE.md) for the full setup procedure. Summary:

```bash
git fetch origin main
git worktree add .agent-worktrees/<type>-issue-<N>-<desc> \
  -b <type>/issue-<N>-<desc> origin/main
```

If the path already exists, abort and ask the user. Do all subsequent work
inside the worktree.

## Design

Read the issue, relevant source files, and the project's development
documentation (`CLAUDE.md`, `CONTRIBUTING.md`, etc.).

**Pattern A**: Present the implementation plan and wait for approval before
writing code.
**Pattern B**: Send the plan to the Lead and wait for approval.

Do not create an `implementation_plan.md` file — plans belong in conversation
context or plan mode, not as file artifacts in the repository (whether
committed or not).

## Implementation

- Follow the project's coding standards and conventions.
- Co-author trailer: see Commit & PR Conventions in `AGENTS.md`.
- **Pattern B**: Minimize changes to files that the project identifies as
  conflict-prone.

**Doc updates** (part of implementation, not a separate step):
Update project documentation to reflect your changes — READMEs, architecture
docs, config examples, and contributing guides as appropriate.

## Verification

See [VERIFY.md](VERIFY.md) for the quality gate. All project checks must
pass before pushing.

## Pull Request

Write the PR body to a temp file to avoid shell-escaping issues.

```bash
git fetch origin main
git rebase origin/main
git push -u origin HEAD
gh pr create --title "<type>: <description>" --body-file /tmp/pr_body_<N>.md
```

PR body should include: `Closes #<N>`, overview, changes, and testing status.

**Bundle PR**: One commit per issue (`Ref #<N>`), single worktree, PR body
lists all `Closes #<N>`. See `AGENTS.md` for eligibility criteria.

Do **not** merge. Notify the approver that the PR is ready.

## Cleanup (On Request)

When instructed after the PR is merged:

```bash
git worktree remove .agent-worktrees/<type>-issue-<N>-<desc>
git branch -d <type>/issue-<N>-<desc>
```

Pattern B: wait for Lead instruction before removing anything.

## Team Operation Flow

```
1. Lead: create team → create tasks (per issue) → spawn issue-slayer agents
2. Each agent: claim → plan → Lead approval → implement → verify → PR
3. Lead: coordinate merge order → rebase if needed → shut down → delete team
```
