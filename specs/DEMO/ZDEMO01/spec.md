---
program: ZDEMO01
project: DEMO
spec_version: 1.1
status: active
fs_version: V4.0
fs_date: 2026-10-18
fs_file: spec/source/FS_ZDEMO01_V4.0_20261018.md
fs_original_name: "IPLATFORMANCE_DEMO_FS_MM_ZDEMO01_Split batch at External WH and Report_V4.0_20261018.md"
scope: FS Option 8 only - create DO, batch split, issue no., PGI at the external storage location
implemented_version: v21
owner: Pongg
updated: 2026-11-14
---

# ZDEMO01 - spec (FS Option 8)

The contract we build and test against. `AGENTS.md` holds the rules, `reports/DECISIONS.md`
holds the why, `templates/plan.md` holds the order of work. This file holds **what** and
**how we know it is done**. Change a requirement here before changing code.

## 1. Purpose

FG stock that sits at an external warehouse must leave against a Sales Order: create an
outbound Delivery Order with a batch split, record the issue document, then post the goods
issue and keep the quantity history in `ZMMT014` / `ZMMT015`.

| Item | Value |
|---|---|
| Actor | MM / warehouse user, transaction `ZDEMO01`, radio button Option 8 |
| Trigger | Execute 1 = create DO + batch split + issue no.; Execute 2 = PGI |
| Target | DS4, code client 100, test client 900, transport `DS4K904935` |

## 2. Scope

| In | Out |
|---|---|
| FS Option 8 only: DO + batch split + issue document + PGI | Options 1-7 (GR, split/update, transfer 311/309, conversion, report) |
| `ZDEMO01_MODL`, `ZDEMO01_MSG`, `ZDEMO01_VIEW` (ALV field catalog only) | SAP standard code |
| `ZMMT010`, `ZMMT012`, `ZMMT014`, `ZMMT015` read/write | VL09 / VL02N reversal history - FS L96-118, a separate BAdI object (`MB_DOCUMENT_BADI`), not this program |

## 3. Requirements

Status: `implemented` = built and runtime-verified; `pending-test` = built, runtime test not
recorded; `pending` = not built; `out-of-scope`.

| ID | Requirement (one line, testable) | FS | Status | Since |
|---|---|---|---|---|
| REQ-01 | Entering a Sales Order lists `ZMMT010` rows whose `MATNR`/`WERKS`/`LGORT` match `VBAP` and `MENGE_PD > 0` | L1459-1469 | implemented | v10 |
| REQ-02 | The user enters SO / SO item / quantity per batch row; the quantity is editable and cannot exceed the external-warehouse stock; once that row's DO and batch split succeed the quantity (`Ex.WH.Stck`) turns display-only | L1469, DEV-02, DEV-06 | implemented | v11 |
| REQ-03 | Create an outbound Delivery Order referencing the Sales Order, with batch-split sub items under one main item; the sub-item quantities sum to the main item quantity | L1471 | implemented | v6 |
| REQ-04 | Group by plant, storage location and material; the main item carries the total; different batches become sub items `900001`, `900002`, ... | L1473-1476 | implemented | v6 |
| REQ-05 | Create the DO with `BAPI_OUTB_DELIVERY_CREATE_SLS` (`SHIP_POINT` = `VBAP-VSTEL`, `DUE_DATE` = `SY-DATUM`, `REF_DOC`/`REF_ITEM`, `DLV_QTY` = main-item total, `SALES_UNIT` = `VBAP-ZIEME`) and commit with `WAIT = X` only when no E/A message | L1482-1502 | implemented | v6 |
| REQ-06 | Split the batches with `BAPI_OUTB_DELIVERY_CHANGE` (`HIERARITEM` = main item, `USEHIERITM` = 1, batch, `DLV_QTY`/`DLV_QTY_IMUNIT`, `ITEM_CONTROL-CHG_DELQTY` = X) and commit only when no E/A message | L1504-1560 | implemented | v6 |
| REQ-07 | Create the issue document, store it in `ZMMT012` (the FS writes `ZMMMT012`), and show the DO number plus the issue number | L1562-1566 | pending-test | v14 |
| REQ-08 | Execute 2 gates on picking status: C (or no picking required) posts immediately; A/B requires the picking quantity on the split sub items first | L1570-1575 | pending-test | v15 |
| REQ-09 | Post the goods issue with `WS_DELIVERY_UPDATE_2` (`VBELN_VL`, `WABUC` = X, `WADAT_IST`, `DELIVERY`, `SYNCHRON` = X, `COMMIT` = X) referencing the displayed DO | L1577-1593 | pending-test | v15 |
| REQ-10 | After the goods issue, subtract `MATDOC-MENGE` (BWART 601) from `ZMMT010-MENGE_PD` and add it to `MENGE_GI` | L1595-1599 | pending-test | v6 |
| REQ-11 | Write the 601 material document lines to `ZMMT014` (one row per batch-split sub item) and the material document to `ZMMT015` | L1601 | pending-test | v6 |
| REQ-12 | VL09 reversal and VL02N goods return (602/653/655) update `ZMMT013-MENGE_GI` and the `ZMMT014` history | L96-118 | out-of-scope | - |

## 4. Acceptance criteria

Each AC is one run in client 900 unless stated. `Pending` means no evidence is recorded yet -
do not report it as passed.

| ID | Given / When / Then | REQ | Evidence |
|---|---|---|---|
| AC-01 | Given SO `1011099686`/10 (KWMENG 60), when Option 8 runs, then the editable row offers 30 KG (not 60) and the two `1041100095` lines are shown read-only | REQ-01, REQ-02 | client 900, 2026-11-14 (v11/v12) |
| AC-02 | Given a selected editable row, when Create DO runs, then a second DO for 30 KG is created with a batch split, and neither the existing split DO nor its 30 KG blocks it | REQ-03, REQ-05, REQ-06 | client 900, 2026-11-14 (partial) |
| AC-03 | Given a DO that is already batch-split, when Create DO runs again for it, then the program does not reuse or re-split it and message 041 is shown | REQ-03 | client 900, 2026-11-14 |
| AC-04 | Given a DO created by Option 8, when Create DO completes, then an issue number is stored in `ZMMT012` and shown with the DO | REQ-07 | Pending |
| AC-05 | Given a DO with picking A/B, when Execute 2 runs, then the DO ends picked and posted (`WBSTK = C`) with a 601 material document, or a standard error is shown - never picked but not posted | REQ-08, REQ-09 | Pending |
| AC-06 | Given a successful PGI, when the ALV is read back, then `MENGE_PD` decreased by the 601 quantity, `MENGE_GI` increased by the same, and the units are the base UoM | REQ-10 | Pending (Q-08) |
| AC-07 | Given a successful PGI, when `ZMMT014`/`ZMMT015` are read, then one `ZMMT014` row per split sub item has `PGI_FLAG = 'X'` and `ZMMT015` has one row per 601 material document | REQ-11 | Pending |
| AC-08 | Given a posted DO, when Option 8 is executed, then the posted delivery is no longer listed | REQ-01 | client 900, 2026-11-14 (v14) |
| AC-09 | Given a quantity above the open quantity, when Create DO runs, then it is blocked by the GR-pending / KWMENG / live-LIPS checks (no bypass at 0) | REQ-02 | client 900, v11 |
| AC-10 | Given an SO item with no `ZMMT010` row, when Option 8 runs and Create DO is pressed, then the program reports the condition and does not dump with `GETWA_NOT_ASSIGNED` | REQ-01 | built v20, runtime Pending |
| AC-11 | Given a row whose DO and batch split succeeded, when the ALV refreshes, then `Ex.WH.Stck` on that row is display-only while rows without a DO stay editable | REQ-02 | built v21, runtime Pending |

## 5. Deviations from the FS (approved)

| ID | FS says | We do | Why / approval |
|---|---|---|---|
| DEV-01 | `UPDATE_PICKING` and `VBPOK_TAB` stay blank (L1591, L1593), while L1575 says the picking quantity on the sub items must be updated first | One `WS_DELIVERY_UPDATE_2` with `UPDATE_PICKING = 'X'` and `VBPOK` rows (`PIKMG`, `UMVKZ`/`UMVKN`, SO ref) | D15.1/D15.3, 2026-11-14; removes the picked-but-not-posted state. Runtime Pending |
| DEV-02 | Open quantity from `ZMMT010-MENGE_PD > 0` (L1467) | `KWMENG - SUM(LIPS-LFIMG)` per SO item; the editable row is the open remainder per batch | D11.1-D11.4, 2026-11-13 |
| DEV-03 | No extra ALV column | `OPEN_SO_QTY` between TF DEMO Qty and Ex.WH.Stck, editable rows only | v12, user-approved 2026-11-14 |
| DEV-04 | FS does not say to hide posted deliveries | Posted DOs (`PGI_FLAG = 'X'` / `WBSTK = 'C'`) are removed from the list | D14.1, 2026-11-14 |
| DEV-06 | FS L1469 lets the user edit the GI quantity freely | The row's quantity (`Ex.WH.Stck`) is locked as soon as its DO + batch split succeed, so the ALV cannot drift from the delivery it created | user request 2026-11-14, v21 |

## 6. Open questions (do not guess)

Optional helper: a Thai copy for the FS owner in `reports/FS_QUESTIONS.md`; it is
not part of the contract and can be deleted. The table below is the source of truth.

| ID | Question | Impact | State |
|---|---|---|---|
| Q-01 | FS L1601 says "update `ZMMT014` as follows" but the field mapping is missing | History fields are implementation-defined | open |
| Q-02 | `ZMMT013` is referenced and displayed but never defined in the FS | Reversal flow (REQ-12) cannot be specified | open |
| Q-03 | `ZMMT014-BUDAT` is declared twice (key and non-key) | Decide before the next table change | open |
| Q-04 | The issue form reads `ZMMT012-MENGE_TF_P`, which Option 8 never populates | Printed issue document may show 0 | open |
| Q-05 | FS L1537 says the main item is **not** zeroed, but the split leaves `LIPS-LFIMG = 0` on the main item | Sum over all `LIPS` items is correct either way; confirm with the FS author | open |
| Q-06 | Should `ZMMT014` also store the main item row? | Row count and report grouping | open |
| Q-07 | Is `ISSNO` ever populated in Option 8, and should `PGI_FLAG` reset on VL09? | History correctness after reversal | open |
| Q-08 | Is `MENGE_GI` in base UoM or sales UoM? | AC-06 tolerance | open |
| Q-09 | Is clamping `ZMMT010-MENGE_PD` at 0 acceptable when the 601 quantity is larger? | Hidden stock difference | open |
| Q-10 | Why does DO `1041100095` have no `ZMMT014` row - created outside ZDEMO01, or the history write was skipped? | Whether `ZMMT014` is the only history source | open |
| Q-11 | FS L736 titles Option 8 "Transfer Material to Material and Move to Ex.WH" (same as Option 7), while the content is DO + PGI | Wrong label in the FS only | open |
| Q-12 | `KWMENG`, `LIPS-LFIMG` and `ZMMT010-MEINS` are assumed to be the same unit (KG) | A different sales unit needs conversion | open |
| Q-13 | The FS body says `Document Version: V1.0` and the change control lists 1.0/2.0, while the filename says V4.0 (2026-10-18); the header also names the program "Goods Receipt at External WH" | Which revision is authoritative for sign-off | open |

## 7. Change log

| Spec | Date | Change |
|---|---|---|
| 1.1 | 2026-11-14 | REQ-02: `Ex.WH.Stck` (`MENGE_PD`) becomes display-only per row once its DO + batch split succeed (DEV-06, AC-11); implemented v21 |
| 1.0 | 2026-11-14 | First spec from FS V4.0 (moved to `spec/source/`), v1-v20 decisions, and the current ALV behaviour |
