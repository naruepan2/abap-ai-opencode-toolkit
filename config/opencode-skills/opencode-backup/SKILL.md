---
name: opencode-backup
description: Manual-only backup of OpenCode instance data and curated config into a dated, hash-verified snapshot, with optional cleanup of stale backups. Use only when the user explicitly invokes /opencode-backup, types @opencode-backup, or directly asks to back up OpenCode. Never at session start, from a digest, on a timer, or for an ordinary request.
metadata:
  opencode/autoinvoke: false
disable-model-invocation: true
---
# OpenCode Backup

Run **only after explicit user invocation**. This is opt-in, not a background
habit. Never start it from a session-start digest, a timer, or a normal coding
request — even if the user mentions backups in passing.

Treat the toolkit repo as the source of the script: resolve its root from the
global `AGENTS.md` pointer, then run `scripts/backup_opencode.ps1` from that
root. The script is the single implementation; do not rewrite it inside this
skill.

## 1. Confirm scope before any write

Ask only if the destination is not obvious. The default is `<toolkit>/Backup`
(git-ignored). The script refuses any destination inside `workspace/` or
`~/.config/opencode` — a destination inside a source tree makes robocopy copy
itself forever.

State what will be excluded and why:

| Excluded | Reason |
|---|---|
| `service.json` | plaintext OpenCode service password |
| SAP passwords | Windows Credential Manager, machine-bound — re-store on the new machine |
| `memory` junction, vendor clones, `skills-parked/` junction targets | re-creatable / separate git repos; targets are recorded in the manifest |
| `*.bak*`, `sap-gui-audit.jsonl`, `memory.live-backup-*` | stale or noisy; archived separately if the user asks |
| session DB while OpenCode is running | SQLite WAL may be inconsistent; only with `-IncludeSessions` after the user closes OpenCode |

## 2. Dry run, then run

```powershell
# from the toolkit root
.\scripts\backup_opencode.ps1 -Destination "<toolkit>\Backup" -DryRun
.\scripts\backup_opencode.ps1 -Destination "<toolkit>\Backup"
```

Optional, only after the user confirms OpenCode is closed:
`-IncludeSessions`. If the DB is locked, the script records
`session_unverified` instead of failing — report that; never call a locked
session copy verified.

## 3. Verify before reporting done

Read `<snapshot>/manifest.json` and require:

- `ok: true`, `failures: []`
- `workspace_files` and `config_files` are non-zero and match the counts shown
- `junctions` is recorded (typically ~43)
- `config/service.json` is **absent**
- no credential-looking literal in the manifest

Report the snapshot path, file counts, size, and the exclusions. Never claim
success from the "copy" lines alone.

## 4. Cleanup — only when the user asks

Move, never delete:

- all `opencode.json.bak*` except the **two newest**, to
  `<toolkit>\Backup\archive-<date>`
- `sap-gui-audit.jsonl` and `memory.live-backup-*` to the same archive

Never touch `skills-parked/`, `abap-skills/`, `open-computer-use/`, or
`opencode.db` during cleanup.

## 5. Restore note (handoff, not an action)

Clone the repo → `install.ps1 -Seed` → restore `workspace/` at the same path
(or set `ABAP_WORKSPACE`) → restore `config/` without overwriting newer files →
recreate junctions from the manifest with `New-Item -ItemType Junction` →
restore `session/` only if verified → re-store SAP secrets with
`sap\store-sap-secret.ps1` → verify with `session_context.py` and
`registry_check.py --check`.

## Never

- auto-run this skill for any reason
- point the destination inside a source tree
- include `service.json`, tokens, or SAP credentials in a snapshot
- delete source files while "cleaning up"
- report success without reading the manifest
- treat a same-disk snapshot as protection against disk failure — tell the user
  to copy `Backup/` to external or cloud storage periodically
