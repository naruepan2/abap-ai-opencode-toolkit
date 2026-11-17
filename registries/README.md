# Registries

Machine-readable snapshots of the workspace. Generated and checked by
`scripts/registry_check.py`. See `docs/catalog.md` for the repository-wide map.

## Baseline — committed

Updated only when installed assets change, by `registry_check.py --init` / `--refresh`.

| File | Purpose |
|---|---|
| `skills.json` | every installed `SKILL.md`, with harness, path, owner, hash, description length, status, last validated |
| `agents.json` | every agent, with harness, owner, editable flag, declared skills, hash |
| `mcp-servers.json` | configured MCP servers (OpenCode and Copilot), enabled state, command kind, URL host |
| `tools.json` | baseline of the live tool catalog: total, namespaces, and tool IDs |

## Live snapshots — generated, git-ignored

Written by `plugins/tool-snapshot/`. They carry local paths, so they never enter git.

| File | Purpose |
|---|---|
| `tools-snapshot.json` | latest captured catalog summary; compared with `tools.json` |
| `tools-full.json` | latest full tool list (`id`, `name`, `namespace`, `description`) |

The check report lives in `workspace/memory/reports/registry-report.md`.

## Rules

- `tools-snapshot.json` and `tools-full.json` are written by the OpenCode plugin.
- Do not hand-edit generated rows unless you are correcting metadata.
- `status` and `last_validated` belong to the registry, not to the scanner.
- Vendor rows are read-only; personal rows end with `-by-pongg`.
- No credentials, no environment variables, no command arguments are stored.
