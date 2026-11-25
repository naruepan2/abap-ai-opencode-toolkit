# Relocation playbook — moving the toolkit or the instance

> On-demand reference. Read this when the portfolio root or `~/.config/opencode`
> moves, or when a new machine must use the same toolkit. The repo is self-resolving;
> the hazards are the **global AGENTS pointer** and the **absolute junction targets**.
> No file here changes prompt cost. Nothing here authorises SAP access.

## What survives a move automatically

- `scripts/_paths.py:23` — `REPO = Path(__file__).resolve().parent.parent`. Every script
  derives its location from itself, not from a drive letter.
- `scripts/_paths.py:9-14,34-38` — three env overrides for a different layout:
  `ABAP_WORKSPACE` (instance dir), `ABAP_PROJECTS_ROOT` (program folders),
  `ABAP_INDEX` (portfolio index).
- `install.ps1:43-44,70-83` — `$PSScriptRoot` / `$HOME`, no hardcoded drive (root-level file).
- `scripts/closeout.py` portability check — shipped files contain no machine-only path
  (verified clean 2026-11-25).

## What does NOT survive

| Item | Why | Evidence |
|---|---|---|
| global `~/.config/opencode/AGENTS.md:68` | literal absolute portfolio path in the session-start instruction | read this session |
| junction targets | targets in `manifest.json` are absolute drive paths | backup manifest, verified this session |
| `~/.config/opencode/opencode.json` MCP commands | local servers name absolute home paths | read this session |
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

## Dry-run evidence (2026-11-25, simulated — not a real move)

A copy of the toolkit was placed in a temporary directory and all checks were run from that
new root using env overrides, with the SAP MCP servers parked. The instance data came from
the latest backup. No file in the real toolkit or instance was modified.

| Check | Result |
|---|---|
| `session_context.py --brief` | pass — card, health, tool rules loaded from the new root |
| `registry_check.py --check --brief` | 0 issues / 8 warnings, 126 tools, 7 namespaces |
| `memory_check.py --brief` | 0 issues / 0 warnings |
| `closeout.py` | clean; audit line `adds 0, updates 1, deletes 0, skipped 0` |
| `compatibility_check.py` | valid, no errors |
| `tools_now.py --check` | exit 1 **expected** — SAP MCP is parked; not a playbook defect |

Caveats:
- `ABAP_INDEX` was set one level too low in the dry run (a test-setup mistake, not a
  playbook defect); the default is `PROJECTS.parent.parent / INDEX.md`, i.e. one level
  above the `SAP Projects` folder. Step 3 in this playbook is correct as written.
- `tools_now.py --check` reports `none` because the SAP servers are parked; that is the
  intended steady state (see §SAP on-demand in `tool-map.md`).
- The `closeout` card showed v37 / 30 REQ / 29 AC / 26 changelog rows, newer than the
  toolkit's last close-out (v36 / 29 REQ / 28 AC / 25 rows). The mirror stayed in sync.

Status: playbook logic **verified** on a copy. Still `UNVERIFIED` against a real move —
junction rewire, global AGENTS pointer, config paths and SAP credentials were not exercised.

## Rules

- Never edit vendored agents/skills; restore personal `*-by-pongg` files from the toolkit.
- Never store passwords in `opencode.json` or any doc; keychain only.
- A backup is not a restore until the checks in step 8 pass from the new root.
- Record a real move as one `note:` row in `docs/idea-ledger.md` with the old root, new
  root and the verification commit — so a future session can find it without re-asking.
- This file is navigation evidence, not a runbook that grants authority; SAP remains
  on-demand and no external effect is approved by reading this document.
