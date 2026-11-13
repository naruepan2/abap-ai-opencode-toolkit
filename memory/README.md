# Memory system (A-scope)

> What this is: a small, durable memory that makes the AI know Pongg and the project
> without re-explaining every session — and that **gets more expert instead of
> longer**. Design and rationale: `docs/memory-model.md`.

## Read at session start — one call, then pick a tier

```powershell
python scripts\session_context.py            # digest, ~2.4k chars
python scripts\session_context.py --tiny     # light tier, ~0.8k chars
python scripts\session_context.py --full     # + file map + raw checks
python scripts\session_context.py --project DEMO/ZDEMO01
```

The digest prints: the active project's resume card, memory and registry health, the
always-on style rules, the **inbox** (incidents not yet consolidated), the **knowledge
inventory** (entries per domain), the curated tool rules, and the size of every file
that can be opened on demand.

| Tier | When | Read |
|---|---|---|
| `light` | a question, an analysis, a review | the digest only |
| `task` | any code, file, or SAP work | digest + project card + the project's knowledge domains |
| `deep` | new project, incident, design | digest + every memory file |

## The model: incident → knowledge

```
task ─► INBOX (one line per incident, disposable)
          │
          └─ close-out: consolidation gate
                ├─► KNOWLEDGE  merge into the existing rule (Seen +1) or add one
                ├─► PLAYBOOK   multi-step procedure → AGENTS.md line or a skill
                ├─► CHECK      a script can catch it → memory_check / registry_check
                └─► DROP       one-off with no generalisation
```

| Layer | Path | Lifetime | Read at |
|---|---|---|---|
| Inbox | `memory/corrections.md` | ≤7 days, then archived | digest count |
| Knowledge | `memory/knowledge/<domain>.md` | permanent, edited in place | task (by domain) |
| Playbook | `AGENTS.md` levels + skills | permanent | harness / on demand |
| Competency | `memory/competency.md` | monthly | digest |

`lessons.md` no longer exists: **a knowledge entry *is* the lesson.** The old ledger
is kept at `memory/_archive/v0-ledger/` and in git.

## Write during work: the inbox

- One row, **≤240 chars**, status `open`, the moment the user corrects you or a fact
  is discovered the hard way. A session can end mid-task, so this cannot wait.
- One line per column: what the AI did, the correct behavior, the root cause, the fix
  level, the evidence. Detail belongs in the project card.
- The inbox is a buffer. It is not a history and it is not read in full at start.

## Close-out: the consolidation gate

For each open row, pick exactly one:

| Situation | Action |
|---|---|
| The rule already exists in a domain file | **merge**: edit that entry, `Seen +1`, raise confidence if it was verified again; set the row `drained` |
| A new, general rule | **add** an entry (domain under cap); set the row `drained` |
| A one-off ("I typed the wrong name") | **drop**; set the row `drained` |
| A multi-step procedure | promote to a skill or an `AGENTS.md` line, keep a one-line entry |
| A script can catch it | add the check, keep a one-line entry |

Then archive the drained rows when the inbox passes 40 rows or at month end:
`memory/_archive/inbox-YYYY-MM.md`. One batched edit per file; the `memory_check`
run is the verification, so do not re-read what you just wrote.

## Knowledge entry

One rule per entry, no dates in the body except `last confirmed`, no status:

```markdown
## <the rule, imperative>

- **Rule:** what to do, concrete and checkable
- **Why:** the mechanism that makes it true
- **Break it, and:** the symptom the next agent will see
- **Seen:** 2 · **Confidence:** high · **Last confirmed:** 2026-11-13
- **Evidence:** table, tool output, or project card section
```

Confidence: `low` (once, unverified) · `medium` (verified in a table/test/run) ·
`high` (more than once, or it cost a real failure). `Seen` counts confirmations, not
mentions.

## Size discipline

- **≤12 entries per domain.** At the cap, merge the lowest `Seen`/confidence entry
  into a neighbour, or archive it to `memory/_archive/knowledge/`.
- **≤40 inbox rows**, drained at close-out, archived monthly.
- **One fact, one file.** Other files point at it; they never restate it.
- **≤240 chars per inbox row; ≤9k chars per project card; ≤1.2k per knowledge entry.**
- **A rule that repeats belongs in a check**, not in prose.

### The goal is expertise, not notes

`memory/expertise.md` defines the end state: a rule has become expertise when it is
**unprompted, not looked up, and testable**. It tracks three levels — reflex (printed
into every session), enforced (a check fails when it breaks), handbook (only correct
if read) — and lists eight cold probes that prove it. Promote a rule up the ladder
only when getting it wrong is expensive and it recurs; archive an entry once its probe
can no longer fail. Today: 6 reflex, 3 enforced, 15 handbook — the honest gap.

Measured prompt budget (skills, tools, AGENTS, digest, cards): `docs/design.md`
§"Prompt budget".

## Ownership

- `*-by-pongg` agents: editable with approval
- vendor agents/skills: read-only
- new personal skills: allowed, but test on a real task before promoting

## Registry check

`scripts/registry_check.py` writes `memory/reports/registry-report.md` and never
changes the system.

- `--check --brief` at session start (already inside `session_context.py`)
- `--check` for the full report, including the prompt budget
- `--refresh` only after installing a new skill, agent, or MCP server

An **issue** means something is broken now (missing path, duplicate name, agent
pointing at a missing skill, missing tool/server, zero tools on a non-optional
server), or a knowledge entry that breaks its schema. A **warning** is a human
decision or a designed state: new asset, stale date, idle on-demand server, a domain
at its cap. Warnings do not fail the gate.

## Where project memory lives

`memory/projects/<PROJECT>/<program>.md` — the resume card: status, next step, do
not, business rules, code map, decisions, known unknowns, evidence. Template:
`memory/projects/README.md`. A card declares `domains: [...]` so a task session loads
only the knowledge it touches.

A long task also gets a `plan-<task>.md` next to the program (template:
`templates/plan.md`), and the card's `Plan:` line points at it. The plan carries the
acceptance test, the contract, the approved scope and ≤12 todos — that is the
checkpoint a long run resumes from.
