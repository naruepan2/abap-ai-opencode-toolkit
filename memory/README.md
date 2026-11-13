# Memory system (A-scope)

> What this is: a small, durable memory that makes the AI know Pongg and the
> project without re-explaining every session. It does **not** edit any vendor
> agent or skill.

## Read at session start — one call, then pick a tier

```powershell
python scripts\session_context.py            # digest, ~1.8k chars
python scripts\session_context.py --full     # digest + file map + raw checks
python scripts\session_context.py --project DEMO/ZDEMO01
```

The digest prints: the active project's resume card (status / next step / do not),
memory and registry health in one line each, the always-on style and evidence rules
from `user-profile.md`, the **open corrections**, the curated tool rules, and the
size of every file that can be opened on demand.

| Tier | When | Read |
|---|---|---|
| `light` | a question, an analysis, a review | the digest only |
| `task` | any code, file, or SAP work | digest + the active project card |
| `deep` | new project, incident, design | digest + every file below |

Files on demand (the digest says when they matter):

1. `user-profile.md` — how Pongg communicates and decides
2. `lessons.md` — durable lessons (already promoted; do not repeat them)
3. `corrections.md` — every correction, its root cause, and its fix level
4. `tool-map.md` — which MCP/tool owns which job
5. `team-roster.md` — who to delegate to, and when not to
6. `skill-candidates.md`, `agent-registry.md` — patterns and ownership

The digest always shows the **open** corrections, because a lesson that is written
but never read is not learning. Reading the closed rows is a `deep` activity.

Two files carry a `<!-- digest:start -->` … `<!-- digest:end -->` block:
`user-profile.md` (style and evidence rules, true for every session) and
`tool-map.md` (tool traps, true for every project). Edit that block, not the digest
script, when a rule must appear on every session — and keep it to a few one-liners.

## Write immediately (do not wait for close-out)

- **A user correction** → one row in `corrections.md`, status `open`. One line per
  column: what the AI did, the correct behavior, the root cause, the fix level, the
  evidence. **≤240 chars for the whole row** — `memory_check.py` warns above that.
  This is the one write that must happen mid-task, because a session can end
  mid-task.
- A decision that cannot be cheaply reversed → project `memory/decisions.md` or
  `reports/DECISIONS.md`

## Write at task close-out

- A durable lesson → `lessons.md`, in **one** row (≤240 chars), then set the source
  correction's status to `promoted` and point `evidence` at the lesson. Do not
  restate the same fact in both files: the promotion replaces the open row, it does
  not copy it.
- Update the active project's resume card (status / next step / do not).
- A repeated pattern → `skill-candidates.md` (rule of 2).
- A non-obvious tool choice → a row in `tool-map.md`; add it to the `digest` block
  only if it is easy to get wrong and true for every project.
- A rule that must bind the next session → the `AGENTS.md` of the level where the
  mistake happened (program → project → workspace). A skill is for a multi-step
  procedure, not for a one-line rule.

Close-out is one edit per file, batched. Do not re-read a file you just wrote; the
`memory_check` run is the verification.

## Promotion ladder

```
memory rule → AGENTS.md line → personal agent prompt → skill → script/check
```

Rule of 2: a lesson becomes a skill candidate only after the same correction
appears twice (or once if the risk is high).

## Size discipline

The memory is read at every session start, so its size is the price of every
future task.

- One fact lives in exactly one file; other files point at it.
- One row ≤240 chars. If it needs more, the detail goes to the project card and the
  row keeps the pointer.
- A closed or promoted row older than 30 days moves to
  `memory/_archive/<file>-YYYY-MM.md` (git keeps the history). Keep the last 30
  days plus everything still `open`.
- If `memory/*.md` passes ~8k chars, archive before adding.
- `scripts/memory_check.py` fails on a broken table, a missing evidence cell, a
  credential-like string, and an unknown status value — run it after a close-out,
  not at session start.

## Ownership

- `*-by-pongg` agents: editable with approval
- vendor agents/skills: read-only
- new personal skills: allowed, but test on a real task before promoting

## Registry check

The workspace scanner lives in `scripts/registry_check.py`. It writes
`memory/reports/registry-report.md` and never changes the system.

- `--check --brief` at session start (already inside `session_context.py`)
- `--check` when you want the full report
- `--refresh` only when new skills, agents, or MCP servers are installed

An **issue** means something is broken now (missing path, duplicate name, agent
pointing at a missing skill, missing tool/server, zero tools on a server that is
not optional). A **warning** is a human decision or a designed state: a newly
installed asset, a stale validation date, an over-budget description, or an
on-demand SAP server that is idle. Warnings do not fail the gate; do not spend a
turn explaining them.

## Where project memory lives

For a real project, create `memory/projects/<PROJECT>/<program>.md` from
`memory/projects/README.md`. The card is the resume point: status, next step, do
not, business rules, code map, decisions, known unknowns, evidence.
