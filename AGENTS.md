# Workspace rules

This repository is the portable memory and registry workspace for the OpenCode
side of the AI teammate.

- Read `memory/user-profile.md`, `memory/lessons.md`, `memory/tool-map.md`, and
  the active `memory/projects/<name>.md` at session start.
- Update `memory/lessons.md` at task close-out. Log corrections in
  `memory/corrections.md`.
- Do not edit vendor agents or skills. Only `*-by-pongg` files and newly created
  personal skills may be edited, and only after approval.
- Keep Copilot and OpenCode separate: this repository is the OpenCode side.
- Never commit credentials or customer data.
- Prefer evidence over guesses: if something is unknown, say so and propose a
  read-only check.
- At session start, run `python scripts/registry_check.py --check --brief` and
  show the summary only when it reports actionable issues.
