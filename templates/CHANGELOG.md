# <PROGRAM> - changelog

One row per deploy, newest first. This covers the window SAP does not: SAP
version management snapshots a TR only when it is **released**, so until then the
system holds only the current code. Keep every row for the life of the program —
do not collapse rows at release. Stamp the TR the change actually used. Detail
and evidence stay in `reports/DECISIONS.md`.

| Ver | Date | TR | Scope | What changed | Verified |
|---|---|---|---|---|---|
| v20 | YYYY-MM-DD | DEVK900123 | CL: ZMMM010 | <one line, past tense> | syntax 0 |
| v19 | YYYY-MM-DD | DEVK900124 | RAP: ZI_A → ZI_B → ZC_X, ZB_A, ZCL_A | <one line> | 900 OK |

Rules:

- **One row per deploy.** Keep all rows until the program is unregistered. SAP
  versions remain the authority for exact code diffs; this table is the local
  index of what changed and which TR carried it, so a person or an agent does not
  have to open every SAP version to find a change.
- **TR column.** Record the number SAP actually used. If a write auto-reused the
  object's lock correction number, read it back and record that value — never
  guess. Use `none` or `$TMP` when no transport is involved. If it cannot be
  determined, write `unknown` and put the reason in `reports/DECISIONS.md`.
- **Scope column.** Prefix `CL:` for classic objects, `RAP:` for a RAP stack.
  List only the objects that row touched — a chain (`ZI_A → ZI_B → ZC_X`) is fine,
  full source is not. One TR may contain both kinds during a migration; keep them
  in this one table, distinguished by the prefix.
- `Verified`: `900 OK` (runtime seen in client 900), `syntax 0` (activated, not
  exercised), `pending`.
- Newest row first; the first row must match the spec `implemented_version`.
- **Externally made edit** discovered in SAP: add a **new** row with the TR that
  carried it, `Scope` = only the affected objects, `What changed` = `external edit
  detected; reconciled`, `Verified: pending`. Never rewrite or delete an earlier
  row. See `docs/catalog.md` §"Co-edit contract".
- **At TR release, do not remove rows.** Delete the `.baseline` copy; if the
  release needs a note, put it in `reports/DECISIONS.md`. If the object is later
  re-bound to a new TR, add a new row with the new TR and leave the old row
  pointing at the released TR.
