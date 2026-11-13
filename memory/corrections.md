# Corrections

> One row per correction; what "right" looked like. Fix level, strongest first:
> architecture -> type/check -> lint/CI -> test -> memory/AGENTS -> skill.

| Date | AI did | Correct behavior | Root cause | Fix level | Evidence | Status |
|---|---|---|---|---|---|---|
| 2026-11-13 | Called `sap_press_key` | Tool is `sap_send_key` | wrong tool name | tool-map | tool error message | closed |
| 2026-11-13 | Opened SE16N | SE16N is policy-blocked; use SE16 | missing policy fact | tool-map | session error | closed |
| 2026-11-13 | Used a PowerShell dump as the Thai source | Use ADT `get_source`; the dump mangles Thai | encoding | memory rule | Thai character count | closed |
| 2026-11-13 | Assumed local v5 was the live source | Re-read the live source before patching | stale local copy | working method | live diff found `kosta` | closed |
| 2026-11-13 | Preload stored `LIPS-VBELN/POSNR` but read it with the SO key | Store `VGBEL/VGPOS` and `VBELN AS VBELN_VL` | key shape confusion | code + memory | v8 fix; line 5290 | closed |
| 2026-11-13 | Typed `CHG_DELQY` | `CHG_DELQTY` | typo | syntax gate | syntax finding | closed |
| 2026-11-13 | Blamed only the missing main-item control row | Two causes: preload key and BAPI create return | partial root cause | memory + code | LIPS/VBFA, debug data | closed |
| 2026-11-13 | Pressed a custom button while SAP GUI was unfocused | Bring the session forward or ask the user | GUI focus | tool-map | windows-mcp USER_CONTROL | closed |
| 2026-11-13 | Kept `MKPF` + `MSEG` in a new S/4 method | Read `MATDOC` once | legacy table | code + memory | MATDOC DDIC; v10 | closed |
| 2026-11-13 | Pressed F5 in SICF with no node selected | Select the parent node first; expect "Create/Change a Service" | F5 needs a selection | memory/AGENTS + skill `sap-sicf-service-create` | popup title | closed |
| 2026-11-13 | Used the SICF F9 wizard | Use F5 on the selected node | wrong tool | tool-map + skill | unreadable HTML popup | closed |
| 2026-11-13 | Claimed the node was absent because a filter popup was empty | Verify with `ICFSERVICE` and HTTP 401/404 | concluded from a popup | memory rule | node existed | closed |
| 2026-11-13 | Counted open qty as picked LIPS (`KOSTA = C`) plus non-PGI ZMMT014 (`KOSTK <> C`) | Use `SUM(LIPS-LFIMG)` per SO item over all deliveries; the split main item is 0, so no main/sub case | qty tied to picking status and two overlapping sources | code + memory | LIPS 0+50+10, KOSTA A: picked 0, ZMMT014 60; KOSTK B counts twice | open |
| 2026-11-13 | Emitted one editable GR row per ZMMT010 record next to each DO row | One row per DO item, editable rows only for the open remainder per batch | two loops for one quantity; `MENGE_PD` drops only at Post Goods Issue | code | ZMMT010 50+20 and ZMMT014 50+10 = 4 rows | open |
| 2026-11-13 | Trusted ZMMT014 as the delivery source of truth | Read deliveries from LIPS/LIKP; ZMMT014 is display metadata | the mirror is not always written | code + memory | DO 1041100095 has LIPS but no ZMMT014 -> open qty 60 instead of 30 | open |
