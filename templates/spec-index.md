# <PROGRAM> — FS index

Read this file, not `spec/source/<file>`. The FS is the functional's document and is
immutable; this index is our read map — tens of lines instead of thousands.

| | |
|---|---|
| current | `spec/source/<file>` |
| owner | functional — **never edit anything under `spec/source/`** |
| received | YYYY-MM-DD |
| integrity | `spec.md` front matter: `fs_lines` / `fs_bytes` · `closeout.py` checks it |

## Read this much

| Task | Open | Lines | ~tok |
|---|---|---:|---:|
| What it does / is this the right object | *Summary* below | 0 | 0 |
| Object metadata, WRICEF type, T-code | <section> | <a>–<b> | <n> |
| The requirement in the author's words | <section> | <a>–<b> | <n> |
| Authorization objects | <section> | <a>–<b> | <n> |
| Customize table and structure field lists | <section> | <a>–<b> | <n> |
| Selection screen / input parameters | <section> | <a>–<b> | <n> |
| Output screen per option | <section> | <a>–<b> | <n> |
| Field-level output mapping | <section> | <a>–<b> | <n> |
| Core processing rules | <section> | <a>–<b> | <n> |
| Printed form layout | <section> | <a>–<b> | <n> |
| Test scenarios | <section> | <a>–<b> | <n> |
| **Never read by default** | cover, approval block, change control, TOC | 1–<n> | <n> |

Rule: start at *Summary*. Open **one** mapped slice only when the task touches it. Never
read the whole file. If `closeout.py` reports a fingerprint change, the functional sent a
new revision — **rebuild this map before using any line range**; no script can do that.

## Summary (written by us, from the FS — ≤10 lines)

- **Purpose** —
- **Entry point** —
- **Flow** —
- **Data** —
- **Output** —
- **Must not** —

## Open questions and contradictions

Keep them in `spec.md` Q rows and `reports/DECISIONS.md`. Never edit the FS to fix them.
