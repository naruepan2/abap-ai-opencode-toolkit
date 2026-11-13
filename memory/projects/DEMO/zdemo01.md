# ZDEMO01

> Last updated: 2026-11-13 (OpenCode session, v11 built). Re-verify live state
> before changing anything.

## Resume card

- **Status:** v11 is **deployed and active** in client 100 (syntax check 0
  findings). The runtime test in client 900 is pending; do not claim it passed
  until LIPS and ZMMT014 are read back.
- **Next step:** in client 900 run Option 8 for SO `1011099686` item `10` and
  confirm the ALV offers **30 KG** (not 60), shows the two `1041100095` lines,
  and that pressing Create DO creates a **second** DO for 30 (the existing split
  DO must not block it).
- **Do not:** edit SAP standard objects, vendor agents/skills, or claim a test
  passed without reading LIPS / ZMMT014 back.

## Goal

FS Option 8 — create a Delivery Order at the external storage location, split it
by batch, then Post Goods Issue (PGI), and keep the history in `ZMMT014` /
`ZMMT015`.

## Constraints

- Only `ZDEMO01_MODL` and `ZDEMO01_MSG` may change.
- Do not modify SAP standard code.
- Target transport: `DS4K904935` (task `DS4K904936`).
- Client 100 = ADT/code; client 900 = SAP GUI/business data.
- Picking status: `LIKP-KOSTK` (header) and `LIPS-KOSTA` (item), not `VBUP`.
  Picking status is display information and must not drive the open quantity.

## Environment

| Item | Value |
|---|---|
| System | DS4 (DEMO DEV) |
| Code client | 100 (ADT) |
| Test client | 900 (SAP GUI) |
| ADT destination | `ds4-100` (client-bound) |
| Table display in 900 | `SE16`; `SE16N` is policy-blocked |
| Source dump | ADT `get_source` (UTF-8); CLI dump mangles Thai |

## Business rules

- Option 8 creates one DO per shipping point.
- Batch-split sub items are `9xxxxx`; the main item keeps `UECHA = '000000'` and
  its `LFIMG` becomes 0, so summing all `LIPS` items of a delivery is correct.
- `ZMMT014-UECHA` carries the parent: a sub item row points to its main item.
- Re-run guard: if `LIPS-UECHA <> '000000'`, the DO is already split → msg 041.
- Picking auto-update: `WS_DELIVERY_UPDATE_2` with `UPDATE_PICKING = 'X'` and
  `VBPK_TAB` (`PIKMG` = `LIPS-LFIMG`); re-read twice; still incomplete → msg 032.
- PGI write-back: `ZMMT010-MENGE_PD -= MSEG-MENGE`, `MENGE_GI += MSEG-MENGE` for
  `BWART = '601'`; `MSEG-VBELN_IM` = DO; convert units with
  `MD_CONVERT_MATERIAL_UNIT`; clamp at 0; failure → msg 033.
- Open quantity (v11): `KWMENG - SUM(LIPS-LFIMG)` over every delivery; the batch
  availability is `ZMMT010-MENGE_PD - SUM(non-PGI delivery items of that batch)`.
- Quantity checks (v11): GR pending qty, then `KWMENG`, then the live LIPS open
  quantity. The old `remain_kwmeng <> 0` bypass is gone — 0 blocks.
- Partial delivery (v11): only an **unsplit** DO of exactly the requested qty is
  reused; a DO that is already split never blocks a new DO.
- Limit: a failed split whose DO already covers the whole order qty leaves no
  editable row, so the retry must be done in VL02N.
- History: one `ZMMT014` row per batch-split sub item; `PGI_FLAG = 'X'` after
  PGI; `ZMMT015` one row per 601 material document.

## Code map

- `create_delivery_document` — DO creation, batch split, `ZMMT014`
  (`_save_history('D')`), live quantity re-check
- `post_goods_issue_from_do` — Post Goods Issue, picking update, `ZMMT010`,
  `ZMMT014`/`ZMMT015` (`_save_history('P')`)
- `_select_option8` — commitment from `LIPS`/`LIKP`, editable rows for the open
  remainder only, `ZMMT014` history rows plus `LIPS`-only rows (`hist_flag`)
- `_save_history` — shared persistence for `ZMMT014` and `ZMMT015`; reads
  `MATDOC` (header + item fields) and fills `ZMMT014-UECHA` from `LIPS-UECHA`
- Messages: `ZDEMO01_MSG` has 39 entries. 040 = existing DO, not split; 041 = DO
  + split done, press Post Goods Issue; 042 = ZMMT014 write failed; 043 = ZMMT015
  write failed; 044 = BAPI created more than one DO; 045 = DO created but number
  not found.

## Decisions

- Dump fix: pass `lt_return TYPE bapirettab` and
  `lt_docu_batch TYPE /spe/docubatch_dlv_item_tty` explicitly to
  `BAPI_OUTB_DELIVERY_CHANGE`.
- `hist_flag` separates read-only history rows from actionable rows.
- `ZMMT015` is also written by `ZMMFM_POST_DELV_TO_ZMMT010` on VL09/VL02N,
  keyed by the 602/653/655 document; the 601 rows here do not collide.
- v7: existing-DO detection falls back to a direct `SELECT SINGLE` from LIPS;
  `BAPI_OUTB_DELIVERY_CREATE_SLS` imports `NUM_DELIVERIES`; if `DELIVERY` is
  empty after commit, the DO is recovered from LIPS; the batch-split BAPI gets a
  main-item control row with `CHG_DELQTY = 'X'`.
- v8: `lt_so_lips_pre` stores the SO key (`VGBEL/VGPOS`) plus the DO number
  (`VBELN AS VBELN_VL`). Before this, the READ compared a DO number with an SO
  number and always missed.
- v9: `ZMMT014-UECHA` is read from `LIPS-UECHA` in both `_save_history` modes.
  Messages 033 and 041 now use the full “Post Goods Issue”.
- v10: `_save_history` reads `MATDOC` only. `MATDOC` carries the header fields
  (`BUDAT`, `CPUDT`, `CPUTM`, `USNAM`, `BKTXT`) and the item fields, so the
  `MKPF` read is removed.
- v11: open quantity comes from `LIPS` + `LIKP`, not from `ZMMT014`. Editable
  rows exist only for the open remainder per batch; history of a deleted
  delivery is skipped; DO items missing from `ZMMT014` are shown from `LIPS`.
  A DO that is already split no longer blocks a new DO (partial delivery); only
  an unsplit DO holding exactly the requested qty is reused. Editable rows now
  carry `VBELN_VA`/`POSNR_VA` (the `MMT010` substructure has no SO key).
  Approved scope extension to `_select_option8` (recorded in `DECISIONS.md`).
- v12: new ALV column `OPEN_SO_QTY` ("Open Sales Order Qty") between TF DEMO Qty
  and Ex.WH.Stck. Value = `KWMENG - SUM(LIPS-LFIMG)` per SO item, on editable
  rows only, no total. Header set in `ZDEMO01_VIEW` (user approved touching it).

## Known unknowns (do not guess)

1. Should `ZMMT014` also store the main item row?
2. Is `ISSNO` ever populated in Option 8?
3. Should `PGI_FLAG` reset on VL09 reversal?
4. Is `MENGE_GI` in base UoM or sales UoM?
5. Is the `ZMMT010-MENGE_PD` clamp at 0 acceptable?
6. Why does DO `1041100095` have no `ZMMT014` row — created outside ZDEMO01, or
   was the history write skipped?
7. FS gaps: `ZMMT014` mapping is empty; `ZMMT013` has no definition; `BUDAT` is
   declared twice; ใบเบิก `MENGE_TF_P` is never populated by Option 8.

## Latest debugging findings (client 900, 13.11.2026)

- DO `1041100092` (60 KG, sub items `900001 = 50` batch `0105240100` and
  `900002 = 10` batch `1012240100`) was **deleted** from `LIKP`; its two
  `ZMMT014` rows (created 19:23:45) remain. `UECHA` is blank in those rows
  because they predate the v9 code.
- DO `1041100095` (30 KG, sub items `900001 = 15` batch `1012240100` and
  `900002 = 15` batch `0105240100`) exists, `KOSTK = A`, `WBSTK = A`, and has
  **no** `ZMMT014` row.
- `ZMMT010`: `4900000646` MENGE_PD 50 (batch `0105240100`), `4900000647`
  MENGE_PD 20 (batch `1012240100`). MENGE_PD drops only at Post Goods Issue.
- `VBAP` SO `1011099686`/`10`: `KWMENG = 60` KG, `VRKME = MEINS = KG`, `LFSTA = B`.
- `SE16` filter `LIPS-UECHA = '000000'` returns exactly the main item, so the
  main-item lookup is correct; an empty ALV cell is only the ALPHA display.
- General process rules from this session — the BAPI count, `CHG_DELQTY`, and the
  GUI focus caveat — live in `memory/lessons.md`, not here.

## Evidence

- Deployed source: `patched_MODL_v10.abap`, 272,187 bytes,
  md5 `41380b876a114c6a71668282112211a3`; syntax check 0 findings; active.
- Built source: `patched_MODL_v11.abap`, 279,549 bytes,
  md5 `1e2b6437c3888368c68f97742525c124` (builder `build_v11.py`, 31 exact-match
  edits); `patched_VIEW.abap`, 56,968 bytes,
  md5 `86a9307dfa7979c0b2bd530f51e3bcfc` (builder `build_view.py`, fetches the live
  VIEW so the `i_soft_refresh` argument is kept).
- Deployed: `write-source include ZDEMO01_VIEW` (55,537 bytes) and
  `ZDEMO01_MODL` (272,384 bytes) into task `DS4K904936` of request `DS4K904935`;
  `syntax-check program ZDEMO01` -> 0 findings; `activate program ZDEMO01` ->
  success; both includes re-read identical to local (MODL 7,166 lines
  `c3f3a8b9940d30e6ffcd110c9d3c46bb`, VIEW 1,431 lines
  `4d3228443dd6db8484825161f409c494`).
- `memory_check.py` reports 0 issues, 0 warnings.

## Files

- Working directory: `<portfolio>\SAP Projects\Projects\DEMO\ZDEMO01`
- Current source: `patched_MODL_v11.abap`
- Builder: `build_v11.py`
- Decisions log: `reports/DECISIONS.md`
