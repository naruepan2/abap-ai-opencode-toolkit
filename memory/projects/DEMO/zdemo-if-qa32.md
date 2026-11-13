# HCL Interface QA32

> Last updated: 2026-11-13 (OpenCode session). Re-verify live state before changing
> anything.

## Resume card

- **Status:** ICF node `/default_host/sap/bc/rest/HCLInterface` exists, active, and
  answers HTTP. **Created manually by the user**, not by the agent.
- **Next step:** wait for the user's instruction about what was configured wrongly
  (four candidates listed in the project README). Do not change anything unasked.
- **Do not:** press Store after a declined save gate, kill MCP processes, or claim a
  service is "not created" from a single failed popup.

## Goal

HCL interface on DS4 (client 100). The immediate task was creating the SICF host /
service node at `/default_host/sap/bc/rest/HCLInterface`. The wider interface scope
is still undefined ("QA32" unclarified).

## Verified state (2026-11-13)

| Item | Value |
|---|---|
| System | DS4, client 100, user DEMOUSER, release 755, kernel 75F, HDB |
| ICF node | `ICFSERVICE` `ICF_NAME = HCLINTERFACE`, `ORIG_NAME = HCLInterface` |
| Parent GUID | `00EE53Z8TX0ULF35LCK0D51B6` (= node `rest`) |
| Node GUID | `00A9WAK8Z5R9CLD1PTD5J2O2U` |
| Handler | `ZCACL_REST_HTTP_HANDLER_HCL`, order `01`, type `A` |
| Active | `ICFSERVLOC-ICFACTIVE = X` |
| `TADIR` | `R3TR SICF HCLINTERFACE   00EE53Z8TX0ULF35LCK0D51B6`, package `Z001` |
| Handler class `TADIR` | `R3TR CLAS ZCACL_REST_HTTP_HANDLER_HCL`, package `Z001` |
| HTTP | `https://sap.example.com:44300` (also HTTP 8000, HTTPS 20400, SMTP 2500) |
| HTTP result | `/sap/public/ping` 200, `/sap/bc/rest/HCLInterface` 401, `/sap/bc/rest/NOPE123` 404 |

Parent chain: `DEFAULT_HOST` (`0000000000000000000000000`) → `SAP`
(`DFFAEATGKMFLCDXQ04F0J7FXK`) → `BC` (`EEPI2GLFNOLHN7IW9R54I61RZ`) → `REST`
(`00EE53Z8TX0ULF35LCK0D51B6`). The `REST` node has **no handler of its own** — every
child defines its own (siblings: `4-WAYS`, `ASRS`, `SALESFORCE`, `SLPROTOCOL`, `TEST`,
`THEMES`).

## What went wrong in this session (agent mistakes)

1. **Restart did not reach the MCP server.** `sap-gui` reads
   `%APPDATA%\mcp-sap-gui\policy.json` once at start. Restarting the OpenCode window
   is not enough: the MCP servers are held by the background
   `opencode-cli.exe serve --service` daemon (was PID 8848). The audit log proved it:
   a `policy` event with `allow: ["SICF"]` at 20:52, yet calls at 20:54/20:56 still
   blocked — those were served by an older, pre-policy process.
2. **Killed the live MCP process.** Killing the stale 19:45/19:50 stacks removed the
   `sap-gui` namespace from the session mid-task. Killing MCP processes to force a
   reload costs the session its tools; stop and let the user restart instead.
3. **Assumed F5 creates a sub-service.** F5 acts on the tree selection. With nothing
   selected it opens **"Create/Change a Virtual Host"**, not the service dialog.
4. **Used the F9 wizard.** It opens an HTML (Edge) popup that scripting cannot read,
   so every answer needs a separate user approval — wrong tool for this job.
5. **Sent arrow keys through `open-computer-use` to SAP GUI.** SAP GUI was not
   foreground; the keys landed in another window and the tree row was never selected.
6. **Told the user a service was not created** based on a filter popup
   ("Selection criteria did not select any data"), while the node actually existed.
   Verify from `ICFSERVICE` / HTTP before reporting absence.

## Correct procedure (SICF sub-element) — use next time

1. `sap_execute_transaction("SICF")`.
2. Fill the filter: **Virtual Host** = `default_host`, **Service Path** = parent path
   (`/sap/bc/rest`), optional **ServiceName**, then **Apply**. Plain Enter does
   nothing; Apply without host+path returns "no data".
3. **Select the parent node row in the tree.** The tree is an ALV tree: `sap_read_tree`
   and `sap_find_tree_node_by_path` fail with "Cannot read tree node keys", and
   `sap-gui` has no coordinate click — the row has to be clicked in the GUI.
4. Press **F5**. The dialog title must be **"Create/Change a Service"** with
   `Path: /default_host/sap/bc/rest/`. If it says "Create/Change a Virtual Host", the
   selection is wrong — cancel and select the node.
5. Fill Service Name, Description; switch to **Handler List** and add the handler.
6. If the screen is in display mode, `Ctrl+F1` (Display ↔ Change); **F11 is not
   active** here — save with the **Store (Ctrl+S)** button.
7. The save gate asks the user. If declined: stop, report, do not retry.
8. Package / transport request prompt follows the store, then activate the node in
   the tree if needed.

## Verification recipe (works without the ADT MCP)

- `SE16` (not blocked; `SE16N` is) → `ICFSERVICE`, `ICFHANDLER`, `ICFSERVLOC`, `TADIR`.
- HTTP: `curl.exe -k -s -o NUL -w "%{http_code}" https://sap.example.com:44300/<path>`.
  `401`/`403` means the node exists and routing works; `404` means it does not.
  Compare always with a known-good path (`/sap/public/ping`) and a bogus one.

## Access notes

- `sap-gui` transaction policy: preset `default` blocks SICF; allow it with
  `%APPDATA%\mcp-sap-gui\policy.json` = `{"allow": ["SICF"]}` and **restart the
  opencode service**.
- ADT MCP `ds4-100` was unavailable for most of this session; `SE16` + `SMICM` were
  the working read paths.
