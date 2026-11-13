# Workspace rules

This repository is the portable memory and registry workspace for the OpenCode
side of the AI teammate.

- **Session start is one call.** Run `python scripts/session_context.py` and pick a
  tier: `light` (question/analysis → digest only), `task` (code, file, or SAP work
  → digest + the active project card), `deep` (new project, incident, design →
  digest + every memory file). The digest already shows the open corrections,
  because the corrections ledger is read on purpose: a lesson that is written but
  never read is not learning. Details and the write rules live in
  `memory/README.md`; do not re-read a file the digest shows is not needed.
- The digest runs the registry and memory checks. If it reports an **issue**, show
  the short summary and propose a fix. Warnings (a new asset, a stale date, an idle
  on-demand server) need a human decision, not a turn.
- Log a correction in `memory/corrections.md` the moment it happens, one line, status
  `open`. At task close-out, promote anything durable to `memory/lessons.md`, set the
  source row to `promoted`, and update the project resume card — one edit per file,
  batched, no re-read. A rule that must bind the next session goes into the
  `AGENTS.md` of the level where the mistake happened; a skill is for a repeating
  multi-step procedure, not a one-line rule.
- Do not edit vendor agents or skills. Only `*-by-pongg` files and newly created
  personal skills may be edited, and only after approval.
- Keep Copilot and OpenCode separate: this repository is the OpenCode side.
- Never commit credentials or customer data.
- Prefer evidence over guesses: if something is unknown, say so and propose a
  read-only check.
- Before a significant write or a transport, run
  `python scripts/registry_check.py --check` for the full report; `--refresh` only
  after installing a new skill, agent, or MCP server.
