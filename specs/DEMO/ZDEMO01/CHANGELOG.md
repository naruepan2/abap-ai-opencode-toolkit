# ZDEMO01 - changelog

One row per deploy, newest first. Covers the window SAP does not: version
management only snapshots a TR when it is released. Detail and evidence:
`reports/DECISIONS.md`; before v12 only `DECISIONS.md` has a record.

| Ver | Date | What changed | Verified |
|---|---|---|---|
| v20 | 2026-11-14 | remove `CLEAR <ls_t010>` (GETWA dump) | syntax 0; 900 pending |
| v19 | 2026-11-14 | rename working types MSEG → MATDOC | syntax 0 |
| v18 | 2026-11-14 | VBPOK carries the sales order ref (VBELN/POSNN) | syntax 0 |
| v17 | 2026-11-14 | 601 read from MATDOC; drop `CLEAR <ls_mseg>` dump | syntax 0 |
| v16 | 2026-11-14 | VBPOK carries UMVKZ/UMVKN (unit conversion) | syntax 0 |
| v15 | 2026-11-14 | pick + PGI in one `WS_DELIVERY_UPDATE_2` | syntax 0 |
| v14 | 2026-11-14 | hide posted DOs; issue no. after Create DO | syntax 0 |
| v13 | 2026-11-14 | ALV follow-ups: hide 3 columns, blank SO keys, keep message, unsigned qty | 900 OK |
| v12 | 2026-11-14 | new ALV column `OPEN_SO_QTY` | 900 OK |
