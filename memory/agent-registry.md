# Agent & skill registry

> Owner = who may edit. Vendor = read-only. Never edit a vendor file in place.
> If a vendor agent needs different behavior, create a personal wrapper or a new
> `*-by-pongg` agent/skill instead.

## Copilot agents (`~/.copilot/agents`)

| Agent | Owner | Editable | Scope |
|---|---|---|---|
| abap-developer-by-pongg | Pongg | ✅ yes | ABAP development (personal) |
| sap-abap-reverse-engineer-by-pongg | Pongg | ✅ yes | Read-only ABAP reverse engineering |
| sap-se38-report-tester-by-pongg | Pongg | ✅ yes | SE38 report testing (read-only) |
| sap-st22-dump-analysis-by-pongg | Pongg | ✅ yes | ST22 dump analysis |
| abap-developer | vendor | ❌ no | ABAP development |
| abap-runtime-debugger | vendor | ❌ no | Runtime diagnosis |
| hana-cloud-hdi-specialist | vendor | ❌ no | HANA Cloud / HDI |
| rap-service-developer | vendor | ❌ no | RAP services |
| sap-integration-architect | vendor | ❌ no | Integration architecture |
| sap-integration-developer | vendor | ❌ no | Integration delivery |
| sap-solution-architect | vendor | ❌ no | Solution architecture |

## OpenCode agents (`~/.config/opencode/agents`)

| Agent | Owner | Editable | Scope |
|---|---|---|---|
| abap-developer | vendor | ❌ no | ABAP development |
| abap-runtime-debugger | vendor | ❌ no | Runtime diagnosis |
| hana-cloud-hdi-specialist | vendor | ❌ no | HANA Cloud / HDI |
| rap-service-developer | vendor | ❌ no | RAP services |
| sap-integration-architect | vendor | ❌ no | Integration architecture |
| sap-integration-developer | vendor | ❌ no | Integration delivery |
| sap-solution-architect | vendor | ❌ no | Solution architecture |

> OpenCode has no personal agent yet. To add one, create
> `~/.config/opencode/agents/<name>-by-pongg.md`. Do not edit the seven above.

## Skill sources

| Source | Location | Editable |
|---|---|---|
| arc-1 | `~/.agents/skills`, `~/.config/opencode/skills` | ❌ vendor |
| mattpocock/skills | `~/.agents/skills` | ❌ vendor |
| caveman | `~/.agents/skills` | ❌ vendor |
| ponytail | `~/.agents/skills` | ❌ vendor |
| SAP domain skills | `~/.config/opencode/skills` | ❌ vendor |
| new local skills | `~/.config/opencode/skills/<name>` | ✅ Pongg (new only) |

## Change policy

1. New file/draft: allowed.
2. Edit an existing `-by-pongg` agent: propose + wait for approval.
3. Edit a vendor agent/skill: never. Wrap or fork into a personal file.
4. Every approved change needs: reason, evidence, date, and a test on a real task.
