---
name: sap-mcp-upgrade
description: Check or upgrade MCP server versions in OpenCode from evidence in one pass. Use for "upgrade MCP", "bump pin", "update sap-gui version", "check MCP version", "add MCP server", "MCP pin drift". Scans known servers, batches approval, one restart, one verification.
---

# SAP MCP upgrade

**Batch-first.** Scan every known server in one pass, present one table, ask one
approval, apply all non-breaking upgrades, restart the daemon once, verify once,
restore once. The live config is the target; upstream release data is the source
of truth. Memory of a last version is not evidence.

The catalog plan lives in `docs/plan-mcp-pins.md`. Until it is executed, use the
manual commands below. Do not call a script that does not exist.

## Stop first

Ask before any of these:

- editing `~/.config/opencode/opencode.json`
- installing or upgrading a package
- restarting the opencode service daemon
- connecting to SAP

Never kill an MCP process to force a reload — the namespace disappears for the
rest of the session. A task-scoped server stays `enabled:false` in the steady
state; enable it only for the task that needs it, then set it back.

## Known-server registry

Use this table to avoid asking "which one?" on every run. A server not listed
here gets one row added from vendor docs before it is probed.

| Server(s) | Pin location | Probe (read-only) | Source |
|---|---|---|---|
| `ai-dev-*` (ds4-100/900, sus-100, gsd-120) | env `SAP_AI_DEV_TOOLKIT_VERSION` in `sap-mcp.ps1` (0.9.9928) | `https://registry.npmjs.org/sap-ai-dev-toolkit/latest` | github.com/grknylmz/sap-ai-dev-toolkit |
| `arc1-*` (ds4-100, sus-100, gsd-110) | npm global, unpinned (1.10.1) | `https://registry.npmjs.org/arc-1/latest` | github.com/arc-mcp/arc-1 |
| `sap-gui` | `mcp-sap-gui[screenshots]==0.6.1` in config command | `https://pypi.org/pypi/mcp-sap-gui/json` | github.com/kts982/mcp-sap-gui |
| `sap-docs` | hosted HTTP, no local pin | endpoint status / release notes | github.com/marianfoo/mcp-sap-docs |
| `playwright` | npm global, unpinned | `https://registry.npmjs.org/@playwright/mcp/latest` | github.com/microsoft/playwright-mcp |
| `open-computer-use` | npm global, unpinned | `https://registry.npmjs.org/open-computer-use/latest` | github.com/iFurySt/open-computer-use |
| `windows-mcp` | uvx tool, unpinned (0.8.8) | `https://pypi.org/pypi/windows-mcp/json` | github.com/CursorTouch/Windows-MCP |
| `browse` | self-updating CLI (`browse --version`) + npm `@opencode/browse` | `browse status`, Anomaly release channel | github.com/anomalyco/browse |
| `opencode_console`, `browser`, built-ins | none | n/a | github.com/anomalyco/opencode |

One package can back several server entries (e.g. `ai-dev-*`). Upgrade the
package **once**, not once per entry.

## 1. One-pass scan — read only

```powershell
python scripts\registry_check.py --check --brief
python scripts\tools_now.py
npm ls -g --depth=0
```

- Read each config entry's exact `command` / `type` / `url` and `enabled`.
- Read pins from the table above (config command, launcher env var, global
  package, CLI version).
- Probe upstream endpoints in one batch. Read the changelog for every version
  that is ahead.
- Output **one** table:

```
server | current | latest | pin location | breaking? | source URL
```

**Terminal case:** if no server is behind, report "all known servers current"
with the table and STOP. Do not ask "update anything else?" — that question is
the one this redesign removes.

## 2. One approval for the batch

- Non-breaking upgrades → one question: `apply all listed upgrades?` with
  options `yes / choose subset / no`. Default = no.
- Breaking change in a tool name or argument → exclude that server from the
  batch, report it separately, and ask only about that one. Knowledge base and
  skills may need an edit before its pin moves.
- Hosted/self-updating servers are reported, never manually bumped.

## 3. Apply once

1. Back up the live config once:

   ```powershell
   $cfg = "$env:USERPROFILE\.config\opencode\opencode.json"
   Copy-Item $cfg "$cfg.bak"
   ```

2. Edit **only** version tokens. Keep `enabled`, URL, profile and every other
   field exactly as they were.
3. Install/resolve with the manager already in the command. For `uvx`:

   ```powershell
   cmd /c "uvx mcp-sap-gui[screenshots]==0.6.1 --help >nul 2>&1"
   "EXIT=$LASTEXITCODE"
   ```

   Exit 0 means the package resolves, not that the server is connected.
4. Ask once for an opencode **service daemon** restart. Restarting the window
   does not reload MCP entries.

## 4. Verify all changed servers in one pass

For every changed server, all four must pass before claiming success:

- catalog: expected namespace and tool count (`registry_check.py --check --brief`)
- process: running command line contains the new pin
  (`Get-CimInstance Win32_Process | Where-Object CommandLine -like '*<pkg>*'`)
- package metadata: installed distribution reports the new version
- one read-only call from that server (e.g. `sap_list_connections` for sap-gui)

A server that needs SAP requires user logon; then use `sap_connect_existing`.
A read-only answer is not proof a write will be confirmed.

## 5. Finish once

- `registry_check.py --refresh` only if the tool list changed.
- Update the evidence line in memory from old version to new.
- Set every task-scoped server back to `enabled:false`; ask for one final daemon
  restart if their state changed.
- Report: per-server pin before/after, upstream version, source URL, tool
  counts, verification results, and an explicit **"no further upgrades pending"**
  so the user does not have to ask what is next.

## Add a new server

Take command, package, pin, transport and tool count from vendor docs. Add the
entry with `enabled:false`; do not enable it until a task asks. Add a row to the
registry table above, then follow steps 1, 3, 4 and 5. Registries describe one
machine — refresh the baseline in the same change.

## Never

- bump a pin because a probe says newer, without reading the changelog
- ask which server to upgrade when the registry table already answers it
- ask again after reporting "all current" — that is the terminal result
- enable every server "to be safe"
- edit a vendor agent or skill (only personal skills may change, with approval)
- call `--help` success a connection test
- leave a task-scoped server enabled after the task
