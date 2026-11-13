# Registry report

Generated: 2026-11-13T19:13:26+00:00

## Summary

| Area | Count | Issues | Warnings |
|---|---|---|---|
| Skills | 180 | 0 | 4 |
| Agents | 23 | 0 | 0 |
| MCP servers | 14 | 0 | 0 |
| Tools | 170 | 0 | 0 |

## Skills by harness

- agents: 47
- claude: 30
- copilot: 25
- opencode: 78

## New skills

_None._

## Missing skill paths

_None._

## Duplicate skill names within a harness

_None._

## Skill descriptions over budget (vendor >1000, personal >500)

- `abap-cloud-migration` (opencode, vendor) — 1014 chars
- `badi-enhancement` (opencode, vendor) — 1077 chars
- `sap-integration-wiki` (opencode, vendor) — 1006 chars
- `sap-support-case` (opencode, vendor) — 1221 chars

## Stale or unvalidated skills (>90 days)

_None._

## Agents referencing missing skills

_None._

## New agents

_None._

## MCP servers

| Server | Harness | Enabled | Tools | Note |
|---|---|---|---|---|
| `browse` | opencode | yes | 18 |  |
| `playwright` | opencode | no | 0 |  |
| `open-computer-use` | opencode | yes | 9 |  |
| `windows-mcp` | opencode | yes | 19 |  |
| `sap-gui` | opencode | no | 59 |  |
| `sap-docs` | opencode | no | 0 |  |
| `gsd-120` | opencode | no | 0 |  |
| `ds4-100` | opencode | no | 0 |  |
| `ds4-900` | opencode | no | 0 |  |
| `com.figma.mcp/mcp` | copilot | yes | n/a |  |
| `io.github.ChromeDevTools/chrome-devtools-mcp` | copilot | yes | n/a |  |
| `io.github.SAP/fiori-mcp-server` | copilot | yes | n/a |  |
| `io.github.UI5/mcp-server` | copilot | yes | n/a |  |
| `arc-1` | copilot | yes | n/a |  |

## New MCP servers

_None._

## Missing MCP servers

_None._

## Enabled MCP servers with zero tools

_None._

## On-demand servers idle (expected, not an issue)

_None._

## Tool snapshot changes

_None._

## New tools

_None._

## Missing tools

_None._

## Prompt budget

- skills (opencode): 41748 chars of description across 78 entries — budget 20000
- tools: 26525 chars of description across 170 tools — budget 28000

## Prompt budget notes

- skill catalog is 41748 chars over budget 20000 (78 skills); park unused skills
- config disables sap-gui but the running catalog still exposes it — restart the opencode service (the daemon), not the window

## Notes

- This report is read-only; it changes nothing.
- `status` and `last_validated` are owned by the registry, not by the scanner.
- Zero tools can mean the server is disabled, failed to load, or needs a session restart.
