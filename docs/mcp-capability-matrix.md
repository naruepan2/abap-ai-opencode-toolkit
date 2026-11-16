# MCP capability matrix — which SAP server owns which job

Three ADT servers claim to cover ABAP work. This document records what each one
actually exposes, so a gap is answered by evidence rather than by adding another
server and hoping the model picks the right tool.

Sources: the repositories as of 2026-11-17 (`fr0ster/mcp-abap-adt` @ `b29d6ff`,
`arc-mcp/arc-1` @ `755a265`, `grknylmz/sap-ai-dev-toolkit`) plus the live tool
catalog of the current session (`registries/tools-full.json`). The fr0ster
figures below were re-derived from its generated tool docs at that commit on
2026-11-17 — `b29d6ff` was still `main` when the check ran.

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
| Tools exposed | **75** (live) | **12** documented / **8** live — the live set is **read-only** | **292** total · **188** high-level · **74** read-only — the compact binary is a separate shape: **28** tools, **17** read-only |
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
- fr0ster: the generated tool docs carry **292** `####` entries
  (`AVAILABLE_TOOLS.md`), **188** in `AVAILABLE_TOOLS_HIGH.md` and **74** in
  `AVAILABLE_TOOLS_READONLY.md`; the categories are Domain, Data Element, Table,
  Table Type, Structure, Message Class, Metadata Extension, Behavior Definition,
  Service Definition and Service Binding. The compact binary takes the object type
  as an argument — `DOMAIN`, `DATA_ELEMENT`, `TABLE`, `STRUCTURE`, `TABLE_TYPE`,
  `DDL` (`compact-readonly-entries/src/handlers/compactReadRoutes.ts:110-132`).

### Corrections to two common assumptions

1. **"arc-1 cannot create domains or data elements"** — false. It has no tool *named*
   `CreateDomain`; the capability lives in `SAPWrite` with `type: "DOMA"` / `"DTEL"`.
   Judging arc-1 by tool names understates it by an order of magnitude.
2. **fr0ster's "👁️ View Management: GetView, CreateView, UpdateView"** — not present in
   its generated tool list (0 matches for `GetView`/`CreateView`/`UpdateView` across all
   three generated docs). The bullet is still in the README (`README.md:273`), and the
   only tool whose name matches `/view/i` is `GetServiceBindingPreviewUrl`. CDS is
   handled as `Ddl`; classic views are not covered.

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

Beyond context, fr0ster adds a **second credential path**. Every authentication it
supports is a *destination* described by env vars; the basic one holds
`SAP_USERNAME` + `SAP_PASSWORD` (`docs/user-guide/AUTHENTICATION.md:11`), and the
words keychain or keyring appear nowhere in that guide. Its browser login
(`@mcp-abap-adt/auth-broker-cli`, `README.md:86`) avoids the password but writes the
session to `<auth-broker-path>/sessions/<name>.env` — still a second place on disk.
The Windows Credential Manager used here knows neither route.

---

## 5. Recommendation

1. **Keep ai-dev + arc-1 + sap-gui, with scoped roles.** ai-dev owns the edit loop,
   the debugger and the frontend/migration jobs; arc-1 owns analysis, DDIC entity
   types, transport lifecycle, abapGit and the data surface. The split is in
   `docs/mcp-orchestration.md` §2.
2. **Close the DDIC gap with arc-1, not with a new server.** Domain, data element and
   table type creation already exist in `SAPWrite`; the launcher is simply not passing
   `-AllowWrites`. That is a per-task switch, not a missing engine.
3. **fr0ster is absent by design, not disabled.** There is no entry for it in
   `opencode.json`, so it cannot connect and it costs nothing. If a task ever needs
   what arc-1 refuses, bring it in as a task-scoped entry with `disabled: true` and
   the read-only shape (`@mcp-abap-adt/core-ro`, or `compact-ro` at 17 tools) — 292
   tools is not worth a permanent slot. Its credentials would have to travel the same
   Windows Credential Manager route as the other engines; its own env vars are a
   second place for a SAP password to exist.
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

# upstream claims
curl -fsSL https://raw.githubusercontent.com/arc-mcp/arc-1/main/README.md
curl -fsSL https://raw.githubusercontent.com/fr0ster/mcp-abap-adt/main/docs/user-guide/AVAILABLE_TOOLS_HIGH.md
```

If a row changes, edit it here. A capability that exists but is undiscoverable is a
documentation bug in this file, not a reason to install another server.
