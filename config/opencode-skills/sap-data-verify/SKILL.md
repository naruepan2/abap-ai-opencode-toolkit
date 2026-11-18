---
name: sap-data-verify
description: Verify that an ABAP program/report/transaction or Fiori-OData app processes and displays data correctly by reading real rows via ARC-1, Clean-Core-first. Prefer C1/C2-released CDS views (e.g. I_SalesDocument) over raw tables (VBAK); check release state with SAPRead(type=API_STATE). Freestyle SQL (SAPQuery) needs SAP_ALLOW_FREE_SQL=true; table/CDS preview (SAPRead TABLE_CONTENTS/TABLE_QUERY) needs SAP_ALLOW_DATA_PREVIEW=true. If a gate is closed, STOP, explain both flags, and ask whether to enable one or both before reading data. Use to check data behind a program, verify ALV/report or Fiori output against the database, compare rows with the screen, or validate totals.
argument-hint: [program/table/CDS name] [suspect value or key]
---

# SAP Data Verification — Clean-Core-First (read-only)

Read logic → derive expected output → read actual rows → compare → report with evidence.
**Strictly read-only; never enables flags itself; Clean Core by default.** Respond in the
user's language. Client config/restart: see the appended Appendix (V = VS Code, O = OpenCode).

## 0. Safety (non-negotiable)
1. SELECT only. No DML/DDL/native SQL/`CALL`/`SUBMIT`; one statement; no `INTO`/`APPENDING`/
   `PACKAGE SIZE`/`UP TO … ROWS` (ARC-1 appends the row cap).
2. Never enable flags yourself. Prepare the exact env change; apply only with explicit
   consent; restart required. Shared/BTP server → hand to admin.
3. Respect every deny layer: `SAP_BLOCKED_DATA_SOURCES`, `SAP_DENY_ACTIONS`, CDS DCL, SAP
   auth. Never suggest disabling a control to make a query run.
4. Built-in gated tools only. `Custom_*` plugins can raw-GET **outside** the data gates —
   never route around a closed gate through them.
5. **Clean Core:** prefer released APIs; never use `noAPI` patterns (e.g. `RFC_READ_TABLE`-
   style raw dumps) or unreleased objects when a released successor exists. Minimize and
   mask personal/credential data; no bulk extracts into chat.
6. PROD: prefer DEV/QA, tight WHERE + small maxRows; note SAP API Policy FAQ Q33 (a
   technical flag is not a policy allowance; integration should use published business APIs).
7. Empty result ≠ no data (client/DCL/exit/filter). Code ≠ spec: requirement/KTD first;
   without one, report "matches code", not "correct".

## 1. Gates & capability model
| Capability | Call | Server flag (default false) | HTTP scope |
|---|---|---|---|
| Freestyle ABAP SQL | `SAPQuery(action="sql", sql, maxRows)` | `SAP_ALLOW_FREE_SQL=true` | `sql` (⇒`data`) |
| Unfiltered sample | `SAPRead(type="TABLE_CONTENTS", name, maxRows)` | `SAP_ALLOW_DATA_PREVIEW=true` | `data` |
| Structured table/CDS query | `SAPRead(type="TABLE_QUERY", name, columns, where, maxRows)` | `SAP_ALLOW_DATA_PREVIEW=true` | `data` |
| Long text / SLG1 log | `SAPQuery(action="long_text"/"application_log")` | `SAP_ALLOW_DATA_PREVIEW=true` | `data` |
| odata_perf / authorization_trace | `SAPDiagnose(...)` | `SAP_ALLOW_DATA_PREVIEW=true` | `data` |
| Source/search/deps/DCLS/API_STATE/dumps | `SAPRead`/`SAPSearch`/`SAPContext`/`SAPDiagnose` | none | `read` |

- Permission = **server flag AND user scope AND SAP auth**. SAP 403 after flags on = auth
  (SU53), not flags. `FREE_SQL` alone does **not** unlock TABLE_* (separate flag) → for full
  verification recommend **both**.
- Reads are never package-gated; SAP auth (`S_TABU_NAM`/`S_TABU_DIS`/`S_ADT_RES`) + CDS DCL
  govern reads. DCL applies at the SQL **entry-point entity**, not inherited from base views.
- Backend: preview 7.40 SP05; SQL console 7.40 SP08; TABLE_QUERY on CDS 752+. TABLE_CONTENTS
  = DDIC endpoint; SAPQuery **and TABLE_QUERY** = freestyle endpoint. Flags read at startup.
- `maxRows` default 100, clamp 10,000; 2 MiB cumulative/call (`DATA_RESPONSE_TOO_LARGE`);
  ~2 concurrent data calls/process → run data queries **sequentially**.

## 2. Phase 0 — gate check (always first; probe, don't ask for flag values)
0a. Preflight `SAPRead(type="SYSTEM")` (returns `user` = whose auth applies). On failure
    stop; startup auth preflight 401/403 blocks ALL tools → fix credentials + restart.
    Optional `SAPRead(type="COMPONENTS")` for release.
0b. Schema signal: `SAPQuery` absent / TABLE_* absent from SAPRead enum → gate closed.
0c. **Clean-Core probes** (released CDS, tiny):
```
SAPRead(type="TABLE_QUERY", name="I_Currency", maxRows=1)      # preview gate
SAPQuery(action="sql", sql="SELECT COUNT(*) AS CNT FROM I_Currency", maxRows=1)  # SQL gate
```
Fallback only if the backend lacks CDS preview (404/unsupported): `TABLE_CONTENTS T000
maxRows=1` — label it a **technical connectivity probe, not a data-access pattern** (T000
is not released for direct use). If the probe source is blocklisted, ask admin which
released sources are permitted.

| Result fragment | Layer | Action |
|---|---|---|
| success | open | proceed |
| `allowDataPreview=false` / `allowFreeSQL=false` | flag OFF | §3 ask |
| `Insufficient scope: 'data'/'sql'` | scope missing | admin grants `viewer-data`/`viewer-sql`/`developer-sql` or BTP `ARC-1 Data Viewer`/`Viewer + SQL` |
| SAP 403 / no authorization | SAP role | SU53 → PFCG (`S_TABU_NAM`/`S_TABU_DIS`/`S_ADT_RES`); try a released alternative |
| `DATA_SOURCE_BLOCKED`/`DATA_LINEAGE_UNRESOLVED`/`DATA_SQL_UNSUPPORTED`/`DATA_POLICY_UNAVAILABLE` | blocklist (gate OPEN) | respect; provable/permitted source or stop |
| 404 on /datapreview/… | backend too old | fallback / report prerequisite |

Matrix: both open → full; preview-only → per-table reads (ask to add SQL for joins/totals);
SQL-only → SAPQuery (TABLE_* stays closed); both closed → **STOP §3**. Source-only analysis
may run, labeled "code-only". Re-probe each task and after any config change.

## 3. Gate closed → inform + ask (do not proceed)
State what was detected; offer **A** preview only, **B** free SQL only, **C** both
(recommended) — explain each enables what, that both stay read-only, and SAP auth/DCL still
apply. Give the exact env edit + restart from the Appendix. Wait for the choice; if declined,
offer code-only analysis and state what cannot be verified. After change+restart → re-probe.

## 4. Clean Core source selection (the heart)
Levels: **A** released APIs only (ABAP Cloud, cloud-ready) · **B** "Classic API"
(Cloudification Repository; stable) · **C** unclassified (conditional, may change per
release) · **D** `noAPI`/modifications (not clean core — never).

Ladder for every data source:
1. **Released CDS view / API first (Level A).** Find candidates via `SAPSearch` (`I_*`/`C_*`),
   the program's own CDS stack, or `SAPContext(action="impact", type="DDLS")`. Confirm:
   `SAPRead(type="API_STATE", name="<view>")` → contract **C1/C2 = released**; if a
   **successor** is reported, use it. Read fields with `SAPRead(type="DDLS", include="elements")`
   and row security with `SAPRead(type="DCLS")`.
2. **Classic table only as a flagged exception** (Level C/D risk) when no released view
   covers the need, or a like-for-like comparison against a classic program requires it.
   Record the justification; prefer the released successor if one exists.
3. Never `noAPI`/modification patterns; never raw dumps.

Semantics: released CDS uses camelCase aliases (`SalesDocument`≠`VBELN`,
`TotalNetAmount`+`TransactionCurrency`), carries currency/quantity semantics, derivations and
DCL — rows may legitimately differ from the raw table. When verifying a **classic** program
that reads `VBAK` directly, prefer the released view; if semantics diverge, do the classic
read as a **justified exception** and say so. Optional governance:
`SAPDiagnose(action="atc", type, name, variant="<cloud-readiness variant>")` to classify the
program's own API usage (variant is system-dependent; check `atc_variants`).

## 5. Phase 1 — expectation from code (no flags needed)
Collect object, output to verify, keys, system/client. TCODE→`SAPRead(TRAN)`;
`SAPContext(action="deps")`→KTD+contracts; find sources via
`SAPRead(PROG, grep="SELECT|FROM|JOIN|SUM|COUNT")`, CLAS `method="*"`→bodies,
FUGR `expand_includes=true`, `SAPSearch(source_code)` (751+); prefer
`SAPSearch(tadir_lookup)` over long TADIR IN-lists. Fiori: SRVB→SRVD→DDLS. Freshness:
`[cached:revalidated]`; non-PP instances may serve a draft ~120 s post-activation →
`force_refresh=true`; check `INACTIVE_OBJECTS`/`object_state` for impossible results.
Output: expectation table (key → expected → requirement/code → source+filter+aggregation).

## 6. Phase 2 — read data (cheapest first; released source per §4)
| Need | Call | Gate |
|---|---|---|
| sample | TABLE_CONTENTS maxRows=20 | preview |
| filtered rows+columns | **TABLE_QUERY** (preferred single-source) | preview |
| JOIN/COUNT/SUM/GROUP BY/subquery | SAPQuery sql | free SQL |
| count before fetch | SAPQuery `SELECT COUNT(*)` | free SQL |
| program log / long text | SAPQuery application_log (check schema) / `long_text, longText={mode:"read",keys:[…]}` | preview |

**TABLE_QUERY — released view (default):**
```
SAPRead(type="TABLE_QUERY", name="I_SalesDocument",
  columns=["SalesDocument","CreatedByUser","SalesDocumentType","TotalNetAmount","TransactionCurrency"],
  where=[{"field":"SalesDocument","op":"=","value":"0000012345"},
         {"field":"CreationDate","op":">=","value":"20260101"}], maxRows=100)
```
Classic exception (flagged, only if §4 allows): same call with `name="VBAK"`,
`columns=["VBELN","ERDAT","AUART","NETWR","WAERK"]`.
Ops: `= != <> < <= > >= LIKE NOT LIKE IN NOT IN IS NULL IS NOT NULL STARTS_WITH` (literal
prefix). ANDed; IN bare comma-separated ("261,262"), ARC-1 quotes/escapes; on 758 use `<>`.
columns/where are TABLE_QUERY-only; **never legacy `sqlFilter`**. CDS needs 752+; DCL applies.

**SAPQuery — ABAP SQL dialect (released entity as source):**
```
SAPQuery(action="sql",
  sql="SELECT h~SalesDocument, h~TotalNetAmount, SUM( i~NetAmount ) AS items_total
       FROM I_SalesDocument AS h INNER JOIN I_SalesDocumentItem AS i
         ON i~SalesDocument = h~SalesDocument
       WHERE h~SalesDocument = '0000012345'
       GROUP BY h~SalesDocument, h~TotalNetAmount", maxRows=100)
```
| Works | FAILS → use |
|---|---|
| `ORDER BY f ASCENDING`/`DESCENDING` | `ASC`/`DESC` |
| `maxRows` parameter | `LIMIT n` |
| `alias~field` | `alias.field` |
| one `SELECT` | `;`/multiple/`INTO`/`APPENDING`/`PACKAGE SIZE`/`UP TO … ROWS` |
| aggregates + full `GROUP BY` | missing non-aggregated field |
Avoid `@` host vars, comments, dynamic `FROM (name)`, `CLIENT SPECIFIED`, `WITH PRIVILEGED
ACCESS`, native-DB functions. Connected client (MANDT implicit); IN auto-chunked. Response:
`rows`, `rowsReturned`, `rowLimitReached`, `sapReportedTotalRows` (diagnostic only — confirm
with COUNT(*)), `queryExecutionTimeMs`, `executedQueryString` (quote as evidence). On
`DATA_RESPONSE_TOO_LARGE`: fewer columns/rows or key-range paging (`WHERE key>'<last>'
ORDER BY key`); on timeout narrow WHERE (don't loop lowering maxRows). Sequential calls.

## 7. Phase 3 — verify; before blaming the program check
client mismatch; ALPHA/date/currency/unit/language exits; DCL/S_TABU filtering (compare via
the **same CDS entity** the program uses); INNER vs LEFT OUTER / empty FOR ALL ENTRIES driver;
active vs inactive version; aggregation window; released-view vs raw-table semantics (§4);
then "data really wrong". Helpers: `SAPDiagnose(dumps/gateway_errors/odata_perf*/cds_sql/
unittest/authorization_trace*)`, SU53, `SAPRead(MSAG)`, SAPQuery application_log* (*preview).

## 8. Errors
| Symptom | Action |
|---|---|
| allowDataPreview/allowFreeSQL=false | §3 ask |
| Insufficient scope | admin grants scope/profile/role (don't edit server env for one user) |
| SAP 403 | SU53/PFCG; released alternative |
| DATA_SOURCE_BLOCKED | respect; permitted source or stop |
| DATA_SQL_UNSUPPORTED | one static SELECT/WITH or TABLE_QUERY where/columns |
| DATA_LINEAGE_UNRESOLVED / DATA_POLICY_UNAVAILABLE | report reason/path; provable source; no blind retry |
| DATA_RESPONSE_TOO_LARGE | fewer columns/rows; key-range paging |
| sqlFilter / `!=` on 758 | TABLE_QUERY where; `<>` |
| ASC/DESC/LIMIT | ASCENDING/DESCENDING; maxRows |
| 404 datapreview; TABLE_QUERY fails but TABLE_CONTENTS works | backend prerequisite; fallback/report |
| bare 403 only on SQL-bearing calls | possible WAF; admin; `SAP_GZIP_DATAPREVIEW_BODY` admin-approved fallback |
| empty ADT HTML | error, never "0 rows" |
| startup auth preflight 401/403 | fix credentials + restart |
| 0 rows but data "must exist" | §7 checklist |
Blocklist active: TABLE_CONTENTS unfiltered only; TABLE_QUERY catalog checks need the
freestyle endpoint (fail-closed). Never ask to remove entries to run a query.

## 9. Report (user's language)
Verdict ✅/❌/⚠️ + evidence table (expected vs actual + exact call/executedQueryString + rows)
+ root cause (§7) + **Clean Core compliance** (sources used: released C1/C2 vs classic
exception + justification; any Level D avoided) + coverage/limits (rowLimitReached, filters,
client, DCL, sapReportedTotalRows caveat, not-verified) + next steps (never auto-executed).
Mask sensitive values; summarize, don't paste large row sets.

## Appendix O — OpenCode (generic upstream reference)
Skill path: `.opencode/skills/sap-data-verify/SKILL.md` (global `~/.config/opencode/skills/…`).
Tools appear as `sap_SAPRead`/`sap_SAPQuery` (Code Mode: `tools.sap.SAPRead(...)`;
`codemode:false` keeps the native list). Load via `skill` tool / `@sap-data-verify`.
ARC-1 env: `opencode.json` → `mcp.servers.sap.environment` (legacy V1: `mcp.sap.environment`).
Enable = set the flag(s) `"true"` → `/mcps` → sap → disconnect/connect (or restart).
```jsonc
{ "$schema":"https://opencode.ai/config.json",
  "mcp":{"servers":{"sap":{"type":"local","command":["npx","-y","arc-1@latest"],"codemode":false,
    "environment":{"SAP_URL":"https://host:44300","SAP_USER":"{env:SAP_USER}",
      "SAP_PASSWORD":"{env:SAP_PASSWORD}","SAP_CLIENT":"100",
      "SAP_ALLOW_DATA_PREVIEW":"false","SAP_ALLOW_FREE_SQL":"false"}}}},
  "permissions":[{"action":"skill","resource":"sap-data-verify","effect":"allow"},
                 {"action":"sap_*","resource":"*","effect":"ask"}] }
```
`{env:NAME}` reads host env (never commit secrets); `disabled:true` keeps it configured but
offline. Verify: `opencode mcp list`; admin `arc1 config show` / `arc1 tools SAPQuery`.

## Appendix L — this machine (local instance)

Appendix O is the generic upstream shape. On this machine ARC-1 is launched by
`~/.config/opencode/sap/sap-mcp.ps1`, not `npx -y arc-1@latest`, and tools are namespaced
per profile:

- LUF DS4 read instance: `arc1-ds4-100` → Code Mode `tools["arc1-ds4-100"].SAPRead(...)`
- SUS read instance: `arc1-sus-100` → `tools["arc1-sus-100"].SAPRead(...)`
- `SAPRead` / `SAPQuery` / `SAPContext` / `SAPDiagnose` names are unchanged inside the namespace.
- Pick the instance whose system/client matches the object; confirm with
  `python scripts\tools_now.py`. This skill reads only; no writer selection is needed.
- Both data flags are currently `"false"` in `opencode.json` for all five SAP entries
  (set 2026-11-18). ARC-1 posture prints `data=false sql=false`. Re-probe; do not assume.
- Credentials come from Windows Credential Manager via `store-sap-secret.ps1`. Never put a
  password in `opencode.json` and never type one into chat.
- Two write-armed ai-dev instances (`ai-dev-ds4-100`, `ai-dev-sus-100`) also mount
  `run_query` / `get_table_contents`, but they are not ARC-1 and do not honour these flags.
  Do not use them to route around a closed ARC-1 gate.
- To open a gate: ask first, edit the target entry's `environment` in `opencode.json`,
  set one or both flags to `"true"`, then reconnect the MCP or restart the daemon. Never
  kill an MCP process to force a reload; the namespace disappears for the session. Shared
  or BTP server → administrator, not this machine.
