# Knowledge: SAP data semantics

> Which table is the truth, and what a quantity means. One entry per rule; edit in
> place and raise `Seen`.

## `LIPS`/`LIKP` are the delivery truth

- **Rule:** read deliveries from `LIPS`/`LIKP`. A mirror such as `ZMMT014` is display
  metadata and may not be written at all.
- **Why:** deliveries are created outside the transaction too (VL01N, VL02N, VL09), so
  the mirror is not guaranteed.
- **Break it, and:** a delivery with no mirror row is invisible, and the open quantity
  is overstated (60 instead of 30).
- **Seen:** 1 · **Confidence:** high · **Last confirmed:** 2026-11-13
- **Evidence:** DO 1041100095 has `LIPS` rows and no `ZMMT014` row

## Open quantity is `SUM(LIPS-LFIMG)` per SO item

- **Rule:** open quantity = `KWMENG` − `SUM(LIPS-LFIMG)` over **every** delivery of
  the item. The split main item carries 0, so the sum over all items is correct.
- **Why:** picking status is display information; it must not drive the quantity.
- **Break it, and:** the open quantity counts picked or non-PGI rows twice and the
  user sees 60 where 30 is open.
- **Seen:** 1 · **Confidence:** high · **Last confirmed:** 2026-11-13
- **Evidence:** SO 1011099686/10 — `LIPS` 0+50+10; implemented in ZDEMO01 v11

## One goods-receipt row per DO item

- **Rule:** emit one editable row per delivery item, and an editable row only for the
  open remainder of that batch. `MENGE_PD` drops at Post Goods Issue, not before.
- **Why:** the DO item is the unit of action; the batch record is the unit of stock.
- **Break it, and:** four rows appear for two items and the user posts the same
  quantity twice.
- **Seen:** 1 · **Confidence:** high · **Last confirmed:** 2026-11-13
- **Evidence:** ZMMT010 50+20 and ZMMT014 50+10 produced 4 rows before the fix
