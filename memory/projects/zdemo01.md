# ZDEMO01

> Last updated: 2026-11-13 (session with OpenCode). Re-verify live state before
> changing anything.

## Resume card

- **Status:** v6 deployed and active; runtime test pending because SAP GUI was
  disconnected.
- **Next step:** log on to SAP GUI client 900, then run T1–T5 (below).
- **Do not:** edit SAP standard objects, vendor agents/skills, or claim a test
  passed without running it.

## Goal

FS Option 8 — create a Delivery Order at the external storage location, split it
by batch, then post goods issue (PGI), and keep the history in `ZMMT014` /
`ZMMT015`.

## Constraints

- Only `ZDEMO01_MODL` and `ZDEMO01_MSG` may change.
- Do not modify SAP standard code.
- Target transport: `DS4K904935` (task `DS4K904936`).
- Client 100 = ADT/code; client 900 = SAP GUI/business data.
- Picking status: `LIKP-KOSTK` (header) and `LIPS-KOSTA` (item), not `VBUP`.

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
- Batch split sub items are `9xxxxx`; the main item keeps `UECHA = '000000'`.
- Re-run guard: if `LIPS-UECHA <> '000000'`, the DO is already split → msg 041.
- Picking auto-update: `WS_DELIVERY_UPDATE_2` with `UPDATE_PICKING = 'X'` and
  `VBPOK_TAB` (`PIKMG` = `LIPS-LFIMG`); re-read twice; still incomplete → msg 032.
- PGI write-back: `ZMMT010-MENGE_PD -= MSEG-MENGE`, `MENGE_GI += MSEG-MENGE` for
  `BWART = '601'`; `MSEG-VBELN_IM` = DO; convert units with
  `MD_CONVERT_MATERIAL_UNIT`; clamp at 0; failure → msg 033.
- Quantity checks: `KWMENG` first, then `remain_kwmeng` (guard `<> 0`).
- History: one `ZMMT014` row per batch-split sub item; `PGI_FLAG = 'X'` after
  PGI; `ZMMT015` one row per 601 material document.

## Code map

- `create_delivery_document` — DO creation, batch split, `ZMMT014` (`_save_history('D')`)
- `post_goods_issue_from_do` — PGI, picking update, `ZMMT010`, `ZMMT014`/`ZMMT015`
  (`_save_history('P')`)
- `_select_option8` — live data + `ZMMT014` history rows (`hist_flag`)
- `_save_history` — shared persistence for `ZMMT014` and `ZMMT015`
- Messages: `ZDEMO01_MSG` has 37 entries; 040 = existing DO, 041 = DO + split done,
  042 = ZMMT014 write failed, 043 = ZMMT015 write failed.

## Decisions

- Dump fix: pass `lt_return TYPE bapirettab` and
  `lt_docu_batch TYPE /spe/docubatch_dlv_item_tty` explicitly to
  `BAPI_OUTB_DELIVERY_CHANGE`.
- `hist_flag` separates read-only history rows from actionable rows; a new DO can
  be created for the remaining quantity.
- `remain_kwmeng` also subtracts open DO quantity from `ZMMT014`
  (`PGI_FLAG <> 'X'` and `LIKP-KOSTK <> 'C'`).
- `ZMMT015` is also written by `ZMMFM_POST_DELV_TO_ZMMT010` on VL09/VL02N,
  keyed by the 602/653/655 document; the 601 rows here do not collide.

## Known unknowns (do not guess)

1. Should `ZMMT014` also store the main item row?
2. Is `ISSNO` ever populated in Option 8?
3. Should `PGI_FLAG` reset on VL09 reversal?
4. Is `MENGE_GI` in base UoM or sales UoM?
5. Is the `ZMMT010-MENGE_PD` clamp at 0 acceptable?
6. FS gaps: `ZMMT014` mapping is empty; `ZMMT013` has no definition; `BUDAT` is
   declared twice; ใบเบิก `MENGE_TF_P` is never populated by Option 8.

## Evidence

- Deployed source: `patched_MODL_v6.abap`, 270,193 bytes,
  md5 `142254bc0cb1056463bf3936acba7fa5`.
- `syntax-check program ZDEMO01` → 0 findings; activate → OK; no inactive objects.
- Deployed source has 1,986 Thai characters (encoding intact).
- Client 900 at last check: `LIKP`/`LIPS` empty; `ZMMT015` has one VL09/602 row.
- Pending tests T1–T5:
  1. Create DO 30 (2 batches) → `ZMMT014` 2 rows, `PGI_FLAG` blank.
  2. Create DO again → live rows only; remaining quantity creatable.
  3. PGI → `ZMMT014.PGI_FLAG = 'X'` + 601 doc; `ZMMT015` `TCODE = ZDEMO01`.
  4. Re-enter → history green (031) + remaining live rows.
  5. PGI again → 031, no second material document, no duplicate `ZMMT015`.

## Files

- Working directory: `<home>\AppData\Local\Temp\opencode\zmme011`
- Deployed source: `patched_MODL_v6.abap`
- Builder: `build_v6.py`
- Decisions log: `reports/DECISIONS.md`
