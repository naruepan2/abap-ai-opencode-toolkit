# Team roster (OpenCode)

> The main agent is the team lead. Subagents are specialists. The lead owns the
> final answer and writes memory; subagents return evidence, not conclusions.

## Lead

- **Main agent** — plan, decompose, delegate, verify, own the final answer,
  write `memory/`.

## Specialists

| Agent | Best for | Not for | When to delegate |
|---|---|---|---|
| `abap-developer` | ABAP implementation, fixes, validation, transport preparation | Runtime dump forensics | A bounded code change with a clear target |
| `abap-runtime-debugger` | Dumps, runtime failures, performance symptoms | New feature design | A failure needs evidence from logs/source |
| `rap-service-developer` | RAP BO, behavior, projections, service bindings | Classic report work | A RAP service is created or changed |
| `sap-solution-architect` | Standard API analysis, Clean Core, solution design | Line-level coding | The approach or FS is unclear |
| `sap-integration-architect` | Integration Suite design | ABAP coding | CPI/APIM design is needed |
| `sap-integration-developer` | Integration delivery | ABAP coding | An approved integration plan is executed |
| `hana-cloud-hdi-specialist` | HANA Cloud / HDI / CAP | ABAP runtime | HANA artifacts are involved |
| `explore` | Fast codebase search | Deep implementation | Finding files, symbols, callers |
| `general` | Independent verification, cross-cutting work | Specialized SAP design | A second pair of eyes is needed |

## Delegation rules

1. Brief: goal, context, constraints, target, evidence required, output format,
   stop conditions.
2. One owner per file or object. Never parallel-write the same artifact.
3. Read-only tasks may run in parallel; write tasks are serialized.
4. Subagents return: summary, evidence, files touched, open questions,
   confidence.
5. The lead verifies before accepting. A subagent claim is not a fact until the
   evidence is checked.
6. Subagents do not write `memory/`; they return lessons to the lead.

## Routing and fallback

| Task | Primary | Fallback | Manual |
|---|---|---|---|
| ABAP method change | `abap-developer` | `general` + `abap-development` skill | user |
| Dump / ST22 | `abap-runtime-debugger` | `general` + `sap-troubleshooting` | SAP GUI ST22 |
| FS gap / design | `sap-solution-architect` | `general` + FS docs | user |
| Where-used | `explore` | `general` | SE11 / ADT |
| Independent review | `general` | main agent | user |

If the primary is unavailable, use the declared fallback. If there is no
fallback, stop and ask.
