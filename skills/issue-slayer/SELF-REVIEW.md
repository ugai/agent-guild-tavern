# Self-Review

Review your own changes before opening a PR. This step catches logical errors,
missed requirements, and design issues that linters and tests do not detect.

## When to Run

After [VERIFY.md](VERIFY.md) checks pass, before the Pull Request step.

## Review Criteria

Discover review criteria in this order:

1. **Project docs** — look for `REVIEW.md`, review sections in
   `CONTRIBUTING.md`, or `.github/PULL_REQUEST_TEMPLATE.md` checklists
2. **Issue requirements** — re-read the issue to confirm all acceptance
   criteria are met
3. **General** — if no project-specific criteria exist, review for:
   correctness, edge cases, security (OWASP top 10), naming clarity,
   unnecessary complexity

## Procedure

1. Generate the full diff: `git diff origin/main...HEAD`
2. If a sub-agent is available, spawn one with the diff and review criteria.
   Otherwise, review the diff yourself — re-read it as if seeing it for the
   first time
3. List findings with severity (`error` / `warning` / `info`)
4. If `error` or `warning` findings exist — fix them, re-run verification,
   then review again
5. Repeat up to **3 iterations**. If issues remain after 3 rounds, report
   them to the user (Pattern A) or Team Lead (Pattern B) and ask whether to
   proceed

`info` findings are suggestions — note them but do not block on them.

## Completion

When the review is clean (no `error` or `warning` findings), proceed to the
Pull Request step.
