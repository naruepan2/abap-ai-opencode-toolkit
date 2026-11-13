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
| 2026-11-13 | Preload stored `LIPS-VBELN/POSNR` (DO) but read it with the SO key | Store `VGBEL/VGPOS` plus `VBELN AS VBELN_VL`; read by the SO key | key naming/shape confusion | code + memory rule | debug at line 5290; v8 fix | closed |
| 2026-11-13 | Added `CHG_DELQY` | `CHG_DELQTY` is the real component | field-name typo | syntax check gate | syntax check finding | closed |
| 2026-11-13 | Thought the missing main-item control row alone caused the empty `LV_DELIVERY` | Two separate causes: preload key mismatch and BAPI create return | partial root cause | memory + code | LIPS/VBFA and debug data | closed |
| 2026-11-13 | Tried to press a custom toolbar button while the SAP GUI window was unfocused | Bring the session to the foreground or ask the user to press it | SAP GUI focus requirement | tool-map | windows-mcp USER_CONTROL | closed |
