# fr0ster / mcp-abap-adt v24.0.0 — assessment record

**Status: evaluated, not installed.** No `opencode.json` entry, no npm install, no
SAP call, no credential change. This file is the record; the capability comparison
lives in `docs/mcp-capability-matrix.md`, the still-parked trial in
`docs/plan-fr0ster-evaluation.md`. Do not duplicate the rules from those files.

Evidence re-derived 2026-11-18 from upstream tag `v24.0.0` (`8a9ed53`, published
2026-11-17), its generated tool docs, PR #346 and PR #349; compared with the old
baseline `v23.1.0` / `b29d6ff`. Local facts from `opencode.json` and
`registries/tools-full.json` (363 tools, 2026-11-18).

---

## 1. Numbers, re-derived

| Shape | `v23.1.0` | `v24.0.0` |
|---|---|---|
| Full core (`AVAILABLE_TOOLS.md`) | 292 | **289** |
| High-level (`AVAILABLE_TOOLS_HIGH.md`) | 188 | **188** |
| Read-only (`AVAILABLE_TOOLS_READONLY.md`) | 74 | **73** |
| Compact tools | 40 | **39** |
| Compact read-only half | 17 | **16** |

Full set lost `GetAbapAST`, `GetAbapSemanticAnalysis`, `GetAbapSystemSymbols` and
the full-binary `Batch*` tools; gained `GetObjectDraft`, `GetObjectOutline`,
`DebugBatchAnswers` and three background-run tools. Compact `HandlerSearch` +
`HandlerWhereUsed` became `HandlerSystem` with eight actions.

## 2. Changes that matter here

| Change | Effect |
|---|---|
| Start-time restrictions `--deny-actions`, `--allowed-packages`, `--allowed-requests`, `--denied-tables` / `--allowed-tables` (also `MCP_*`, YAML `restrictions.*`); none by default | A task-scoped instance can be allow-listed. SAP authorization stays the boundary. |
| Data tools opt-in `--enable-data-tools`: `GetSqlQuery`, `GetTableContents`, `HandlerGetData` off on every binary by default | `-ro` shape no longer reads business data unless explicitly enabled. |
| Long reads background-by-default: `GetBackgroundRun`, `ListBackgroundRuns`, `DiscardBackgroundRun`; no `timeout` | A where-used/search call returns a `run_handle`; scorecard needs one extra read. |
| `GetObjectDraft` / compact `HandlerGet part: 'draft'` | New read: whose unactivated draft an object holds. |
| RFC destination states `SAP_ASHOST` + `SAP_SYSNR` or message server, plus `SAP_CLIENT` / `SAP_LANGUAGE`; no `SAP_URL` | A hypothetical RFC trial has a different config shape. |
| Named `--mcp` sessions in memory unless `--unsafe`; a named `.env` still written back with a renewed token | Credential-on-disk risk shrinks for `--mcp`, unchanged for `--env` / `--env-path`. |
| Node 22 or 24 required; machine is `v26.13.1` | Trial blocked by runtime, not capability. |

## 3. Local tool landscape

| Namespace | Tools | Posture |
|---|---|---|
| `ai-dev-ds4-100` | 75 | write, LUF DS4/100 |
| `ai-dev-ds4-900` | 75 | verify, LUF DS4/900 |
| `ai-dev-sus-100` | 75 | write, SUS/100 |
| `arc1-ds4-100` | 8 | read, LUF DS4/100 |
| `arc1-sus-100` | 9 | read, SUS/100 |
| `sap-docs` | 9 | remote docs |
| `open-computer-use`, `windows-mcp`, `browse`, `browser`, `opencode` | 9 / 19 / 18 / 45 / 20 | generic desktop and file tools |

Disabled: `playwright`, `sap-gui`, `ai-dev-gsd-120`, `arc1-gsd-110`.
The same ADT capability appears five times (three ai-dev + two arc1 namespaces).
OpenCode prefixes names `<server>_<tool>`, so there is no wiring collision — only
nondeterministic selection.

## 4. Overlap and conflict analysis

| Local tool | fr0ster equivalent | Overlap | Risk if picked together |
|---|---|---|---|
| `ai-dev-*_get_class`, `get_program`, `get_function`, `get_table`, `get_source` | `GetClass`, `GetProgram`, `GetFunctionModule`, `GetTable`, `GetDdl`, `GetBehaviorDefinition` | high | different client/version → conflicting interpretation |
| `arc1-*_SAPRead` | same read-only set | high | duplicate read, no added confidence |
| `ai-dev-*_grep_objects`, `grep_packages`, `search_object`; `arc1-*_SAPSearch` | `SearchSource` | high | duplicate SAP requests |
| `ai-dev-*_find_references`, `arc1-*_SAPContext` | `GetWhereUsed` | high | different impact sets |
| `ai-dev-*_get_package` | `GetPackageTree` | medium–high | different depth/count |
| `ai-dev-*_run_atc_check` | `RunATC`, `GetATCFindings` | medium–high | different `worklist_id` |
| `ai-dev-*_run_unit_tests` | `GetUnitTestResult` | medium | different `run_id` |
| `ai-dev-*_run_query`, `get_table_contents` | `GetSqlQuery`, `GetTableContents` | high | duplicate data read on different clients |
| — | `GetBackgroundRun`, `SessionOpen`, `SessionClose` | low | no local equivalent; different two-step call pattern |

`SessionOpen` / `SessionClose` are absent from the three generated v24 tool docs
(README points to compact `HandlerSession` and HTTP session state).

Specific risks:

1. **Five copies of one capability** — two engines agreeing is two nondeterministic
   choices, not stronger evidence.
2. **Concurrent writes** — three write-armed ai-dev engines: same object in parallel
   hits ADT lock 423; sequential read-modify-write loses an update silently.
3. **Generic file tools replacing ADT reads** — `opencode` `read`/`glob`/`grep`,
   `windows-mcp` `FileSystem`, `browse`/`browser` can read a local mirror instead
   of live SAP source, producing stale evidence.
4. **Duplicate search and data reads** — no correctness gain, extra SAP load.
5. **Policy asymmetry** — fr0ster v24 leaves data tools off by default; ai-dev
   mounts `run_query` / `get_table_contents` by default.

## 5. Rule mechanisms

fr0ster ships no `agents/` or `skills/` folder in its v24.0.0 root (verified from
GitHub contents); only client-rule samples such as `.clinerules` and `.cursor/`.

Local compensating rules already exist:

- `docs/mcp-orchestration.md` §5 — one object, one writer, one session; verify with
  a different engine only after re-read; never cite two engines for one fact.
- `workspace/memory/tool-map.md` — routing table, same writer rule,
  `tools_now.py --check --expect <ns>` after any toggle.
- global and workspace `AGENTS.md` — SAP on-demand, no passwords in config, ask
  before writing.

Gap: these are prose, not config enforcement. No `*.rules.md` or permission deny
rule is configured.

## 6. Decision and gate

Keep fr0ster absent. Reopen only when a task proves a read that ai-dev + arc1
cannot deliver, and all of these hold: Node 22/24 accepted, AGPL server accepted,
credentials routed through Windows Credential Manager, task-scoped entry with
`enabled: false` and the read-only shape, no `--enable-data-tools`, and an
allow-list via `--allowed-packages` / `--deny-actions`.

## 7. Data/SQL posture change — 2026-11-18

User asked to close `SAP_ALLOW_FREE_SQL` and `SAP_ALLOW_DATA_PREVIEW` before any
fr0ster trial. Added explicit `"false"` for both to the `environment` block of all
five SAP entries in `opencode.json`.

- **arc1**: launcher already set both to `false` without `-AllowDataPreview` /
  `-AllowFreeSql`; posture output confirms `data=false sql=false`. The explicit
  env values are a safeguard, not a behaviour change.
- **ai-dev**: the installed engine has no reference to either variable; its
  `run_query` / `get_table_contents` tools stay mounted. These entries are an
  explicit intent record, not an effective block. Blocking those tools in OpenCode
  needs a permission rule and is **not applied**.

## 8. Re-derive, do not remember

```powershell
curl -fsSL https://raw.githubusercontent.com/fr0ster/mcp-abap-adt/v24.0.0/docs/user-guide/AVAILABLE_TOOLS.md
curl -fsSL https://raw.githubusercontent.com/fr0ster/mcp-abap-adt/v24.0.0/compact/docs/AVAILABLE_TOOLS.md
curl -fsSL https://raw.githubusercontent.com/fr0ster/mcp-abap-adt/v24.0.0/docs/user-guide/ACCESS_RESTRICTIONS.md
python scripts\tools_now.py
```
