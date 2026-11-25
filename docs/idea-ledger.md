# Idea ledger — navigation index only

> One line per thing the user proposed, decided, declined or left open. This file is an
> INDEX, not a second decision log and not a second rulebook: the decision lives in
> `docs/memory-decisions.md`, the work in `CHANGELOG.md` + git, the analysis in
> `workspace/memory/reports/`, raw concepts in `workspace/memory/scratch/`. Point at
> those homes; never duplicate their text here. A row is edited in place, never appended
> as a per-check timeline. Git history is the timeline.

## Secretary rules

- User says `note: <text>` → write one row immediately with status `open`; answer after.
- User says `recall <topic>` → search the four homes above and summarize with `file:line`
  or commit hash; never answer from this index alone.
- User says `what's pending` → list every `open` row and what is waiting on a decision.
- When the user chooses or declines an option, mark that row `done`/`declined` in the
  SAME commit as the change; never leave a stale `open`.
- Never surface an old proposal as new without citing its D-row or ledger row.
- Never copy a rejected idea forward without its reason and its own revisit trigger.
- No new always-loaded bytes: this file is on-demand (`docs/`, not in `FILES_ON_DEMAND`).

## Commands the user can type

| Type | Assistant does |
|---|---|
| `note: <text>` | append one row, status `open` |
| `recall <topic>` | search `memory-decisions.md`, `CHANGELOG.md`, `reports/`, `scratch/` and summarize with evidence |
| `what's pending` | list all `open` rows + the decision each one waits on |

## Rows

| Date | Proposed / discussed | Status | Home / evidence | Next |
|---|---|---|---|---|
| 2026-11-25 | Source-intake methodology P0 (provenance catalogue + scratch + intake flow) | done | `a9e6445`, `docs/source-catalogue.md`, `docs/catalog.md` §Source intake | P1 — first real source version bump |
| 2026-11-25 | Create a `source-intake` research skill | declined | chat decision; rule diet D-27, skills already 23.5k/20k | none |
| 2026-11-25 | SQLite embedded memory layer (V9.4) | deferred | `docs/memory-decisions.md` D-29; report `v94-memory-design-20261123.md` | revisit only on the D-29 numeric triggers |
| 2026-11-23 | Write-mode `direct | comment-proposal` field | done | `c262d93`, `templates/plan.md`, both `*-by-pongg` agents | none; Copilot-side divergence noted in D-30 |
| 2026-11-25 | `humanizer` / `thai-humanizer` technique | cited, not adopted | `docs/memory-decisions.md` D-31 | if wanted, one host-neutral profile line with a byte reading |
| 2026-11-25 | Assistant acts as personal secretary / thinking partner (this file + 3 commands) | done | this file, `templates/profile.md` | use `note:` / `recall` / `what's pending` |
| 2026-11-25 | Release after source-intake P0 | open | HEAD `a9e6445`; last tag `v0.8.6` | user decision: tag `v0.8.7` or keep committing |
