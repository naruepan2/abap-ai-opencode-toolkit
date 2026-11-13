# Scripts

## `registry_check.py`

Read-only scanner for skills, agents, MCP servers, and the tool snapshot. It never
enables a server, promotes a skill, or edits an agent. Requires Python 3.8+; uses
only the standard library.

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

`registries/tools-snapshot.json` and `registries/tools-full.json` are written by
the OpenCode plugin at `plugins/tool-snapshot`. The plugin calls `ctx.tool.list()`
in the OpenCode server, so it sees MCP and built-in tools without a manual step.

The scanner compares the full tool IDs with the baseline in `registries/tools.json`
and reports new or missing tools. Run `--refresh` only when you want to accept the
new list into the baseline.

## Safety

The scanner only reads local files. It does not connect to SAP, call MCP tools, or
write outside `registries/` and `memory/reports/`.
