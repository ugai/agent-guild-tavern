---
name: issue-raid-commander
description: >
  Analyzes agent:ready issues for merge conflicts and outputs a sprint plan.
  Read-only assessment — does NOT spawn agents, write code, or pick up issues.
  Use before spawning multiple issue-slayer agents to check for conflicts
  or plan a sprint. NOT for single-issue work. NOT for full pipeline
  orchestration (use dispatching-guild-expedition).
---

# Issue Raid Commander

Battlefield awareness without intervention. Assess the ready queue, detect
collisions, and hand the team lead a plan they can execute immediately.

## Inputs

```bash
gh issue list --label "agent:ready" \
  --search "no:assignee state:open -label:pending" \
  --json number,title,labels,body --limit 50
```

Also read the project's `CLAUDE.md` to identify conflict-prone
files.

If the query returns **zero issues**, output a one-line summary
("No `agent:ready` issues in the queue.") and stop — there is nothing to
analyze.

## Analysis

For each issue, estimate which files it will touch. Use:

- The issue body (issue-ranger usually notes affected files)
- The issue title and labels as hints
- Your own knowledge of the codebase

Flag any two issues that are likely to touch the same file. Issues touching
conflict-prone files warrant extra scrutiny.

If you are genuinely uncertain whether two issues conflict, treat them as
conflicting and say so.

## Output

Output a structured sprint plan with these sections:

```
## Sprint Plan

**Conflicts**: <none | list of conflict pairs with files and suggested order>
**Merge order**: <ordered list, or "any order" if no conflicts>
**Bundle candidates**: <none | groups with pattern and file list>
**Ready to dispatch**: <issue numbers in recommended execution order>
```

Prefer brevity. Omit empty sections. A single sentence is fine when nothing
conflicts.

### Bundle PR candidates

Flag groups of issues as `bundleable` when they meet the criteria in
`../reading-guild-rules/SKILL.md` (same pattern, small, no file conflicts, reviewable as one unit).
Example output:

```
Bundle candidate: #178, #180, #182, #183
  Pattern: unwrap → error propagation
  Files: handler.rs, config.rs, middleware.rs, utils.rs (no overlap)
  → Assign to a single Slayer
```

The Slayer will create one commit per issue and a single PR.

## Feedback

When running standalone (not called by `dispatching-guild-expedition`),
present the sprint plan to the user and wait for confirmation before
concluding — the plan is a recommendation, not a final decision. When called
as a sub-step of the expedition pipeline, the caller handles user approval.
