# Knowledge: ABAP and APIs

> Contracts that SAP enforces on the code side. One entry per rule; edit in place
> and raise `Seen`.

## Batch split needs the main item in `ITEM_CONTROL`

- **Rule:** when the main item ships 0, send it in `ITEM_CONTROL` with
  `CHG_DELQTY = 'X'` together with the sub items.
- **Why:** the BAPI contract requires the parent when its quantity changes to zero.
- **Break it, and:** the split returns nothing, or leaves the delivery unsplit, after
  a call that reported no error.
- **Seen:** 2 · **Confidence:** high · **Last confirmed:** 2026-11-13
- **Evidence:** ZDEMO01 `lt_item_data`/`lt_item_control` debug; v8 fix

## BAPI create can return an empty `DELIVERY`

- **Rule:** `BAPI_OUTB_DELIVERY_CREATE_SLS` may create the document and still return
  an empty `DELIVERY` when `NUM_DELIVERIES > 1`. Recover the number from `LIPS`.
- **Why:** the return value is only filled for a single delivery.
- **Break it, and:** the code reports "not created" while one or two deliveries exist.
- **Seen:** 1 · **Confidence:** high · **Last confirmed:** 2026-11-13
- **Evidence:** DO 1041100092 created at 18:06:31 with an empty return field

## S/4HANA: read `MATDOC`, not `MKPF` + `MSEG`

- **Rule:** read material documents from `MATDOC`; header fields (`BUDAT`, `CPUDT`,
  `CPUTM`, `USNAM`, `BKTXT`) and item fields are in one table.
- **Why:** the S/4 view replaces the two legacy tables.
- **Break it, and:** two reads, a join you do not need, and a result that misses
  fields the view already has.
- **Seen:** 2 · **Confidence:** high · **Last confirmed:** 2026-11-13
- **Evidence:** MATDOC DDIC (350 fields); ZDEMO01 v10 deployed

## `mmt010~*` is a substructure

- **Rule:** address nested fields as `mmt010-mblnr`, not as flat `mblnr`/`mjahr`.
- **Why:** the internal table declares a structured component, not flat columns.
- **Break it, and:** syntax error "No component exists with the name MBLNR".
- **Seen:** 1 · **Confidence:** high · **Last confirmed:** 2026-11-13
- **Evidence:** syntax check line 1450 on `lt_so_zmmt010`

## Name a key by its source, not its shape

- **Rule:** when a preload holds a delivery key but is read with a sales-order key,
  rename the field to its source (`VBELN AS VBELN_VL`) so the mismatch cannot hide.
- **Why:** both are 10-character numbers; the compiler and the eye both accept them.
- **Break it, and:** the READ never matches and every quantity comes back as the full
  amount — a silent, plausible-looking wrong answer.
- **Seen:** 2 · **Confidence:** high · **Last confirmed:** 2026-11-13
- **Evidence:** ZDEMO01 debug line 5290; fixed in v8

## History rows are not actionable rows

- **Rule:** keep read-only history rows and editable rows in separate structures (or
  behind a `hist_flag`); only the open remainder is editable.
- **Why:** one loop for both meanings produces the same quantity twice.
- **Break it, and:** a guardrail blocks the work item ("already created") while the
  open quantity is still there.
- **Seen:** 1 · **Confidence:** medium · **Last confirmed:** 2026-11-13
- **Evidence:** ZDEMO01 v6 — messages 041 and the `hist_flag` decision
