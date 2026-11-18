# MCP capability matrix — which SAP server owns which job

Three ADT servers claim to cover ABAP work. This document records what each one
actually exposes, so a gap is answered by evidence rather than by adding another
server and hoping the model picks the right tool.

Sources: the repositories (`fr0ster/mcp-abap-adt` @ `8a9ed53`, tag `v24.0.0`;
`arc-mcp/arc-1` @ `755a265`, `grknylmz/sap-ai-dev-toolkit`) plus the live tool
catalog of the current session (`registries/tools-full.json`). The fr0ster
figures were re-derived from its generated tool docs at `v24.0.0` on 2026-11-18
and diffed against the previous baseline `v23.1.0` / `b29d6ff`. The ai-dev and
arc-1 figures were **not** re-measured in this pass.

---

## 1. What happens when every server is enabled

Short answer: they all load, the model picks, and nothing arbitrates.

| Question | Answer |
|---|---|
| Do duplicate tools break the config? | No. OpenCode names every tool `<server>_<tool>` (Code Mode: `tools.<server>.<tool>`), so two servers never collide on a name. |
| Can the model choose on its own? | Yes — that is the only mechanism. Selection is driven by name + description, not by a router, priority, or a "best provider" rule. |
| Is it deterministic? | No. The same question can route to a different engine twice. That is the actual risk, not an error message. |
| Is it free? | No. Every connected server adds its namespace index, its tool catalog, and its server instructions to the context. OpenCode's own docs: *"MCP tools consume model context, so add only the servers you need."* |
| Can a server stay configured but silent? | Yes, three levels: `disabled: true` (no connection), `/mcps` disconnect (session only), or a permission rule that denies `server_*` without disconnecting. |

Under Code Mode (default) the full schema set is not pre-loaded; the model sees a
partial catalog and reaches the rest through `search`. So availability is not
discoverability — this session needed a `search` call to find DDIC tools that were
installed all along.

**The rule that follows:** one object, one writer, one session, and never mix
evidence for the same fact from two engines. Two engines agreeing is not stronger
evidence; it is two nondeterministic choices that happened to land together. The
wording and its evidence live in `docs/mcp-orchestration.md` §5.

---

## 2. The three servers at a glance

| | ai-dev (vsp) | arc-1 | fr0ster mcp-abap-adt |
|---|---|---|---|
| Tools exposed | **75** (live) | **12** documented / **8** live — the live set is **read-only** | **289** total · **188** high-level · **73** read-only (was 292/188/74 at `v23.1.0`) — the compact shape is **39** tools, **16** read-only (was 40/17) |
| Design | one tool per action | **one tool per verb**, object type as an argument | both: per-type tools *and* a compact multiplexed binary |
| Read ABAP source | ✔ | ✔ | ✔ |
| Write / activate | ✔ | ✔ | ✔ |
| Transports | ✔ | ✔ | ✔ |
| AUnit / ATC / dumps / profiler | ✔ | ✔ (SAPDiagnose) | ✔ (incl. debugger + profiler traces) |
| Git (abapGit / gCTS) | list only | ✔ SAPGit | ✖ |
| ABAP lint (offline) | ✔ | ✔ SAPLint | ✖ — syntax check only, as `Check<Type>`; no lint or format tool |
| Agents + skills shipped | **24 agents, 32 skills** | skills + commands | ✖ — tooling only: the repo root holds no `agents/` or `skills/` folder |
| CLI fallback | ✔ | ✔ | ✔ |

The count column is misleading on its own: arc-1's 12 tools carry more object types
than ai-dev's 75, because arc-1 multiplexes. Compare capabilities, not tool names.

---

## 3. DDIC matrix — the actual gap

Legend: **C** create · **R** read · **U** update · **A** activate · **D** delete · **V** versions · **–** absent

| Object | ai-dev (75 tools) | arc-1 (SAPWrite/SAPRead) | fr0ster |
|---|---|---|---|
| Domain (DOMA) | **–** | **C R U A** (create gated by ADT endpoint discovery) | C R U A D |
| Data element (DTEL) | **–** | **C R U A** | C R U A D |
| Transparent table | **C R U A** (`create_table`, `update_table`) | C R U A D | C R U A D |
| Structure | **R** only (`get_structure`) | C R U A (`TABL/DS`, alias `STRU/DS`) | C R U A D V |
| Table type (TTYP) | **–** | **C R** (create gated: `/ddic/tabletypes/` must exist, FEAT-65) | C R U A D V |
| Classic view / SHLP / MSAG | view **–**, search help **R**, message class **–** | SHLP **R** (metadata only), MSAG **C R U A** | MSAG **C R U D** (no activate); view/SHLP **no tool** |
| CDS / DCL / DDLX / BDEF / SRVD / SRVB | ✔ full (incl. publish) | ✔ full (incl. publish) | ✔ (DDL + DDLX + BDEF + SRVD + SRVB); **DCL –** |

Evidence, so the table can be re-checked instead of trusted:

- ai-dev: the live 75-tool list contains no `*domain*`, `*data_element*`, or
  `*table_type*` tool; `create_object` advertises PROG/CLAS/INTF/INCL/FUGR/DDLS/BDEF/
  SRVD/SRVB/DEVC, and `write_source` advertises TABL **updates** only.
- arc-1: `src/handlers/write.ts` L207-215 gates `TTYP` and `DOMA` create on endpoint
  discovery; `src/handlers/object-types.ts` carries `DOMA`, `DTEL`, `TTYP`, `VIEW`,
  `SHLP`, `MSAG`, `ENQU`, `ENHO`; the README tool table lists `DOMA`, `DTEL`, `MSAG`
  inside SAPWrite.
- fr0ster: re-derived from the generated tool docs at `v24.0.0` — **289** `####`
  entries (`AVAILABLE_TOOLS.md`), **188** (`AVAILABLE_TOOLS_HIGH.md`) and **73**
  (`AVAILABLE_TOOLS_READONLY.md`); the compact doc states **39** tools, **16**
  read-only. Against `v23.1.0` the full set lost `GetAbapAST`,
  `GetAbapSemanticAnalysis`, `GetAbapSystemSymbols` and the full-binary `Batch*`
  tools, and gained `GetObjectDraft`, `GetObjectOutline`, `DebugBatchAnswers` and
  three background-run tools; high-level is unchanged. Compact `HandlerSearch` +
  `HandlerWhereUsed` became one `HandlerSystem` with eight actions. The categories
  are still Domain, Data Element, Table, Table Type, Structure, Message Class,
  Metadata Extension, Behavior Definition, Service Definition and Service Binding;
  the compact binary still takes the object type as an argument.

### Corrections to two common assumptions

1. **"arc-1 cannot create domains or data elements"** — false. It has no tool *named*
   `CreateDomain`; the capability lives in `SAPWrite` with `type: "DOMA"` / `"DTEL"`.
   Judging arc-1 by tool names understates it by an order of magnitude.
2. **fr0ster's "👁️ View Management: GetView, CreateView, UpdateView"** — still not in
   its generated tool list at `v24.0.0` (0 matches for those three names across all
   three generated docs; re-checked 2026-11-18). The bullet remains in the README,
   and the only tool whose name matches `/view/i` is `GetServiceBindingPreviewUrl`.
   CDS is handled as `Ddl`; classic views are not covered.

### Capability vs configuration

The live arc-1 instance exposes eight tools — `SAPRead`, `SAPSearch`, `SAPContext`,
`SAPManage`, `SAPNavigate`, `SAPLint`, `SAPDiagnose`, `SAPTransport`. `SAPWrite`,
`SAPActivate`, `SAPQuery` and `SAPGit` are **not mounted**.

The cause is in the launcher, not the code: `sap-mcp.ps1` sets
`SAP_ALLOW_WRITES=false` unless it is started with `-AllowWrites`, and leaves
`SAP_ALLOW_DATA_PREVIEW`, `SAP_ALLOW_FREE_SQL` and `SAP_ALLOW_GIT_WRITES` off. Those
four flags are exactly what mounts the four missing tools
(`src/handlers/query-tool.ts:36-44` returns no tool at all when no data action is
enabled). So: the code can create `DOMA` / `DTEL` / `TTYP`, but *this* arc-1 cannot.

A missing tool on the wire is evidence about the configuration, not about the
codebase — check which of the two you are looking at before installing a replacement
server. `python scripts/tools_now.py` now prints that posture per server; the model
behind it is in `docs/mcp-orchestration.md`.

### What v24.0.0 changed (2026-11-18)

The major bumps the version from 23.x; the counts above already use the new
numbers. The changes that matter to this evaluation:

| Change | Upstream evidence | Effect here |
|---|---|---|
| Start-time restrictions: `--deny-actions`, `--allowed-packages`, `--allowed-requests`, `--denied-tables` / `--allowed-tables` (also `MCP_*` and YAML `restrictions.*`); none by default | README "Access restrictions"; `docs/user-guide/ACCESS_RESTRICTIONS.md` (PR #349) | A task-scoped instance can be allow-listed to a package/request/table set. SAP authorization is still the boundary. |
| Data tools opt-in: `GetSqlQuery`, `GetTableContents`, `HandlerGetData` off on **every** binary by default, `-ro` included | README "The data tools: off unless enabled"; `HandlerGetData` in the compact doc | The read-only shape no longer reads business data unless explicitly enabled — matches our no-data-preview rule. |
| Long reads background-by-default: `GetBackgroundRun` / `ListBackgroundRuns` / `DiscardBackgroundRun`; no `timeout` argument | README "Long reads run in the background"; `docs/MIGRATION-24.0.md` | A where-used/search call returns a `run_handle`; a scorecard must count the extra read. |
| New read `GetObjectDraft` (compact `HandlerGet` `part: 'draft'`) — whose unactivated draft an object holds | PR #349; generated tool docs | Not available from the current two engines. |
| RFC destinations state their own address (`SAP_ASHOST` + `SAP_SYSNR`, or message server, plus `SAP_CLIENT` / `SAP_LANGUAGE`); no `SAP_URL` | README "For RFC connection"; `docs/MIGRATION-24.0.md` | A hypothetical RFC trial needs a different config shape; our HTTP/TLS findings stand. |
| Named `--mcp` sessions stay in memory unless `--unsafe`; a named `.env` is still written back with a renewed token | README "Command-Line Options" | Credential-on-disk risk shrinks for `--mcp`, unchanged for `--env` / `--env-path`. |
| Node 22 or 24 still required; this machine remains `v26.13.1` | README "Getting Started"; `node -v`, 2026-11-18 | A trial is still blocked by the runtime, not by a capability. |
| Compact `HandlerSearch` + `HandlerWhereUsed` → `HandlerSystem` (8 actions) | PR #346 (D25); compact tool docs | Any future config or scorecard must use the new tool name. |

---

## 4. Cost of adding a fourth engine

Measured by the check, not by hand: `registry_check.py --check --brief` prints one line
per session. On 2026-11-16, with fr0ster still off:

```
skills 19.8k chars (30)  +  tools 38.7k chars (269)  =  58.5k chars per session
```

Read the current line rather than this one; the numbers move with every server and
skill you add. That 38.7k is the **catalog text**, i.e. the ceiling. Code Mode trims the recurring
cost to a namespace index plus `search` results, so the real per-turn delta is
smaller — and it is not zero. `registry_check.py --check --brief` prints the same
line before and after a change; that is the honest way to measure an addition.

Beyond context, fr0ster adds a **second credential path**, though v24.0.0 narrowed
it. A named `--mcp` destination keeps its session **in memory by default** —
`--unsafe` is what writes it to `<auth-broker-path>/sessions/<name>.env`. A `.env`
named with `--env` / `--env-path` is still read **and written back** with a renewed
token whatever `--unsafe` says, and the basic one holds `SAP_USERNAME` +
`SAP_PASSWORD`. The words keychain or keyring appear nowhere in its authentication
guide (0 matches at `v24.0.0`). The Windows Credential Manager used here knows
neither route.

---

## 5. Recommendation

1. **Keep ai-dev + arc-1 + sap-gui, with scoped roles.** ai-dev owns the edit loop,
   the debugger and the frontend/migration jobs; arc-1 owns analysis, DDIC entity
   types, transport lifecycle, abapGit and the data surface. The split is in
   `docs/mcp-orchestration.md` §2.
2. **Close the DDIC gap with arc-1, not with a new server.** Domain, data element and
   table type creation already exist in `SAPWrite`; the launcher is simply not passing
   `-AllowWrites`. That is a per-task switch, not a missing engine.
3. **fr0ster is still absent by design, not disabled.** No `opencode.json` entry,
   no global install (last checked 2026-11-17), and Node 22/24 required versus
   `v26.13.1` here — so it cannot connect and costs nothing. v24.0.0 makes a future
   trial cheaper and tighter: `compact-ro` is **16** tools, data reads are off by
   default, and start-time allow-lists can scope it to a package, request or table
   set. That does not change the gate: credentials would still have to travel the
   same Windows Credential Manager route, and the roles above already cover the
   work. The full record, including the local tool-overlap analysis, is
   `docs/fr0ster-v24-assessment.md`. Re-open `docs/plan-fr0ster-evaluation.md` only
   if a task proves a real gap.
4. **One object, one writer, one session.** Readers may overlap freely; a second engine
   writes an object only after the first is done and it has been re-read. Record which
   engine produced each piece of evidence. Details and evidence:
   `docs/mcp-orchestration.md` §1 and §5.

---

## 6. Keeping this document true

Re-derive, do not remember:

```powershell
# live catalog of what is actually connected
python scripts\registry_check.py --check --brief

# upstream claims — pin the fr0ster tag; main moves
curl -fsSL https://raw.githubusercontent.com/arc-mcp/arc-1/main/README.md
curl -fsSL https://raw.githubusercontent.com/fr0ster/mcp-abap-adt/v24.0.0/docs/user-guide/AVAILABLE_TOOLS.md
curl -fsSL https://raw.githubusercontent.com/fr0ster/mcp-abap-adt/v24.0.0/docs/user-guide/AVAILABLE_TOOLS_HIGH.md
curl -fsSL https://raw.githubusercontent.com/fr0ster/mcp-abap-adt/v24.0.0/docs/user-guide/AVAILABLE_TOOLS_READONLY.md
curl -fsSL https://raw.githubusercontent.com/fr0ster/mcp-abap-adt/v24.0.0/compact/docs/AVAILABLE_TOOLS.md
curl -fsSL https://raw.githubusercontent.com/fr0ster/mcp-abap-adt/v24.0.0/docs/user-guide/ACCESS_RESTRICTIONS.md
```

If a row changes, edit it here. A capability that exists but is undiscoverable is a
documentation bug in this file, not a reason to install another server.
