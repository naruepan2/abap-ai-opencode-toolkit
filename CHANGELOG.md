# Changelog

## v0.3.2 — 2026-11-13

- ZDEMO01 `_save_history` now reads `MATDOC` instead of `MKPF` + `MSEG`.
  Header fields (`BUDAT`, `CPUDT`, `CPUTM`, `USNAM`, `BKTXT`) and item fields
  (`VBELN_IM`, `VBELP_IM`, `BWART`, material, plant, sloc, batch, quantity) come
  from one table.
- Deployment: `ZDEMO01_MODL` v10 (transport `DS4K904935`); syntax 0 findings,
  active, no inactive objects.

## v0.3.1 — 2026-11-13

- Scanner: flatten the V2 `mcp.servers` shape (the `browse` server is now in the
  MCP registry) and support `optional_namespaces` in the tool baseline.
- Marked `ds4-100` / `ds4-900` optional so enabling an on-demand SAP server does
  not produce false tool drift.
- Captured the ZDEMO01 v7–v9 debugging lessons: preload key mismatch (DO vs SO),
  `BAPI_OUTB_DELIVERY_CREATE_SLS` `NUM_DELIVERIES`, batch-split main-item
  control, `ZMMT014-UECHA`, and the SAP GUI custom-button focus caveat.
- Deployment: `ZDEMO01_MODL` v9 (transport `DS4K904935`); messages 033/041 now
  use “Post Goods Issue”, messages 044/045 added.

## v0.3 — 2026-11-13

- Added `plugins/tool-snapshot`: an OpenCode server plugin that writes
  `registries/tools-snapshot.json` and `registries/tools-full.json` from
  `ctx.tool.list()`. It refreshes on load and on MCP/tool/session events, and only
  rewrites when the tool set changes.
- The scanner now records tool IDs in `registries/tools.json` and reports new or
  missing tools.
- `--refresh` adds newly discovered assets with `status: new`; stale checks skip
  `new` rows.
- Updated `sap-ai-dev-toolkit` from 0.9.9922 to 0.9.9924. The npm install emitted
  a postinstall warning for `@sap/hana-client` (`checkbuild.js` missing); the core
  launcher and VSP binary still respond.
- The toolkit update added 6 Copilot skills and 5 Copilot agents (BTP,
  BW/DataSphere, Cloud ALM, DataSphere, process automation, DevOps observability).
  They are vendor assets and are recorded in the Copilot registry only.

## v0.2 — 2026-11-13

- Added the read-only registry scanner (`scripts/registry_check.py`).
- Added machine-readable registries for skills, agents, MCP servers, and tools.
- Added the session-start registry brief to the global `AGENTS.md`.
- Disabled the drifted `ds4-100` MCP server (SAP is on-demand).
- Split actionable issues from informational warnings.
- Added the team model, task lifecycle diagrams, and the comparison template.

## v0.1 — 2026-11-13

- Bootstrapped the workspace: user profile, lessons, corrections, skill
  candidates, agent registry, tool map, team roster, and the ZDEMO01 project card.
- Added `README.md`, `AGENTS.md`, `SECURITY.md`, and the design/lifecycle docs.
