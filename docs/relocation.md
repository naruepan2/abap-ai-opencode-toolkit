# Relocation playbook — moving the toolkit or the instance

> On-demand reference. Read this when `D:\Opencode Projects` (or `~/.config/opencode`)
> moves, or when a new machine must use the same toolkit. The repo is self-resolving;
> the hazards are the **global AGENTS pointer** and the **absolute junction targets**.
> No file here changes prompt cost. Nothing here authorises SAP access.

## What survives a move automatically

- `scripts/_paths.py:23` — `REPO = Path(__file__).resolve().parent.parent`. Every script
  derives its location from itself, not from a drive letter.
- `scripts/_paths.py:9-14,34-38` — three env overrides for a different layout:
  `ABAP_WORKSPACE` (instance dir), `ABAP_PROJECTS_ROOT` (program folders),
  `ABAP_INDEX` (portfolio index).
- `scripts/install.ps1:43-44,70-83` — `$PSScriptRoot` / `$HOME`, no hardcoded drive.
- `scripts/closeout.py` portability check — shipped files contain no machine-only path
  (verified clean 2026-11-25).

## What does NOT survive

| Item | Why | Evidence |
|---|---|---|
| global `~/.config/opencode/AGENTS.md:68` | literal `D:\Opencode Projects\SAP Projects\abap-ai-opencode-toolkit` in the session-start instruction | read this session |
| junction targets | 43/43 targets in `manifest.json` are absolute `D:\...` / `C:\...` | backup `opencode-20261125-123448` |
| `~/.config/opencode/opencode.json` MCP commands | local servers name `C:\Users\narue\...` | read this session |
| SAP secrets in Windows Credential Manager | keyed to the user account, not to this repo | `sap-mcp-upgrade` skill |

## Move procedure

1. **Tell the AI the new root explicitly.** It cannot infer a moved root from a past chat;
   chat history is not on disk. Say: `toolkit อยู่ที่ <new path> — session start ให้รัน
   python scripts\session_context.py จากที่นั่น`.
2. **Clone / copy the repo** to the new path. Git carries scripts, templates, docs,
   registries, config. `workspace/` is git-ignored instance data — copy it from the
   latest `Backup/opencode-<timestamp>/workspace/`, not from git.
3. **Set env overrides only if the layout differs.** Same relative layout → nothing to
   set. Different root → set `ABAP_WORKSPACE`, `ABAP_PROJECTS_ROOT`, `ABAP_INDEX`
   (`_paths.py:9-14`). Verify: `python scripts/tools_now.py`.
4. **Fix the global AGENTS pointer.** Edit `~/.config/opencode/AGENTS.md:66-71` so the
   session-start command names the new root (or a portable form). This is the step that
   makes a fresh session find the toolkit without being told again.
5. **Restore config selectively.** Copy backed-up `config/` files without overwriting
   newer ones; re-point local MCP commands to new paths in `opencode.json`. SAP servers
   stay `enabled:false` (on-demand, D-30 posture).
6. **Recreate junctions from the manifest** — the exact command and order are already in
   `scripts/backup_opencode.ps1:39-45`:
   `New-Item -ItemType Junction -Path <manifest.source> -Target <new-target>`; edit each
   target that moved, keep the ones that are separate git repos elsewhere. Do not copy
   junction targets as ordinary folders (they are separate repos).
7. **Re-store SAP secrets** with `sap\store-sap-secret.ps1` if the user account changed;
   a 401 after a password change means re-store, never retry the old value.
8. **Verify before claiming the move worked** — all from the new root:
   `python scripts/session_context.py --brief`, `python scripts/registry_check.py --check --brief`,
   `python scripts/memory_check.py --brief`, `python scripts/closeout.py`,
   `python scripts/compatibility_check.py`. Expect 0 issues; warnings are human decisions.

## Rules

- Never edit vendored agents/skills; restore personal `*-by-pongg` files from the toolkit.
- Never store passwords in `opencode.json` or any doc; keychain only.
- A backup is not a restore until the checks in step 8 pass from the new root.
- Record a real move as one `note:` row in `docs/idea-ledger.md` with the old root, new
  root and the verification commit — so a future session can find it without re-asking.
- This file is navigation evidence, not a runbook that grants authority; SAP remains
  on-demand and no external effect is approved by reading this document.
