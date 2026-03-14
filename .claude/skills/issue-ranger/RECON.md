# Reconnaissance Guide

Scout each perspective in priority order. Stop when you have enough candidates
(typically 10–15).

**When referencing code**: use file path + function/struct name, not line
numbers. Line numbers drift between the time you scout and the time a Slayer
picks up the issue.

Adapt the specifics of each perspective to the project's language, framework,
and domain. The categories below are universal; the examples are starting points.

## Priority 1 — Robustness & Error Handling

- Unhandled errors in production paths (panics, unchecked nulls, bare exceptions)
- Edge cases: empty inputs, corrupt data, unexpectedly large inputs
- Resource cleanup on exit or failure (handles, connections, temp files)

## Priority 2 — Code Quality & Architecture

- Dead code, unused imports, unnecessary copies or allocations
- Functions that are too long or have too many responsibilities
- Stringly-typed values that should be enums or typed constants
- Module boundaries that could be cleaner

## Priority 3 — Performance

- Unnecessary allocations in hot paths
- I/O or computation that blocks the main thread unnecessarily
- Caching opportunities for expensive operations
- Resources kept alive longer than needed

## Priority 4 — User Experience

- Missing controls or shortcuts that comparable tools provide
- Insufficient feedback for loading, error, or empty states
- Behavioral quirks (window management, responsiveness, accessibility)

## Priority 5 — Cross-Platform & Compatibility

- Platform-specific assumptions that break on other OSes
- Hardware compatibility gaps (older devices, varied configurations)
- Path handling edge cases (Unicode, long paths, symlinks)

## Priority 6 — Documentation Freshness

Compare documentation against the actual source code:

- Features in code but missing from docs
- Modules or APIs added or renamed but not reflected in docs
- Stale descriptions that no longer match current behavior

File one documentation issue per coherent batch of drift — not one per line.

## Priority 7 — New Features (Small Scope Only)

Scope limit: achievable by modifying a small number of files, no new subsystem
required. If larger, break into sub-issues or reject.

- Configuration options users would expect
- Small quality-of-life additions
