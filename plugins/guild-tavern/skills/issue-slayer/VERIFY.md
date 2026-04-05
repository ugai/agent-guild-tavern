# Verification Quality Gate

Before pushing, run the project's full quality gate. Read the project's
`CLAUDE.md`, `CONTRIBUTING.md`, or CI configuration to determine the exact
commands. Typical checks include:

- **Formatting** — auto-formatter check
- **Linting** — static analysis with warnings-as-errors
- **Tests** — full test suite
- **Build** — production/release build

All checks must pass before pushing. On failure, fix the issue and re-run.

## Manual testing

After all automated checks pass, output the command the user should run for
manual/visual testing, based on the project's conventions.
