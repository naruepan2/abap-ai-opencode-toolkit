# <PROGRAM> - changelog

One row per **deploy**. The contract is `spec.md`; the why and the evidence are in
`reports/DECISIONS.md`. This file only answers: *what shipped, and can I roll it back?*

| Ver | Date | Change (one line) | Files | Artifact | Active MD5 | Verified |
|---|---|---|---|---|---|---|
| v20 | YYYY-MM-DD | <what changed> | MODL | `<file>.abap` · <bytes> · `<md5>` | `<md5>` (<lines> L) | syntax 0 |
| v19 | YYYY-MM-DD | <what changed> | MODL+VIEW | `missing` | `<md5>` (<lines> L) | 900 OK |

Rules:
- **Never overwrite a deployed artifact.** The build writes a new `patched_MODL_vN.abap`;
  if `ZDEMO01_VIEW` changed, also keep `patched_VIEW_vN.abap`. If the artifact is
  gone, write `missing` - do not reconstruct a row from memory.
- `Artifact` is the local file you would write back. `Active MD5` is what
  `?version=active` returned after activation (SAP normalises it, so it will not
  equal the local md5 - record both, never infer one from the other).
- `Verified`: `900 OK` (runtime seen in client 900), `syntax 0` (activated, not
  exercised), or `pending`.
- Older history lives in `reports/DECISIONS.md`; do not copy it here.

## Rollback (one version)

```powershell
# 1. write the artifact from the row
write-source include <PROG>_MODL --file <artifact> --transport <TR> --yes
# 2. syntax check, then activate the include(s) and the program
syntax-check program <PROG>
activate include <PROG>_MODL --yes
activate include <PROG>_VIEW --yes      # only if the row changed VIEW
activate program <PROG> --yes
# 3. prove it: the active md5 must equal the row's Active MD5
```
