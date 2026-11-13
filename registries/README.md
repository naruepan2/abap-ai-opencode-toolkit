# Registries

Machine-readable snapshots of the workspace. Generated and checked by
`scripts/registry_check.py`.

| File | Purpose |
|---|---|
| `skills.json` | every installed `SKILL.md`, with harness, path, owner, hash, description length, status, last validated |
| `agents.json` | every agent, with harness, owner, editable flag, declared skills, hash |
| `mcp-servers.json` | configured MCP servers (OpenCode and Copilot), enabled state, command kind, URL host |
| `tools.json` | baseline of the live tool catalog: total and namespace counts |
| `tools-snapshot.json` | latest captured tool catalog snapshot; compared with `tools.json` |

## Rules

- Do not hand-edit generated rows unless you are correcting metadata.
- `status` and `last_validated` belong to the registry, not to the scanner.
- Vendor rows are read-only; personal rows end with `-by-pongg`.
- No credentials, no environment variables, no command arguments are stored.
