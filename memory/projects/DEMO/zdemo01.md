# ZDEMO01

domains: [sap-abap, sap-data]

> Last updated: 2026-11-14 (OpenCode session, v23 built). Re-verify live state
> before changing anything.

## Resume card

- **Status:** v23 is **Deployed and active** in client 100 (syntax check 0
  findings). The runtime test in client 900 is pending; do not claim it passed
  until LIPS and ZMMT014 are read back.
- **FS:** V4.0 `spec\source\FS_ZDEMO01_V4.0_20261018.md`; contract `spec.md` v1.3 (13 REQ/12 AC/13 Q).
- **Deploy is pre-approved end-to-end** (user, 2026-11-14): write both includes into
  `DS4K904935`, syntax-check, and activate immediately at 0 findings — no further
  approval; stop only on a finding. Procedure: `AGENTS.md` §Deploy.
- **Next step:** in client 900 run Option 8 for SO `1011099686` item `10` and
  confirm the ALV offers **30 KG** (not 60), shows the two `1041100095` lines,
  and that pressing Create DO creates a **second** DO for 30 (the existing split
  DO must not block it).
- **Do not:** edit SAP standard objects, vendor agents/skills, or claim a test
  passed without reading LIPS / ZMMT014 back.
- **Change type:** build → extension (v7–v20 are scope extensions of the same FS,
  each recorded in `reports/DECISIONS.md`).
- **Production:** unknown — ask (DS4 is DEV; no production system or sync check is
  recorded). Compare the dev source with production before the first transport.
- **Target:** DS4, client 100 (ADT) + client 900 (test); transport `DS4K904935`.

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
- v7-v10: DO recovery from LIPS when the BAPI returns no `DELIVERY`, the
  `CHG_DELQTY` control row, SO key in `lt_so_lips_pre`, `ZMMT014-UECHA` from
  `LIPS-UECHA`, `_save_history` reads `MATDOC` only. Detail in
  `reports/DECISIONS.md`.
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
- v14: posted DOs (`PGI_FLAG = 'X'` / `WBSTK = 'C'`) no longer listed; `create_issue_no` p_rad8 branch runs after Create DO + Batch Split so ZMMT014 gets ISSNO. Base `base_v13.abap`.
- v21/v22: after DO + batch split the row is read-only (`VBELN_VA`/`POSNR_VA`/`MENGE_PD`); PGI refused (023) without `VBELN_VL` + `POSNR_VL`.
- v23: Option 8 column order = client-900 capture.
- v15-v20: one `WS_DELIVERY_UPDATE_2` for pick + PGI (`wabuc` + `update_picking` + VBPOK with `UMVKZ`/`UMVKN`, `VBELN`/`POSNN` = `LIPS-VGBEL/VGPOS`); 601 from `MATDOC`; unassigned-field-symbol `CLEAR` removed (dump); types renamed `matdoc`.
- v13.1: `menge_pd` is `TYPE lips-lfimg` (MENG13, no sign), so the ALV cannot take a minus; message 046 unused.
- v13: hid `MENGE_GR`/`MENGE_PD_INITIAL`/`MENGE_INITIAL` in Option 8 (whitelist);
  editable rows leave Sales Doc/Item empty for the user to type; ticking the
  select checkbox no longer clears the status message.

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

## Latest findings (details in `reports/DECISIONS.md`)

- DO `1041100095` (30 KG, split 15+15) has no `ZMMT014` row; its remark comes
  from the `ZMMT010` fallback. `1041100092` was deleted, its rows remain.
- SO `1011099686`/10: `KWMENG 60`, `LFSTA = B`; `ZMMT010` MENGE_PD 50 / 20,
  dropping only at Post Goods Issue.

## Evidence

- Built source: `patched_MODL_v11.abap`, 279,566 bytes,
  md5 `01f1456d2c7d7abc916afd5cb099a72f` (builder `build_v11.py`, 33 exact-match
  edits); `patched_VIEW.abap`, 57,337 bytes,
  md5 `3a7cf40f9b7b3006ff2313058db4948c` (builder `build_view.py`, idempotent).
- Deployed AND ACTIVE (verified via `?version=active`): MODL 7,167 lines
  `8bc4f86c838bb2265d7071f1115c7dc6`, VIEW 1,438 lines
  `54881ab7077a313b476a564fb6aeb0f1`; `syntax-check` 0 findings.
- Runtime check (client 900, SO `1011099686`/10): `MENGE_TF | OPEN_SO_QTY |
  MENGE_PD`, `30.000` on the editable row and `0.000` on the DO lines; editable
  row has blank Sales Doc/Item (user types them); DO lines keep message 041 after
  `SELC` is ticked.
- Activation trap: `activate program` alone left the includes inactive;
  `activate include ZDEMO01_MODL` and `ZDEMO01_VIEW` are required. `get-include`
  returns the inactive source, so verification must use `?version=active`.
- `memory_check.py` reports 0 issues, 0 warnings.

## Files

- Working directory: `<portfolio>\SAP Projects\Projects\DEMO\ZDEMO01`
- Current source: `patched_MODL_v11.abap`
- Builder: `build_v11.py`
- Decisions log: `reports/DECISIONS.md`
