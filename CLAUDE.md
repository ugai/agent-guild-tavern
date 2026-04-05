# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Agent Guild Tavern is a **Claude Code plugin** (`guild-tavern`) that provides a multi-agent workflow for autonomous software development. It coordinates specialized AI agents to scout issues, plan sprints, implement fixes, and deliver pull requests through GitHub Issues and git worktrees.

This is a documentation/skill plugin — there is no build system, package manager, or compiled code. The codebase consists entirely of Markdown skill definitions, agent configurations, and a JSON eval suite.

## Running Evals

```bash
claude evals run evals/evals.json
```

Eval prompts with `<ISSUE_N>` or `<PR_N>` placeholders require a seeded test repository. All `pattern` fields use regex syntax.

## Architecture

### Plugin Structure

```
.claude-plugin/                          Marketplace manifest (marketplace.json)
plugins/guild-tavern/                    Installable plugin content
  .claude-plugin/                        Plugin manifest (plugin.json)
  agents/                                Agent role definitions (frontmatter + instructions)
  skills/                                Skill implementations (primary source of truth)
AGENTS.md                                Workflow protocol, label rules, PR conventions
```

### Source of Truth Hierarchy

**SKILL.md** files inside each `plugins/guild-tavern/skills/<name>/` directory are the authoritative source for agent behavior. Agent files (`plugins/guild-tavern/agents/*.md`) are summaries that point back to SKILL.md. When editing behavior, always modify SKILL.md first.

### Skills and Their Roles

| Skill | Role | Key Constraint |
|---|---|---|
| `issue-ranger` | Scout codebase, post `agent:proposed` issues | Never commits code or adds `agent:ready` |
| `issue-slayer` | Implement one issue in a worktree, open PR | Requires `agent:ready` label; isolates in `.agent-worktrees/` |
| `issue-raid-commander` | Analyze ready queue for merge conflicts | Read-only; never spawns agents or writes code |
| `quality-finisher` | Audit PRs for test coverage gaps | Posts comments or pushes test commits |
| `verify-sprint` | Batch-verify and squash-merge sprint PRs | Never pushes verify branch to remote |
| `dispatching-guild-expedition` | Orchestrate full pipeline (Rangers→Commander→Slayers) | Spawns parallel agents in team mode |

### Skill File Conventions

Each skill directory contains:
- `SKILL.md` — Full workflow steps, constraints, output format (authoritative)
- `ENV.md` — Tool name mappings and environment-specific notes
- Optional: `TEMPLATE.md`, `RECON.md`, `APPROVAL.md`, `WORKTREE.md`, `VERIFY.md`

### Two Execution Patterns

- **Pattern A (Standalone)**: User invokes skill directly, approves plan via chat
- **Pattern B (Team Mode)**: Lead spawns multiple agents, approves via `SendMessage`

### Label Protocol

- `agent:proposed` — AI-created issue, awaiting human review
- `agent:ready` — Human-approved for autonomous implementation
- Eligibility: must have `agent:ready` + Open + Unassigned + no `pending` label

### Workflow Pipeline

```
issue-ranger → (human approval) → issue-raid-commander → issue-slayer × N → quality-finisher → verify-sprint
```

`dispatching-guild-expedition` automates the full pipeline except `verify-sprint`.

## Editing Guidelines

- When modifying a skill's behavior, edit `plugins/guild-tavern/skills/<name>/SKILL.md` — it is the source of truth
- Keep agent files (`plugins/guild-tavern/agents/*.md`) as lightweight summaries pointing to SKILL.md
- Shared cross-skill documentation lives in `snippets/`
- AGENTS.md governs workflow protocol, label rules, and PR conventions — changes there affect all skills
- Eval assertions in `evals/evals.json` must stay in sync with skill behavior changes
