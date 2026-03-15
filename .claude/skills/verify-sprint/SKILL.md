---
name: verify-sprint
description: >
  Batch-verifies multiple sprint PR branches by merging them into a local
  ephemeral verify branch, running a build check and user verification, then
  squash-merging each PR into main. The verify branch is never pushed to
  remote. Use after a sprint to merge multiple PRs together. NOT for
  single-PR merges or test coverage audits (use quality-finisher for that).
---

# Verify Sprint

## Workflow checklist

Copy and track progress:

```
- [ ] Step 1: Identify PR branches
- [ ] Step 2: Fetch and create verify branch
- [ ] Step 3: Merge all PR branches
- [ ] Step 4: Build check
- [ ] Step 5: Visual verification (user)
- [ ] Step 6: Merge PRs into main
- [ ] Step 7: Discard verify branch
```

## Step 1 — Identify PR Branches

If the user hasn't provided PR numbers, list open PRs:

```bash
gh pr list --state open --json number,title,headRefName
```

Confirm with the user which PRs to include.

**Quality check:** For each PR, verify that `quality-finisher` has already been run by checking for a `## Quality Finisher Report` comment:

```bash
gh pr view <N> --json comments --jq '.comments[].body | select(startswith("## Quality Finisher Report"))'
```

If no such comment exists, warn the user before proceeding.

## Step 2 — Fetch and Create Verify Branch

**NEVER push this branch to remote** — it is a throwaway integration test.
Pushing it would trigger CI, confuse collaborators, and leave stale branches.

```bash
git fetch origin
git checkout -b verify/sprint-$(date +%Y-%m-%d) origin/main
```

If the branch name already exists, append `-2`, `-3`, etc.

## Step 3 — Merge All PR Branches

```bash
git merge origin/<branch-1> origin/<branch-2> origin/<branch-3> ...
```

If the octopus merge fails due to conflicts, fall back to sequential merges.
Report any conflicts to the user before proceeding.

## Step 4 — Build Check

After a successful merge, run a build to catch compile errors before
asking the user for a visual check. Use the project's standard build command.

If the build fails, identify the responsible PR branch, fix it there, re-merge,
and re-run the build check.

## Step 5 — Visual Verification

Tell the user to run the project's standard run command for manual testing.

Ask: *"Visual check complete — did everything look correct? (yes / issue found)"*

**If an issue is found:**

1. Identify the PR branch responsible.
2. User or agent adds fix commits to that branch.
3. Re-merge and re-check.

Repeat until the user confirms no issues.

## Step 6 — Merge PRs into Main

```bash
gh pr merge <N> --squash --delete-branch
```

Use the Raid Commander's recommended order if available; otherwise merge fixes
before features that depend on them.

## Step 7 — Discard Verify Branch

```bash
git checkout main
git branch -D verify/sprint-<date>
git pull origin main
```
