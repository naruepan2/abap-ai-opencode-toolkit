# <PROGRAM> - changelog

One row per deploy, newest first. This covers the window SAP does not: version
management only snapshots a TR **when it is released**, so until then the system
holds only the current code. Detail and evidence: `reports/DECISIONS.md`.

| Ver | Date | What changed | Verified |
|---|---|---|---|
| v20 | YYYY-MM-DD | <one line, past tense> | syntax 0 |
| v19 | YYYY-MM-DD | <one line> | 900 OK |

Rules:
- **One line per deploy.** No md5, no file list, no rollback recipe - `DECISIONS.md`
  has the bytes, SAP has the released versions.
- `Verified`: `900 OK` (runtime seen in client 900), `syntax 0` (activated, not
  exercised), `pending`.
- Newest row first; the first row must match the spec `implemented_version`.
- **At TR release, collapse the whole block into one line** - after that SAP is
  authoritative and this file only needs the pointer:

```markdown
## Released

- TR `DS4K904935` released 2026-11-20 - v1-v23 (SAP version management is the record)
```
