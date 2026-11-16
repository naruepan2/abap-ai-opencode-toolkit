# Memory model: from a work log to expertise

> Status: **adopted 2026-11-14** (P0–P3 implemented). This file is the *rationale and
> history*; the operating rules are `memory/README.md`. Do not maintain the same rule
> in both — if they disagree, `memory/README.md` wins.
>
> The v0 ledger (dated `corrections.md` / `lessons.md` tables) is migrated: its rules
> live in `memory/knowledge/`, the old tables are at `memory/_archive/v0-ledger/`, and
> `corrections.md` is now the inbox. P4 (the monthly review) is ongoing.
> Supersedes the "one row per correction / per lesson" model.

## The problem with the current model

Today `corrections.md` and `lessons.md` are **chronological ledgers**: one row per
incident, dated, append-only, with a status (`open` → `closed` → `promoted`).

Measured on 2026-11-14:

| Fact | Number |
|---|---|
| Rows across both files | 32 |
| Distinct rules those rows contain | ~25 |
| Growth driver | number of incidents, not amount of knowledge |
| Rows added per incident | 1, whether the rule is new or not |

That is a log, and a log has three structural faults:

1. **It grows with activity.** More work → more rows → a bigger session-start read,
   forever. The 240-char budget only slows the slope.
2. **Retrieval is chronological, not by competence.** To answer "how do I avoid
   losing a GUI click" you scan 32 rows sorted by date; nothing groups the rule with
   the rest of SAP GUI knowledge.
3. **All knowledge looks equally strong.** A rule seen once and a rule that saved a
   production deploy sit in the same table with the same weight.

## The model: how a junior becomes a senior

A junior keeps notes on what happened. A senior keeps **schemas**: rules,
invariants, decision heuristics, and a short list of their own failure modes. They
forget the incident and keep the lesson — and the lesson is *sharpened by repetition*
instead of being re-written each time.

So the memory should have a **consolidation step**, exactly like human memory:
incident → buffer → (merge | generalise | drop | escalate) → knowledge.

```
task
  │  (during work)
  ├─► INBOX         one line per incident, disposable, never read at start
  │
  │  (close-out: the consolidation gate)
  ├─► KNOWLEDGE     one entry per RULE, edited in place, with a seen-count
  │                 (merge if the rule exists · add if it generalises · drop if not)
  ├─► PLAYBOOK      a multi-step procedure → AGENTS.md line or a skill
  └─► CHECK         something a script can catch → memory_check / registry_check
```

## Task kickoff: the change contract

Before the first edit, four answers — and if one is unknown, resolving it *is* the
first task:

| Question | What it decides |
|---|---|
| Is there a functional spec? Where? | the requirement. No FS → propose a one-page FS, never invent one |
| Bug fix, feature extension, or change request? | bug fix → reproduce + smallest patch; extension → designed delta, backward compatible; CR → impact analysis + transport order |
| Live on production? Dev object in sync? | live → compare dev with production first, plan regression; diverged → stop and report |
| Target: system, client, transport? | where the change lands |

The answers are recorded in the project card (`FS`, `Change type`, `Production`,
`Target`), so the next session inherits the direction instead of re-deciding it. The
rule as a knowledge entry: `memory/knowledge/working-method.md`.

## The four layers

| Layer | Path | Lifetime | Read at | Growth |
|---|---|---|---|---|
| Inbox | `memory/corrections.md` | ≤ 7 days, then archived | count only | bounded 40 rows |
| Knowledge | `memory/knowledge/<domain>.md` | permanent, edited in place | by domain (task tier) | bounded per domain |
| Playbook | `AGENTS.md` levels + skills | permanent | harness / on demand | slow |
| Competency | `memory/expertise.md` §"Competency by domain" | updated monthly | monthly review | fixed size |

`lessons.md` disappears: **an entry in the knowledge base *is* the lesson.** Its
history stays in git and in `memory/_archive/`.

## Knowledge entry schema

One rule per entry. No dates in the body except `last confirmed`, no narrative, no
statuses. Editing an entry is how knowledge strengthens.

```markdown
## Batch split needs the main item in ITEM_CONTROL

- **Rule:** when the main item ships 0, add it to `ITEM_CONTROL` with `CHG_DELQTY = 'X'`
- **Why:** BAPI contract; without the row the split fails
- **Break it, and:** the split returns 0 deliveries after a successful-looking call
- **Seen:** 2 · **Confidence:** high · **Last confirmed:** 2026-11-13
- **Evidence:** project card ZDEMO01 §v8
```

- `Seen` counts confirmations, not mentions. One incident, one count.
- `Confidence` is `low` (once, no verification) / `medium` (reproduced or verified in
  a table) / `high` (verified more than once, or cost a real failure).
- The `Break it, and…` line is what makes the entry usable: it tells the next agent
  what symptom to expect, which is how a senior recognises a familiar failure.

## Domains (organised by competence, not by date)

| File | Holds | Seeded from today's rows |
|---|---|---|
| `knowledge/working-method.md` | evidence, root cause, read-before-write | 5 |
| `knowledge/tooling.md` | ADT vs GUI vs dump, SE16, MCP lifecycle, desktop input | 6 |
| `knowledge/sap-gui.md` | focus, ALV trees, SICF navigation | 4 |
| `knowledge/sap-abap.md` | BAPI contracts, MATDOC, key shapes, structures | 5 |
| `knowledge/sap-data.md` | LIPS/LIKP as truth, open quantity, GR rows, history rows | 4 |

A project card declares which domains it touches (`domains: [sap-abap, sap-data]`), so
a task session loads **only those files** — the read cost stays flat while the base
grows. A declared name that does not resolve is an issue in `memory_check.py`: the
digest would silently fall back to every domain file.

The entry itself carries the scope. A `Rule` that names a custom object is a project
decision in the wrong file, and `memory_check.py` warns on it; the routing table (what
belongs to a project versus what belongs here) is in `memory/knowledge/README.md`.

## Bounded growth (the hard rules)

1. **≤ 12 entries per domain.** At the cap, the entry with the lowest
   `seen × confidence` is merged into a neighbour or archived.
2. **≤ 40 inbox rows.** The inbox is drained at every close-out and archived monthly
   to `memory/_archive/inbox-YYYY-MM.md`.
3. **One rule, one entry.** If the rule exists, edit it and increment `seen`. Never
   add a second entry for the same rule.
4. **An incident with no generalisation is dropped.** "I typed the wrong field name"
   is not knowledge; "field names come from the structure, not from memory" is.
5. **Total knowledge ≤ 5k chars per domain.** Beyond that, archive the low-confidence
   tail.

## What the session sees (prompt cost stays flat)

```
digest (light)     project · status · next · one style rule · inbox count · knowledge count
digest (task)      + the project's domain files (declared on the card, not all)
digest (deep)      + every domain file + the archive index
```

Knowledge therefore costs nothing until a task touches its domain — the opposite of
the current model, where every session pays for every past incident.

## Competency map (how "senior" is visible)

The table lives in `memory/expertise.md` §"Competency by domain" (one fact, one file),
reviewed monthly:

| Domain | Level | Basis | Weak spot to watch |
|---|---|---|---|
| SAP GUI automation | practitioner | 5 entries, 2 rules are reflex | focus-dependent actions |
| ABAP and APIs | practitioner | 6 entries, 2 shipped in code | split/BAPI return handling |
| SAP data semantics | apprentice | 3 entries, all verified in tables | Z-table vs LIPS authority |
| Working method | practitioner | 6 entries, 1 enforced by a check | the contract on an unfamiliar program |

Levels: `aware` (knows the trap) → `apprentice` (has the rule) → `practitioner`
(high confidence, reused) → `expert` (the rule is in AGENTS or a check, so it cannot
be forgotten). Promotion to `expert` means the knowledge left the file and became
enforced behaviour — that is the real senior signal.

## Migration plan

| Phase | Work | Effort | Risk |
|---|---|---|---|
| P0 | This document + `memory/knowledge/README.md` + entry template | 20 min | done |
| P1 | Seed 5 domain files from the 32 rows; dedupe; move the old tables to `memory/_archive/v0-ledger/` | 1-2 h | done |
| P2 | Close-out as the consolidation gate; `memory_check.py` validates schema, caps, inbox | 1 h | done |
| P3 | `session_context.py` selects domain files from the project card (`domains:`) | 30 min | done |
| P4 | Monthly review of the competency table and the probes | 30 min/month | ongoing |

P0–P2 change no SAP work and are fully reversible. P1 is the only content move, and
it is a **reorganisation, not a deletion**.

## Anti-goals

- No dated incident table as the primary store.
- No `open/closed/promoted` lifecycle on knowledge — confidence replaces it.
- No duplicate entry for a rule that already exists.
- No new file per project or per month that is read at session start.
- No "log everything" habit: the inbox is a buffer, not an archive.

## What this buys

- **Flat cost:** session prompt no longer scales with the number of incidents.
- **Compounding knowledge:** repeated incidents make an entry stronger, not longer.
- **Real retrieval:** the rule lives next to the knowledge it belongs to.
- **A visible learning curve:** competency levels move only when knowledge is
  verified and reused — the difference between a log and expertise.
