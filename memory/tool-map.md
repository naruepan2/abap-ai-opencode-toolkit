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
   in `lessons.md`.

## Digest (printed by `scripts/session_context.py`)

<!-- digest:start -->
- Source/DDIC → ADT `get_source` / `get_table`; a PowerShell dump mangles Thai.
- Table data: client 100 → ADT; client 900 → SE16. `SE16N` is policy-blocked.
- S/4HANA: read `MATDOC`, not `MKPF` + `MSEG`.
- SAP GUI: a custom toolbar button needs OS focus; a tree may be an ALV tree with no node API and no coordinate click.
- MCP `policy.json` is read once at server start; never kill an MCP process to reload it (the namespace disappears).
- SAP is on-demand: never connect at session start.
- One call per fact, read-only, narrow (`columns_only`, `max_rows`).
<!-- digest:end -->

## Map

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

`ds4-100` (ADT, client 100) and `ds4-900` (SAP GUI, client 900) stay disabled; the
credential dialog must never appear at startup. When a task really needs SAP:

1. Set **only** the requested server to `"enabled": true` in
   `~/.config/opencode/opencode.json`; keep the other one `false`.
2. Ask the user to restart/reconnect opencode once. The dialog appears once and the
   user types username + password. Never store the password.
3. Do the work.
4. Set both back to `"enabled": false` and ask the user to restart once more.

`sap-gui`: `sap_list_connections` first, then `sap_connect_existing`. If the session
dropped, stop and ask the user to log on in SAP GUI before retrying once.

Policy file note: `%APPDATA%\mcp-sap-gui\policy.json` is read once at server start.
Never kill an MCP process to force a reload — the namespace disappears (§Map).

## New MCP checklist

- [ ] Scope is clear (read-only? which system/client?)
- [ ] Does it overlap an existing tool? If yes, mark preferred/fallback.
- [ ] Add a row above with the task it owns.
- [ ] Do not auto-enable it at session start.
