# Changelog

## v0.5 — 2026-11-14

**Memory became a knowledge base instead of a work log.** Design: `docs/memory-model.md`.

- `memory/knowledge/` — 24 entries across 5 domains (`working-method`, `tooling`,
  `sap-gui`, `sap-abap`, `sap-data`). One entry per rule with Rule / Why / Break it /
  Seen / Confidence / Evidence, edited in place. Growth is a merge, not an append.
- `corrections.md` is now the **inbox**: ≤240 chars per incident, status
  `open` → `drained`, archived monthly. It is a buffer, not a ledger.
- `lessons.md` is retired; a knowledge entry *is* the lesson. Both old tables are
  kept at `memory/_archive/v0-ledger/` (the 4 rows still marked `open` were
  implemented in ZDEMO01 v11/v12 and are recorded in the card).
- The close-out is a **consolidation gate** with four outcomes (merge / add /
  promote / drop), written into `AGENTS.md`, `config/opencode-AGENTS.md`,
  `memory/README.md` and `templates/AGENTS.md`.
- `memory_check.py` validates the entry schema (fields, confidence values), the
  per-domain cap (12), the entry size (1.2k), the inbox cap (40) and the row/scheme
  budgets. The knowledge check is negative-tested: a missing field fails with exit 1.
- `session_context.py` prints the inbox count and the knowledge inventory per domain
  instead of the corrections list (~2.4k chars brief, 0.8k `--tiny`).
- Project cards and `tool-map.md` now point at knowledge entries instead of
  `lessons.md`.

## v0.4.2 — 2026-11-14

**Tool diet: 211 → 111 tools, 73.3k → 57.9k chars per session.**

- `sap-gui` (59 tools), `playwright` (25) and `sap-docs` (9) moved to on-demand
  (`enabled: false`). `sap-gui` costs nothing extra in workflow: SAP work already
  needs one enable + restart for `ds4-100`.
- `rosa` removed from `opencode.json`. It is the SAP Cloudification Repository MCP
  (`npx @rosa-mcp/server`: Clean Core level, successor lookup, compliance check);
  never used here and the `atc-cloudification` skill covers the job. The exact
  restore snippet is in `memory/tool-map.md` §"Disabled or removed servers".
- `ds4-100` was left enabled in the steady state; both SAP clients are now off, as
  the on-demand rule requires.
- `optional_namespaces` now lists `sap-gui`, `sap-docs`, `playwright` so toggling
  them is not reported as drift.
- Measured after the change: tools 16.1k chars / 111 tools, under the 28k budget.
  The skill catalog (41.7k / 78) is now the only block over budget.

## v0.4.1 — 2026-11-14

**Measure the prompt, not just the memory.**

- `registry_check.py` now reports a **prompt budget**: the injected skill catalog
  (41.7k chars / 78 entries) and tool descriptions (31.5k / 211 tools) against
  budgets of 20k and 28k, with the top namespaces named. Measured on 2026-11-13,
  the two catalogs cost ~73k chars per session — 7x the memory files they replaced.
- `session_context.py --tiny`: light tier in 0.8k chars (project, status, next step,
  one style rule, open-correction count, health only when broken).
- `memory_check.py` also guards the project-card size (budget 9k chars).
- The global `AGENTS.md` SAP section is now rules + a pointer: the 13-line
  enable/disable procedure moved to `memory/tool-map.md` §"SAP on-demand", where it
  is read exactly when SAP work starts (4.99k → 4.42k chars, every session).
- `docs/design.md` records the measured prompt budget per block; `memory/README.md`
  points at it.
- Fixed a variable shadowing bug (`ns`) that broke the full report in v0.4.

## v0.4 — 2026-11-13

**Tiered context loading, and a gate that stops crying wolf.**

- Added `scripts/session_context.py`: one call replaces eight file reads plus two
  scanner runs. It prints the active project's resume card, memory and registry
  health, the open corrections, the curated tool rules from the `digest` block in
  `memory/tool-map.md`, and the size of every file that can be opened on demand.
  Measured **1.8k chars (~450 tokens)** against **26.6k chars** for the previous
  read-everything rule.
- Session start is now tiered (`light` / `task` / `deep`) in the global `AGENTS.md`,
  the workspace `AGENTS.md`, `memory/README.md`, `templates/AGENTS.md`, and
  `docs/design.md`. Nothing was removed from the `deep` tier.
- `registry_check.py` no longer reports designed states as failures:
  - an `optional_namespaces` server (on-demand SAP) with zero tools is a warning,
    not an issue, and is listed as "on-demand, idle (expected)";
  - the tool total is compared with the optional namespaces removed on both sides,
    so connecting/disconnecting SAP is not drift;
  - new assets and stale validations are warnings; only broken things (missing
    path, duplicate name, missing skill reference, missing server/tool, zero tools
    on a non-optional server) fail the gate.
  Result: a healthy idle session now exits `0` instead of `1` with three
  false positives.
- Added `promoted` to the allowed correction statuses in `memory_check.py`.
- Memory lifecycle: a correction keeps `status: open` and is **promoted** (status
  change + pointer), not copied into `lessons.md`; close-out is one batched edit
  per file; closed/promoted rows older than 30 days move to `memory/_archive/`.
- `team-roster.md`: added a delegation cost model — delegate only for read-only
  work of ≥15 tool calls or >5k tokens of output, one SAP GUI actor, at most 2-3
  children, and a brief of five lines plus a pointer.

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
