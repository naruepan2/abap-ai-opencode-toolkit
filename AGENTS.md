# Workspace rules

This repository is the portable memory and registry workspace for the OpenCode
side of the AI teammate.

## Before creating or changing a program — the change contract

Ask these four questions and **wait for the answers** before the first edit. They are
cheap now and expensive later.

| Question | Why it changes the direction |
|---|---|
| **Is there a functional spec? Where?** | The FS is the requirement. No FS → say so and propose a one-page FS (goal, inputs/outputs, rules, edge cases) for approval. Never invent the requirement. |
| **Bug fix, feature extension, or change request?** | Bug fix → reproduce with evidence, smallest patch, no refactor. Extension → design the delta, keep existing behaviour and objects compatible. CR → impact analysis over every consumer, then the transport order. |
| **Is it live on production? Is the dev object in sync?** | Live → the dev source must be compared with the production version first; plan regression and the transport path; never test on production. Diverged → stop and report. |
| **Target: system, client, transport?** | A write without a target is not a change, it is an accident. |

Record the four answers in the project resume card (`FS`, `Change type`, `Production`,
`Target`). If any answer is unknown, that is the first task — not the code.

## Working rules

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
- **Long runs get a plan.** For a task with more than a few steps, copy
  `templates/plan.md` to the program folder as `plan-<task>.md` and get the plan
  approved once. It carries the goal, the acceptance test (= stop condition), the four
  contract answers, the approved scope, and ≤12 verifiable todos. The card points at it
  (`Plan:`). Pre-arming there is what lets a long run proceed without stopping at
  every write.
- **Checkpoint every todo.** Tick it with one line of evidence and update the card's
  Status / Next step. The plan file plus the digest is the resume point after a
  context reset.
- **A blocked step is a stop, not a retry.** Record `BLOCKED: <question>` in the plan,
  report once, and wait; never loop a gate.
- **Stop when** the acceptance test passes, two consecutive attempts fail, or the next
  step leaves the approved scope.
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
