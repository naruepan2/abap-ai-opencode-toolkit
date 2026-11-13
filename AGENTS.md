# Workspace rules

This repository is the portable memory and registry workspace for the OpenCode
side of the AI teammate.

- **Session start is one call.** Run `python scripts/session_context.py` and pick a
  tier: `light` (question/analysis → digest only), `task` (code, file, or SAP work
  → digest + the project card + the project's knowledge domains), `deep` (new
  project, incident, design → digest + every memory file). Details and the write
  rules live in `memory/README.md`; do not re-read a file the digest shows is not
  needed.
- The digest runs the registry and memory checks. If it reports an **issue**, show
  the short summary and propose a fix. Warnings (a new asset, a stale date, an idle
  on-demand server, a domain at its cap) need a human decision, not a turn.
- **During work:** log an incident in `memory/corrections.md` (the inbox), one row of
  at most 240 characters, status `open`, the moment it happens.
- **At close-out, consolidate — one outcome per open row:** merge it into
  `memory/knowledge/<domain>.md` (`Seen +1`), add a new entry, promote it to an
  `AGENTS.md` line or a skill, or drop it as a one-off. Set the row `drained`, then
  update the project resume card. One batched edit per file, no re-read.
- Do not create a new log: the knowledge base grows by **editing** entries, not by
  appending rows. A rule that repeats belongs in a check, not in prose.
- Do not edit vendor agents or skills. Only `*-by-pongg` files and newly created
  personal skills may be edited, and only after approval.
- Keep Copilot and OpenCode separate: this repository is the OpenCode side.
- Never commit credentials or customer data.
- Prefer evidence over guesses: if something is unknown, say so and propose a
  read-only check.
- Before a significant write or a transport, run
  `python scripts/registry_check.py --check` for the full report; `--refresh` only
  after installing a new skill, agent, or MCP server.
