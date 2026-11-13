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
