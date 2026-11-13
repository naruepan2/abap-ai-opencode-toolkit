# Corrections

> One row per correction. This is how the AI learns what "right" looks like.
> Fix level, strongest first: architecture -> type/check -> lint/CI -> test ->
> memory/AGENTS -> skill.

| Date | AI did | Correct behavior | Root cause | Fix level | Evidence | Status |
|---|---|---|---|---|---|---|
| 2026-11-13 | Called `sap_press_key` | `sap_send_key` is the real tool name | wrong tool name | tool-map | tool error message | closed |
| 2026-11-13 | Tried SE16N for table data | Use SE16; SE16N is policy-blocked | missing policy fact | tool-map | session error | closed |
| 2026-11-13 | Used a PowerShell CLI dump as the Thai source | Use ADT `get_source` as the base; CLI dump mangles Thai | encoding | memory rule | Thai character count | closed |
| 2026-11-13 | Assumed local v5 was the live source | Re-read the live source before patching | stale local copy | working method | live diff found `kosta` change | closed |
