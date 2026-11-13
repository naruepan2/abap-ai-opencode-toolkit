# Knowledge: tooling

> Which tool owns which job, and how the tool layer behaves. One entry per rule;
> edit in place and raise `Seen`.

## ADT returns UTF-8; a PowerShell dump mangles Thai

- **Rule:** read ABAP source and DDIC through ADT (`get_source`, `get_table`). Never
  take a program from a PowerShell/CLI dump when Thai literals are involved.
- **Why:** the console pipeline re-encodes the text.
- **Break it, and:** Thai messages turn into mojibake after deploy, and the diff
  looks like a code change.
- **Seen:** 3 · **Confidence:** high · **Last confirmed:** 2026-11-13
- **Evidence:** ZDEMO01 v6 — 1,986 Thai chars + md5 compared against the live source

## `SE16N` is policy-blocked; use `SE16`

- **Rule:** read table data with `SE16` (or ADT `get_table_contents`). `SE16N` is
  blocked by the `sap-gui` transaction policy.
- **Why:** the policy presets block the newer transaction.
- **Break it, and:** the tool call fails and the read path looks broken.
- **Seen:** 2 · **Confidence:** high · **Last confirmed:** 2026-11-13
- **Evidence:** client 900 session; `ICFSERVICE`/`LIPS` reads all went through `SE16`

## Never recall a tool name from memory

- **Rule:** take the tool name from the catalog, not from recollection —
  `sap_send_key` (not `sap_press_key`), and check the parameter names the same way.
- **Why:** names differ between MCP versions and customizations.
- **Break it, and:** one wasted call and an error message that looks like a server
  problem.
- **Seen:** 1 · **Confidence:** low · **Last confirmed:** 2026-11-13
- **Evidence:** `tool error: unknown tool sap_press_key`

## `sap-gui` reads `policy.json` once, at server start

- **Rule:** after changing `%APPDATA%\mcp-sap-gui\policy.json`, restart the
  `opencode-cli.exe serve --service` daemon. Restarting the window is not enough.
- **Why:** MCP servers are held by that daemon; the window is a client.
- **Break it, and:** the audit log shows `allow: ["SICF"]` while every call is still
  blocked — you debug the policy instead of the reload.
- **Seen:** 1 · **Confidence:** high · **Last confirmed:** 2026-11-13
- **Evidence:** policy event 20:52, calls blocked at 20:54 and 20:56

## Never kill an MCP process to force a reload

- **Rule:** stop and ask the user to restart. Killing the process removes the tool
  namespace from the running session.
- **Why:** the session binds the tools at connect time.
- **Break it, and:** the namespace disappears mid-task and no SAP tool can be called
  for the rest of the session.
- **Seen:** 1 · **Confidence:** high · **Last confirmed:** 2026-11-13
- **Evidence:** `sap-gui` vanished from the catalog after the 19:45/19:50 kills

## Real input lands in the focused window

- **Rule:** arrow keys and other real keystrokes sent through desktop automation go
  to whatever window has focus. Bring the target forward first, or use a tool that
  addresses the window directly.
- **Why:** OS-level input has no notion of "the app the agent meant".
- **Break it, and:** `ctrl+home`/`down` land in VS Code and the SAP tree row is never
  selected — the next call acts on the wrong row.
- **Seen:** 1 · **Confidence:** high · **Last confirmed:** 2026-11-13
- **Evidence:** SICF session — keys hit VS Code, tree unchanged
