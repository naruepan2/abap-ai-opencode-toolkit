# Corrections

> **Archived 2026-11-14** when the memory model changed (`docs/memory-model.md`).
> The rule behind each row now lives in `memory/knowledge/<domain>.md`. The rows
> still marked `open` at archive time (open quantity, GR row, `ZMMT014` authority,
> `mmt010~*` substructure) were implemented in ZDEMO01 v11/v12 and are recorded in
> the project card. This file is history, not input.

> One row per correction, ≤240 chars: the rule, not the story. Detail belongs in
> the project card (`memory/projects/<PROJECT>/<program>.md`). Fix level, strongest
> first: architecture -> type/check -> lint/CI -> test -> memory/AGENTS -> skill.
> Status: `open` (still true) -> `closed` | `promoted` (now a lesson) | `wontfix`.

| Date | AI did | Correct behavior | Root cause | Fix level | Evidence | Status |
|---|---|---|---|---|---|---|
| 2026-11-13 | Called `sap_press_key` | Use `sap_send_key` | wrong tool name | tool-map | tool error | closed |
| 2026-11-13 | Opened SE16N | Use SE16; SE16N is policy-blocked | missing policy fact | tool-map | session error | closed |
| 2026-11-13 | Took a PowerShell dump as the Thai source | Use ADT `get_source`; the dump mangles Thai | encoding | memory rule | Thai char count | closed |
| 2026-11-13 | Assumed the local v5 file was live | Re-read the live source before patching | stale local copy | working method | live diff found `kosta` | closed |
| 2026-11-13 | Stored `LIPS-VBELN/POSNR`, read with the SO key | Store `VGBEL/VGPOS` + `VBELN AS VBELN_VL` | key shape confusion | code | v8 fix, line 5290 | closed |
| 2026-11-13 | Typed `CHG_DELQY` | `CHG_DELQTY` | typo | syntax gate | syntax finding | closed |
| 2026-11-13 | Blamed the missing main-item row only | Two causes: preload key + BAPI create return | partial root cause | memory + code | card §Latest findings | closed |
| 2026-11-13 | Pressed a custom button on an unfocused GUI | Focus the session first, or ask the user | GUI focus | tool-map | windows-mcp | closed |
| 2026-11-13 | Kept `MKPF` + `MSEG` in a new S/4 method | Read `MATDOC` once | legacy table | code | MATDOC DDIC, v10 | closed |
| 2026-11-13 | Pressed F5 in SICF with no node selected | Select the parent node first, then F5 | F5 needs a selection | memory/AGENTS | popup title | closed |
| 2026-11-13 | Used the SICF F9 wizard | Use F5 on the selected node | wrong tool | tool-map | unreadable HTML popup | closed |
| 2026-11-13 | Called the node absent from an empty filter popup | Verify via `ICFSERVICE` + HTTP 401/404 | concluded from a popup | memory rule | node existed | closed |
| 2026-11-13 | Counted open qty as picked LIPS + non-PGI ZMMT014 | `SUM(LIPS-LFIMG)` per SO item over all deliveries; the split main item is 0 | two overlapping sources | code | card §Latest findings | open |
| 2026-11-13 | Emitted one editable GR row per ZMMT010 record | One row per DO item; editable only for the open remainder per batch | two loops for one qty | code | card §Latest findings | open |
| 2026-11-13 | Trusted ZMMT014 as the delivery source of truth | Read deliveries from LIPS/LIKP; ZMMT014 is display metadata | the mirror is not always written | code | DO 1041100095 | open |
| 2026-11-13 | SORTed `lt_so_zmmt010` by flat `mblnr mjahr zeile` | `mmt010~*` is a substructure: use `mmt010-mblnr` and so on | wrong structure level | syntax gate | syntax line 1450 | open |
| 2026-11-13 | Wrote memory rows as prose | One terse row under the budget; move detail to the card | no length rule | check | this row, `memory_check` | closed |
| 2026-11-13 | Built editable rows from `ls_so_zmmt010-mmt010` only | Set `VBELN_VA`/`POSNR_VA` explicitly; the substructure carries no SO key | copied only the GR structure | code + test | ALV editable row had blank Sales Doc | open |
| 2026-11-14 | Left REMARK blank on LIPS-derived DO rows | Fall back to ZMMT010 by batch when no ZMMT014 row | row had no DEMO source | code | 1041100095 blank vs ZMMT010 `PONG1 Remark` | open |
| 2026-11-14 | Asked for approval after a clean syntax check | Activate immediately when 0 findings; stop only on a finding | deploy treated as two approvals | memory/AGENTS | user instruction | open |
| 2026-11-14 | Trusted `get-include` + `activate program` alone | Compare `?version=active`; activate each include, then the program | CLI returns the inactive source | memory/AGENTS | report ran old code until includes were active | open |
