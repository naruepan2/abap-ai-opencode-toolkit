# ZDEMO01 - changelog

One row per deploy. Contract: `spec.md`. Why/evidence: `reports/DECISIONS.md`.
History before v12 is only in `reports/DECISIONS.md`.

> **Rollback gap:** `patched_MODL_v12.abap` / `v13.abap` were overwritten and no
> `build_v12/build_v13.py` exists, so those two cannot be reproduced exactly. The
> oldest artifact-backed version is **v14**; the newest runtime-verified is **v13**.
> From v14 on, every build writes a new file and never overwrites.

| Ver | Date | Change (one line) | Files | Artifact | Active MD5 | Verified |
|---|---|---|---|---|---|---|
| v20 | 2026-11-14 | remove `CLEAR <ls_t010>` (GETWA dump) | MODL | `patched_MODL_v20.abap` · 281,414 · `6f0c4fb1…` | `1f488c7b…` (7,174 L) | syntax 0; 900 pending |
| v19 | 2026-11-14 | rename working types MSEG → MATDOC | MODL | `patched_MODL_v19.abap` · 281,440 · `18691188…` | `30a1aa3d…` (7,175 L) | syntax 0 |
| v18 | 2026-11-14 | VBPOK carries the sales order ref (VBELN/POSNN) | MODL | `patched_MODL_v18.abap` · 281,306 · `b1e1d04b…` | `3df1539c…` (7,175 L) | syntax 0 |
| v17 | 2026-11-14 | 601 read from MATDOC; drop `CLEAR <ls_mseg>` dump | MODL | `patched_MODL_v17.abap` · 281,110 · `70e4fba4…` | `3698e0ce…` (7,171 L) | syntax 0 |
| v16 | 2026-11-14 | VBPOK carries UMVKZ/UMVKN (unit conversion) | MODL | `patched_MODL_v16.abap` · 281,134 · `dd54df7f…` | `632fc5f6…` (7,172 L) | syntax 0 |
| v15 | 2026-11-14 | pick + PGI in one `WS_DELIVERY_UPDATE_2` | MODL | `patched_MODL_v15.abap` · 280,394 · `ba1dbaa2…` | `0be2bab3…` (7,152 L) | syntax 0 |
| v14 | 2026-11-14 | hide posted DOs; issue no. after Create DO | MODL | `patched_MODL_v14.abap` · 283,998 · `140c0579…` | `a2eed355…` (7,255 L) | syntax 0 |
| v13 | 2026-11-14 | ALV follow-ups: hide 3 columns, blank SO keys, keep message, unsigned qty | MODL+VIEW | `missing` | `e2c2a16c…` (7,167 L) | 900 OK |
| v12 | 2026-11-14 | new ALV column `OPEN_SO_QTY` | MODL+VIEW | `missing` | `c3f3a8b9…` (7,166 L) | 900 OK |

## Rollback (one version)

```powershell
# 1. write the artifact from the row  (VIEW only when Files says MODL+VIEW)
write-source include ZDEMO01_MODL --file patched_MODL_v19.abap --transport DS4K904935 --yes
# 2. syntax check, then activate include(s) + program
syntax-check program ZDEMO01
activate include ZDEMO01_MODL --yes
activate program ZDEMO01 --yes
# 3. prove it: the ACTIVE md5 must equal the row's Active MD5
```
