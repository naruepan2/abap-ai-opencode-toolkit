# Tool map — which tool for which job

> Goal: one authoritative source per fact, least privilege, least token.
> Add new MCPs here before using them broadly. Mark overlaps as
> `preferred` / `fallback` / `deprecated`.

## Rules (in order)

1. **System of record first.** Source/DDIC → ADT. Runtime data → SAP GUI or ADT
   data preview. Runtime logs/dumps → ARC-1 / ST22. Web → browser.
2. **Read-only and narrow.** Use filters, `columns_only`, `max_rows`, object-
   specific reads. Avoid full table dumps.
3. **One call per fact.** No parallel duplicate calls to different tools.
4. **Least privilege + least token.** If two tools can answer, pick the one with
   lower privilege and smaller output.
5. **Record the choice.** If the choice was non-obvious, add a row here and a line
   in `knowledge/tooling.md`.

## Digest (printed by `scripts/session_context.py`)

<!-- digest:start -->
- Source/DDIC → ADT `get_source` / `get_table`; a PowerShell dump mangles Thai.
- Table data: client 100 → ADT; client 900 → SE16. `SE16N` is policy-blocked.
- S/4HANA: read `MATDOC`, not `MKPF` + `MSEG`.
- SAP GUI: a custom toolbar button needs OS focus; a tree may be an ALV tree with no node API and no coordinate click.
- MCP `policy.json` is read once at server start; never kill an MCP process to reload it (the namespace disappears).
- SAP is on-demand: never connect at session start.
- One call per fact, read-only, narrow (`columns_only`, `max_rows`).
- Before an ADT call after toggling MCPs, run `python scripts\tools_now.py`; it prints the live path (write/verify/analyse), and `--check --expect <namespace>` fails if the server did not actually connect.
- 48 vendor skills (Basis/DB/integration/Fiori-iOS, plus the old `sap-adt-cli`) are parked in `~\.config\opencode\skills-parked` — restore the family from `RESTORE.md` before any ops work, do not improvise.
<!-- digest:end -->

## Map

> Tool names below are the *capability*. If a server is off (SAP GUI, ADT, docs,
> Playwright), enable it per §"SAP on-demand" or §"Disabled or removed servers".

| Task | Preferred | Fallback | Notes |
|---|---|---|---|
| Read ABAP source | ADT `get_source` | `sap-adt-cli get-include` | ADT returns proper UTF-8; CLI dump can mangle Thai |
| DDIC structure | ADT `get_table` / `get_structure` | SAP GUI SE11 | |
| Table data (client 100) | ADT `get_table_contents` | SAP GUI SE16 | ADT destination is client-bound |
| Table data (client 900) | SAP GUI SE16 | — | SE16N is policy-blocked; use SE16 |
| ICF service config (SICF) | `sap-gui` **after selecting the parent node in the tree** | manual GUI click | Tree is an ALV tree: no node API (`Cannot read tree node keys`), no coordinate click. F5 without selection creates a *virtual host* instead |
| ICF service verify | SE16 `ICFSERVICE`/`ICFHANDLER`/`ICFSERVLOC`/`TADIR` + `curl -k` (401 vs 404) | ADT `get_table_contents` | Works with no ADT connection |
| MCP config change (`policy.json`) | restart `opencode-cli.exe serve --service` | — | Servers are held by that daemon; restarting the window does not reload them. Never kill an MCP process to force it |
| ALV grid read | `sap-gui` `sap_read_table` | — | |
| Selection screen | `sap-gui` `sap_get_screen_elements` | — | |
| SAP GUI custom toolbar button | `sap-gui` `sap_press_button` **after the session window has OS focus** | ask the user to press it | A custom PAI button may not fire while the window is unfocused; ALV built-in buttons can still work |
| SAP GUI cell edit | `sap_modify_cell` for display; controller button (Select All) or user edit for model changes | — | Cell edits may not reach the custom PAI handler |
| Dumps | ARC-1 ST22 / SAP GUI ST22 | — | |
| Transport list | ADT transport tools | `sap-adt-cli` | |
| Web / UI | `browser` | Playwright MCP | |
| Desktop automation | open-computer-use / windows-mcp | — | only on explicit request |
| Files / source search | `grep` / `glob` / `read` | shell | prefer dedicated tools |

## SAP on-demand

`ds4-100` (ADT, client 100), `ds4-900` (SAP GUI, client 900) and `sap-gui` (GUI
automation) are all **off** in the steady state. The credential dialog must never
appear at startup. When a task really needs SAP:

1. In `~/.config/opencode/opencode.json` set **only** what the task needs to
   `"enabled": true` — `ds4-100` for source/DDIC reads, `sap-gui` for transactions
   and ALV, `sap-docs` for documentation lookups. Keep the rest `false`.
2. Ask the user to restart/reconnect opencode once. The dialog appears once and the
   user types username + password. Never store the password.
3. Do the work.
4. Set everything back to `"enabled": false` and ask the user to restart once more.

Measure on 2026-11-14: moving `sap-gui` (59 tools), `playwright` (25), `sap-docs` (9)
and `rosa` (7) out of the always-on set took the tool catalog from **211 tools /
31.5k chars to 111 / 16.1k** — a saving paid on every session.

`sap-gui`: `sap_list_connections` first, then `sap_connect_existing`. If the session
dropped, stop and ask the user to log on in SAP GUI before retrying once.

Policy file note: `%APPDATA%\mcp-sap-gui\policy.json` is read once at server start.
Never kill an MCP process to force a reload — the namespace disappears (§Map).

## Disabled or removed servers (restore on demand)

| Server | State | What it is | Why | Restore |
|---|---|---|---|---|
| `sap-gui` | disabled | SAP GUI automation, 59 tools | only needed during SAP GUI work; 10.4k chars of prompt | `"enabled": true` + restart |
| `playwright` | disabled | Playwright browser MCP, 25 tools | `browse` already drives the user's real browser | `"enabled": true` + restart |
| `sap-docs` | disabled | SAP documentation search (remote), 9 tools | lookup only; `sap-docs` is not needed to code | `"enabled": true` + restart |
| `rosa` | **removed** | SAP Cloudification Repository: `sap_search_objects`, `sap_get_object_details` (Clean Core Level), `sap_find_successor`, `sap_check_clean_core_compliance`, `sap_list_object_types`, `sap_list_versions`, `sap_get_statistics` | never used (no row here, no lesson) and the `atc-cloudification` skill covers the same job | add `"rosa": {"type":"local","command":["cmd","/c","npx","-y","@rosa-mcp/server"],"enabled":true}` under `mcp`, restart, then add `rosa` to `optional_namespaces` in `registries/tools.json` |

**Parked skills:** 47 vendor skills were moved out of the loaded catalog on 2026-11-14
(21,909 chars of description, ~5.5k tokens per session): 29 Basis/DB/infra and 18
duplicates or unused families. The list, the reason per skill and the one-line restore
are in `~\.config\opencode\skills-parked\RESTORE.md`. After restoring any of them, run
`python scripts/registry_check.py --refresh`.

Anything re-enabled must be added to `optional_namespaces` so turning it on and off
does not look like drift.

## New MCP checklist

- [ ] Scope is clear (read-only? which system/client?)
- [ ] Does it overlap an existing tool? If yes, mark preferred/fallback.
- [ ] Add a row above with the task it owns.
- [ ] Do not auto-enable it at session start.
