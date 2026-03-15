---
name: quality-finisher
description: >
  Audits open PRs for test coverage gaps after issue-slayer opens them.
  Writes missing tests and pushes to the PR branch, posts structured coverage
  comments, or confirms coverage is sufficient. Use when asked to check test
  coverage, or "are there enough tests?". Run after PRs
  are opened and before verify-sprint. NOT for implementing features (use
  issue-slayer) or reviewing code correctness (use a code review tool).
---

# Quality Finisher

Post-PR test coverage audit. Confirm the kill is real before verify-sprint merges it.

## Inputs

One or more PR numbers provided by the user.

## Workflow

For each PR:

1. Read the PR diff (`gh pr diff <N>`)
2. Identify changed source files and their existing test coverage
3. Diagnose coverage gaps
4. Apply the [Decision Matrix](#decision-matrix)
5. **Always** post a `## Quality Finisher Report` comment (all outcomes)
6. Report outcome to user

## Decision Matrix

| Situation | Action |
|---|---|
| Writable tests exist | Checkout PR branch in a worktree, implement tests, push, then post report |
| Tests not writable yet (missing infra, etc.) | Post structured comment — gap, blocker, unblock path |
| Coverage already sufficient | Post short confirmation comment, done |
| Blocker requires a source-level change | Open a new `agent:proposed` issue, post link on PR |

> **Every outcome requires a `## Quality Finisher Report` PR comment.**
> `verify-sprint` uses this comment as the signal that auditing is complete.

## Writing Tests

When tests are writable, check out the PR branch in an isolated worktree.
Use a distinct local branch name (`qf/pr-<N>`) so the temporary checkout is
never confused with the actual PR branch:

```bash
git fetch origin
git worktree add -B "qf/pr-<N>" .agent-worktrees/quality-finisher-pr-<N> "origin/<branch-name>"
```

Write tests following the project's existing test conventions.

**Before committing**, run the project's test suite to confirm the new tests
pass. Refer to the project's `CLAUDE.md`, `CONTRIBUTING.md`, or CI
configuration for the exact test command. If the new tests fail, fix them
before proceeding — do not push failing tests.

Commit and push with the co-authorship trailer format defined in `AGENTS.md`.

**If `git push` fails** (e.g., branch protection, diverged history):

1. Try `git fetch origin <branch-name> && git rebase origin/<branch-name>` then push again.
2. If push still fails due to branch protection, post a report comment
   explaining the blocker and ask the user to push manually or adjust
   branch protection settings.
3. Do NOT force-push unless the user explicitly instructs you to.

Remove the worktree after pushing:

```bash
git worktree remove .agent-worktrees/quality-finisher-pr-<N>
git branch -D "qf/pr-<N>"
```

Then post a report comment.

## Report Comment Templates

Write all report comments to a temp file first, then post via
`gh pr comment <N> --body-file`.

### Tests Pushed

```markdown
## Quality Finisher Report

**Status**: Tests pushed

**Added**: <N> test cases covering <what was covered>
```

### Tests Not Writable

```markdown
## Quality Finisher Report

**Status**: Coverage gap — tests not yet writable

**Gap**: <what is not covered>

**Blocker**: <reason — e.g., requires a test harness that does not exist yet>

**Unblock path**: <what needs to happen first>

**Recommended next step**: <specific action>
```

### Coverage Sufficient

```markdown
## Quality Finisher Report

**Status**: Coverage sufficient — no additional tests needed.
```

### Prerequisite Required

```markdown
## Quality Finisher Report

**Status**: Prerequisite required

A source-level change is needed before tests can be written for this PR.
New issue opened: #<new-issue-number>
```

## Opening a Prerequisite Issue

When a source-level change is required before tests can be written,
open a new issue with the `agent:proposed` label. Do not add `agent:ready`.

## Summary Report

After all PRs are processed, output a summary to the user:

```
Quality Finisher — Summary
PR #A: tests pushed (N new test cases)
PR #B: comment posted (gap: X, blocker: Y)
PR #C: coverage sufficient
```
