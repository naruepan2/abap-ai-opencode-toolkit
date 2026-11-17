---
name: sap-mcp-upgrade
description: Upgrade an MCP server version or add a new MCP entry in OpenCode from evidence, not memory. Use for "upgrade MCP", "bump pin", "update sap-gui version", "check MCP version", "add MCP server", "new MCP entry", "MCP pin drift". Reads the live config, upstream changelog and installed package; never enables a server, installs silently, or restarts a daemon without asking. Not for posture flags or write gates — use docs/mcp-orchestration.md.
---

# SAP MCP upgrade

One change at a time: one server, one version token, one verification.
The live config is the target. The upstream release is the source of truth.
Your memory of the last version is not evidence.

The catalog plan lives in `docs/plan-mcp-pins.md`. Until that plan is executed,
use the manual commands below. Do not call a script that does not exist.

## Stop first

Ask before any of these:

- editing `~/.config/opencode/opencode.json`
- installing or upgrading a package
- restarting the opencode service daemon
- connecting to SAP

Never kill an MCP process to force a reload. The namespace disappears for the
rest of the session. A server stays `enabled:false` in the steady state; enable
it only for the task that needs it, then set it back.

## 1. Read the current state

```powershell
python scripts\registry_check.py --check --brief
python scripts\tools_now.py
```

Open the MCP entry in `~/.config/opencode/opencode.json`. Quote its exact
`command` array. Record the pin token, for example `mcp-sap-gui[screenshots]==0.6.1`.
Note whether the server is enabled and how many tools it contributes.

## 2. Probe upstream — read only

Fetch the vendor's release API or PyPI JSON. Read the changelog for the target
version. Report:

- current pin
- latest published version
- breaking changes in tool names or arguments
- the exact source URL

If there is no newer version, say so and stop. A probe never writes anything.

## 3. Upgrade — only after approval

1. Read the changelog. If a tool name or argument changed, stop and ask — the
   knowledge base and skills may need an edit before the pin moves.
2. Back up the live config:

   ```powershell
   $cfg = "$env:USERPROFILE\.config\opencode\opencode.json"
   Copy-Item $cfg "$cfg.bak"
   ```

3. Edit **only** the version token in the command array. Keep `enabled`, the
   URL, the profile, and every other entry exactly as they were.
4. Resolve the pinned package with the package manager already in the command.
   For `uvx`:

   ```powershell
   cmd /c "uvx mcp-sap-gui[screenshots]==0.6.1 --help >nul 2>&1"
   "EXIT=$LASTEXITCODE"
   ```

   Exit 0 means the package resolves. It does not mean the server is connected.
5. Ask the user to restart the opencode **service daemon**. Restarting the
   window does not reload MCP entries.

## 4. Verify after the restart

All four must pass before you claim success:

- catalog: the server is live with the expected tool count
  (`registry_check.py --check --brief`)
- process: the running command line contains the new pin
  (`Get-CimInstance Win32_Process | Where-Object CommandLine -like '*<pkg>*'`)
- package metadata: the installed distribution reports the new version
  (`mcp_sap_gui-0.6.1.dist-info` for uvx)
- one call: a read-only tool from that server answers, e.g.
  `sap_list_connections` for sap-gui

If the server needs SAP, ask the user to log on, then use `sap_connect_existing`.
A read-only probe result is not proof that a write will be confirmed.

## 5. Finish

- Run `python scripts\registry_check.py --refresh` if the tool list changed.
- Update the evidence line in memory from the old version to the new one.
- Set the server back to `enabled:false` when the task is over and ask for one
  more daemon restart.
- Report pin before/after, upstream version, source URL, tool counts, and
  which verification passed.

## Add a new server

Take command, package, pin, transport and tool count from the vendor docs. Add
the entry with `enabled:false`; do not enable it until a task asks for it. Then
follow steps 1, 4 and 5. Registries describe one machine — refresh the baseline
in the same change.

## Never

- bump a pin because a probe says newer, without reading the changelog
- enable every server "to be safe"
- edit a vendor agent or skill
- call `--help` success a connection test
- leave a task-scoped server enabled after the task
