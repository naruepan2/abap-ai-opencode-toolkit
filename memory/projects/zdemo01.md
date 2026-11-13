# ZDEMO01

> Last updated: 2026-11-13 (OpenCode session, v9). Re-verify live state before
> changing anything.

## Resume card

- **Status:** v10 deployed and active. Runtime test is in progress by the user.
  Do not claim the split passed until LIPS and ZMMT014 are read back.
- **Next step:** restart `ZDEMO01`, Option 8, SO `1011099686` item `10`,
  quantities `50 + 10`, then press Create DO and verify:
  - LIPS `1041100092`: main item and sub items
  - ZMMT014: two rows with `UECHA = 000010`
- **Do not:** edit SAP standard objects, vendor agents/skills, or claim a test
  passed without reading the result.

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
- Batch-split sub items are `9xxxxx`; the main item keeps `UECHA = '000000'`.
- `ZMMT014-UECHA` carries the parent: a sub item row points to its main item.
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

- `create_delivery_document` — DO creation, batch split, `ZMMT014`
  (`_save_history('D')`)
- `post_goods_issue_from_do` — Post Goods Issue, picking update, `ZMMT010`,
  `ZMMT014`/`ZMMT015` (`_save_history('P')`)
- `_select_option8` — live data + `ZMMT014` history rows (`hist_flag`)
- `_save_history` — shared persistence for `ZMMT014` and `ZMMT015`; reads
  `MATDOC` (header + item fields) and fills `ZMMT014-UECHA` from `LIPS-UECHA`
- Messages: `ZDEMO01_MSG` has 39 entries. 040 = existing DO; 041 = DO + split
  done, press Post Goods Issue; 042 = ZMMT014 write failed; 043 = ZMMT015 write
  failed; 044 = BAPI created more than one DO; 045 = DO created but number not
  found.

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
- v7: existing-DO detection falls back to a direct `SELECT SINGLE` from LIPS;
  `BAPI_OUTB_DELIVERY_CREATE_SLS` imports `NUM_DELIVERIES`; if `DELIVERY` is
  empty after commit, the DO is recovered from LIPS; the batch-split BAPI gets a
  main-item control row with `CHG_DELQTY = 'X'`.
- v8: `lt_so_lips_pre` now stores the SO key (`VGBEL/VGPOS`) plus the DO number
  (`VBELN AS VBELN_VL`). Before this, the READ compared a DO number with an SO
  number and always missed.
- v9: `ZMMT014-UECHA` is read from `LIPS-UECHA` in both `_save_history` modes.
  Messages 033 and 041 now use the full “Post Goods Issue”.
- v10: `_save_history` reads `MATDOC` only. `MATDOC` carries the header fields
  (`BUDAT`, `CPUDT`, `CPUTM`, `USNAM`, `BKTXT`) and the item fields
  (`VBELN_IM`, `VBELP_IM`, `BWART`, material, plant, sloc, batch, quantity), so
  the `MKPF` read is removed.

## Known unknowns (do not guess)

1. Should `ZMMT014` also store the main item row?
2. Is `ISSNO` ever populated in Option 8?
3. Should `PGI_FLAG` reset on VL09 reversal?
4. Is `MENGE_GI` in base UoM or sales UoM?
5. Is the `ZMMT010-MENGE_PD` clamp at 0 acceptable?
6. FS gaps: `ZMMT014` mapping is empty; `ZMMT013` has no definition; `BUDAT` is
   declared twice; ใบเบิก `MENGE_TF_P` is never populated by Option 8.

## Latest debugging findings

- DO `1041100092` was created on 13.11.2026 at 18:06:31. VBFA has one delivery
  for SO `1011099686` / item `10`.
- LIPS for `1041100092` at that point: only main item `000010`, `LFIMG = 60`,
  `UECHA = 000000`, `KOSTA = A`, `VGBEL = 1011099686`, `VGPOS = 000010`.
  No sub items.
- `lt_so_lips_pre` was populated with `LIPS-VBELN/POSNR` (the DO number/item)
  but read with `ls_so_first-ref_doc/ref_item` (the SO number/item). The preload
  always missed and the code fell through to the direct SELECT.
- `BAPI_OUTB_DELIVERY_CREATE_SLS` may create a DO but return an empty `DELIVERY`
  when `NUM_DELIVERIES > 1`. The code now imports and checks the count.
- The batch-split BAPI needs the main item in `ITEM_CONTROL` with
  `CHG_DELQTY = 'X'`; the field is `CHG_DELQTY` (not `CHG_DELQY`).
- SAP GUI custom toolbar buttons may not fire when the session window lacks OS
  focus. ALV built-in buttons (Select All / Deselect All) can still respond.
  Use a user click or focus the window before pressing a custom button.

## Evidence

- Deployed source: `patched_MODL_v10.abap`, 272,187 bytes,
  md5 `41380b876a114c6a71668282112211a3`.
- `_save_history` contains `FROM matdoc` and no `FROM mseg` / `FROM mkpf`.
- `syntax-check program ZDEMO01` → 0 findings; activate → OK; no inactive objects.
- Messages 033 and 041 updated; 044 and 045 added. Class has 39 entries.
- Client 900 at last check: `ZMMT015` has one VL09/602 row.
- Pending tests:
  1. Create DO / split `1041100092` with 50 + 10.
  2. Read LIPS: expect sub items `900001 = 50`, `900002 = 10`, and verify the
     main item quantity the BAPI leaves behind.
  3. Read ZMMT014: expect two rows with `UECHA = 000010`, `PGI_FLAG` blank.
  4. Post Goods Issue; verify ZMMT014 PGI fields and ZMMT015 601 rows.
  5. Re-run Post Goods Issue; expect msg 031 and no duplicate material document.

## Files

- Working directory: `<home>\AppData\Local\Temp\opencode\zmme011`
- Deployed source: `patched_MODL_v10.abap`
- Builder: `build_v10.py`
- Decisions log: `reports/DECISIONS.md`
