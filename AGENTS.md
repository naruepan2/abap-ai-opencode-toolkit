# Workspace rules

This repository is the portable memory and registry workspace for the OpenCode
side of the AI teammate.

- Read `memory/user-profile.md`, `memory/lessons.md`, `memory/corrections.md`,
  `memory/tool-map.md`, and the active `memory/projects/<name>.md` at session
  start. The corrections ledger is read on purpose: a lesson that is written but
  never read is not learning.
- Log a correction in `memory/corrections.md` the moment it happens. At task
  close-out, promote anything durable to `memory/lessons.md`. A rule that must
  bind the next session goes into the `AGENTS.md` of the level where the mistake
  happened; a skill is for a repeating multi-step procedure, not a one-line rule.
- Do not edit vendor agents or skills. Only `*-by-pongg` files and newly created
  personal skills may be edited, and only after approval.
- Keep Copilot and OpenCode separate: this repository is the OpenCode side.
- Never commit credentials or customer data.
- Prefer evidence over guesses: if something is unknown, say so and propose a
  read-only check.
- At session start, run `python scripts/registry_check.py --check --brief` and
  show the summary only when it reports actionable issues.
- Then run `python scripts/memory_check.py --brief`. It validates the memory
  tables, row evidence, status values, and that no credential was recorded.
