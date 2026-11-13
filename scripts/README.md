# Scripts

Planned:

- `registry_check.py` — scan skills, MCP config, and the live tool snapshot;
  compare with `registries/*.json`; write `memory/reports/registry-report.md`.
- `snapshot_tools.py` — helper that accepts a tool catalog export and writes
  `registries/tools-snapshot.json`.

The scanner is read-only. It never enables an MCP server, promotes a skill, or
edits an agent.

Status: placeholder. Next milestone after the bootstrap commit.
