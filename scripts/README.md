# Scripts

## `registry_check.py`

Read-only scanner for skills, agents, MCP servers, and the tool snapshot. It never
enables a server, promotes a skill, or edits an agent.

```bash
# one-time baseline (writes registries/*.json)
python scripts/registry_check.py --init

# merge newly discovered items into the existing registries
python scripts/registry_check.py --refresh

# compare and write memory/reports/registry-report.md
python scripts/registry_check.py --check

# short summary for a session start
python scripts/registry_check.py --check --brief
```

Exit code is `0` when there are no issues, `1` when the report has issues. That
is a report signal, not a crash.

## Tool snapshot

`registries/tools-snapshot.json` is a compact namespace count from the live
OpenCode catalog (total tools + tools per namespace). It is captured outside this
script because MCP tool enumeration needs the live agent session.

Update it when the MCP configuration changes, then run `--check` again.

## Safety

The scanner only reads local files. It does not connect to SAP, call MCP tools, or
write outside `registries/` and `memory/reports/`.
