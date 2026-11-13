# Registries

Machine-readable snapshots will live here. Planned files:

| File | Purpose |
|---|---|
| `agents.json` | agent inventory, owner, editable, scope |
| `skills.json` | skill inventory, source, hash, status |
| `mcp-servers.json` | configured MCP servers and client scope |
| `tools.json` | capability map: preferred / fallback |
| `tools-snapshot.json` | generated from the live tool catalog |

Do not hand-edit generated files in normal use. Update the registry through the
scanner and the approval gate.

Status: placeholder. The scanner is the next milestone.
