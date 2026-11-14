# Design: an AI teammate that grows

## Relationship

The AI is a co-worker, not a tool and not a subordinate. It has memory, opinions,
and the duty to say "I don't know" when it doesn't. The human supplies context,
corrections, approval, and priorities. Both review outcomes and improve the
process.

## Learning layers

| Layer | File | What it stores |
|---|---|---|
| Facts | `memory/projects/<PROJECT>/<program>.md` | environment, business rules, code map |
| Decisions | project card / `DECISIONS.md` | why a choice was made |
| Inbox | `memory/corrections.md` | incidents not yet consolidated (≤7 days) |
| **Knowledge** | `memory/knowledge/<domain>.md` | **the rule, its mechanism and its symptom** |
| **Expertise & competency** | `memory/expertise.md` | the end state, the three levels, the per-domain levels, the probes |
| Patterns | `memory/skill-candidates.md` | repeated work that may become a skill |
| Preferences | `memory/user-profile.md` | language, style, risk rules |
| Tool behavior | `memory/tool-map.md` | authoritative tool per task |
| Outcomes | evidence logs / comparison | what worked, what did not |

## Context tiers

Memory is read at every session start, so its cost is paid on every task. The
digest (`scripts/session_context.py`) prints what must be known *before* choosing a
tier; everything else is read only when that tier calls for it.

| Tier | When | Read | Cost |
|---|---|---|---|
| `light` | a question, an analysis, a review | the digest | ~0.6k tokens |
| `task` | code, file, or SAP work | + the project card + that project's knowledge domains | ~2.5k |
| `deep` | new project, incident, design | + every memory file | ~10k |

Three rules keep the cost flat as the memory grows: one fact lives in exactly one
file; an incident is **consolidated** into an existing entry (or dropped) instead of
appended; and a project declares its domains, so a task loads only the knowledge it
touches. The inbox is archived monthly. See `docs/memory-model.md`.

The digest still surfaces the **open inbox rows** on every session, so a correction
is not repeated while it waits for consolidation.

## Program spec

Granularity is the **program**, not the project. The FS is signed for a program, the
code changes are in a program, and the test evidence is per program. A project keeps
`README.md` + `project.yaml`; a project-wide `spec.md` is allowed only when the
project itself is the deliverable (a cross-program initiative).

Five files, five questions - no duplication:

| File | Question | Owner |
|---|---|---|
| `spec.md` | What must be true, and how do we know it is done | requirement |
| `CHANGELOG.md` | What shipped since the last released TR | release |
| `AGENTS.md` | How we work (constraints, deploy, editable objects) | process |
| `reports/DECISIONS.md` | Why a choice was made (with evidence) | history |
| `templates/plan.md` | In what order, for a long run | execution |

`CHANGELOG.md` is one table row per deploy, not a prose log: version, date,
one-line change, verification. It covers the window SAP does not: SAP version
management snapshots a TR only when it is **released**, so until then the system
holds only the current code. When the TR is released, the block collapses to one
line (`TR ... released ... - v1-vN`) and SAP becomes the record; the file never
grows past one transport. The failure mode is real: ZDEMO01 reached v20 while the
card and README still said v12.

`spec.md` is a thin, checkable contract: YAML front matter (`program`,
`spec_version`, `status`, `fs_version`, `fs_file`, `implemented_version`,
`updated`), then REQ / AC / DEV / Q tables. The customer FS moves to
`spec/source/` and is immutable; a new FS is a new file and a new `fs_version`.
Each REQ cites the FS by line, so a reviewer can trace the code back without
re-reading a 1,700-line document.

This is deliberately **not** the Kiro three-file layout (`requirements.md`,
`design.md`, `tasks.md`). Design already lives in `reports/DECISIONS.md` and task
order in `templates/plan.md`; copying them into a spec would double both the
maintenance and the tokens for no new information.

Enforcement:

- Global `AGENTS.md` reads the spec before the first edit; project and program
  `AGENTS.md` put it in the session-start list.
- `templates/spec.md` is the only template an agent needs to start.
- `closeout.py` checks the front matter, that `fs_file` exists, and that the REQ
  and AC tables parse; a program without a spec is a warning (lazy migration), a
  malformed spec is an issue.
- `scripts/specs_sync.py` mirrors every spec and FS into `specs/` with a sha256
  manifest (the program folder is not a git repository). `closeout.py` warns when
  the mirror is stale, so the backup cannot rot silently.
- The session digest prints one line (`SPEC v1.0 · FS V4.0 - 12 req (5 pending-test),
  10 ac, 13 open q`) so the contract is discoverable without loading it.

## When the spec is read (and when it is not)

One read per session per program. The file is ~110 lines / ~9 KB (~2.3k tokens) - cheap
once, wasteful every turn.

| Situation | Read it? | What |
|---|---|---|
| First touch of the program in a session | **yes, once** | the whole `spec.md` |
| The next turn of the same change | no | it is already in context |
| A later session continuing the same change | yes | only the REQ/AC/Q rows you work on |
| A bug that may be a requirement gap | yes | the AC for that behaviour + open Q |
| The spec changed during the session | yes | the changed REQ/AC rows |
| After a context compaction in a long run | yes | only the REQ/AC you are on |
| Before transport or close-out | yes | AC evidence + Q still open |
| Navigation, "where is X", status question | no | the digest `SPEC` line |
| Formatting, typo, no behaviour change | no | - |

The trigger is **behaviour**, not the file: read when you are about to change what
the program does, or to claim a test passed. If the work is "where is this / what is
the status", the digest already answers it.

Why not a skill or a subagent:

| Mechanism | Cost | Why it is the wrong/right tool |
|---|---|---|
| `AGENTS.md` line (used) | ~1 line, always present | the guardrail must fire even when the agent does not think to load a skill |
| Skill | description always, body on demand | skills are opt-in by description match; a "read the spec" skill is a one-line procedure |
| Subagent | a whole session | delegation is for parallel work, not for reading 9 KB |

If spec **authoring** later grows into a real procedure (ambiguity review, FS
line mapping, approval gates), it becomes a personal skill (`spec-author`), not a
change to a vendor skill. The template already covers the writing itself.

## Prompt budget (measured)

Every session pays for what the harness injects before any work starts. Measured
on 2026-11-13:

| Block | Measured | Budget | Enforced by |
|---|---|---|---|
| Skill catalog (descriptions) | **19.8k chars / 31 entries** | 20k | `registry_check.py` |
| Tool descriptions | 16.1k chars / 111 tools | 28k | `registry_check.py` |
| `AGENTS.md` chain (5 files loaded in ZDEMO01) | **15.1k chars** (global 5.2k, workspace 4.2k, ZDEMO01 3.2k, DEMO 1.2k, SAP Projects 1.3k) | — | one canonical copy per rule |
| Session digest | 2.6k chars (2.6k brief, 0.8k `--tiny`) | 3k | `session_context.py` |
| Task tier add-on | card 8.7k + 2 domain files 4.9k = 13.7k | 9k card | `memory_check.py` |
| Inbox row | ≤240 chars | 240 | `memory_check.py` |
| Knowledge entry | ≤1.2k chars, ≤12 per domain | per domain | `memory_check.py` |

Measured 2026-11-14, in three steps:

| Change | Tools | Skills | Fixed prompt |
|---|---|---|---|
| baseline | 211 / 31.5k | 78 / 41.7k | 73.3k |
| SAP/GUI/docs/Playwright on-demand, `rosa` removed | 111 / 16.1k | 78 / 41.7k | 57.9k |
| 29 Basis/DB skills parked | 111 / 16.1k | 49 / 25.8k | 41.9k |
| 18 duplicates and unused families parked | 111 / 16.1k | **31 / 19.8k** | **36.0k** |

Both catalogs are now inside budget. The only remaining warnings are four vendor
descriptions over the 1,000-char per-skill budget, which cannot be shortened without
forking the vendor file — leave them.

## No-guess protocol

- Unknown -> say unknown and propose a read-only check.
- Hypothesis -> label it and state how to falsify it.
- Every claim needs evidence: `file:line`, command output, DDIC read, test result.
- Never invent field names, table structures, tool output, or test results.
- If a tool or session is unavailable, report it; do not substitute silently.

## Advice protocol

- **When:** risk, a better alternative, conflicting evidence, scope creep, or a
  repeated mistake.
- **Shape:** observation -> evidence -> options -> recommendation.
- **Not:** nagging, overriding the human, or silently changing scope.
- **Record:** advice + decision + outcome in the project card or decisions log.

Disagree once with evidence; after the human decides, execute and record the risk.

## Team model

- **Lead (main agent):** plan, decompose, delegate, verify, own the final answer,
  write memory.
- **Specialists (subagents):** ABAP, runtime, RAP, integration, HANA, architecture,
  exploration, general verification.
- **Skills:** playbooks the team uses.
- **Memory:** the team wiki; the lead writes it, subagents return findings.

Delegation rules and routing live in `memory/team-roster.md`.

## Boundaries

- The AI may advise but does not decide irreversible actions.
- The AI may delegate but remains accountable for the final answer.
- Subagents never edit vendor agents/skills or write SAP without approval.
- No credentials in prompts, memory, or commits.
