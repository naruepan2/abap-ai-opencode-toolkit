# Knowledge: SAP GUI

> How the SAP GUI behaves when driven by automation. One entry per rule; edit in
> place and raise `Seen`.

## A custom toolbar button needs OS focus

- **Rule:** bring the SAP GUI session window to the foreground before pressing a
  custom (Z) toolbar button. ALV built-in buttons usually still respond.
- **Why:** a custom PAI handler fires only when the window owns the focus.
- **Break it, and:** the call returns success but nothing happens — no message, no
  screen change, so it looks like the button does not exist.
- **Seen:** 2 · **Confidence:** high · **Last confirmed:** 2026-11-13
- **Evidence:** ZDEMO01 toolbar tests; `windows-mcp` returned `USER_CONTROL`

## SICF: select the parent node before F5

- **Rule:** in SICF, filter (host + service path + Apply), then select the parent node
  row in the tree, then press F5.
- **Why:** F5 acts on the selection. With nothing selected it creates a *virtual host*.
- **Break it, and:** the dialog title is "Create/Change a Virtual Host" instead of
  "Create/Change a Service" — and the object is created in the wrong place.
- **Seen:** 1 · **Confidence:** high · **Last confirmed:** 2026-11-13
- **Evidence:** popup title changed only after the node was selected

## SICF: the F9 wizard popup cannot be scripted

- **Rule:** do not use F9. It opens an HTML (Edge) popup that no tool can read.
- **Why:** the content is not a GUI screen; it is a browser control in a modal.
- **Break it, and:** every field needs a separate user answer, and the flow cannot be
  verified.
- **Seen:** 1 · **Confidence:** high · **Last confirmed:** 2026-11-13
- **Evidence:** unreadable HTML popup in the HCL_INTERFACE_QA32 session

## The SICF tree is an ALV tree

- **Rule:** treat it as a grid: `sap_read_tree` and `sap_find_tree_node_by_path` fail,
  and `sap-gui` has no coordinate click — the row must be clicked by the user or via
  a coordinate-capable tool.
- **Why:** the control is `cntlALV_TREE`, not a `GuiTree`.
- **Break it, and:** "Cannot read tree node keys" on every tree call, and no way to
  select the node that F5 needs.
- **Seen:** 1 · **Confidence:** high · **Last confirmed:** 2026-11-13
- **Evidence:** tool errors on `wnd[0]/usr/cntlALV_TREE`

## Verify an ICF service without ADT

- **Rule:** read `ICFSERVICE`, `ICFHANDLER`, `ICFSERVLOC`, `TADIR` with `SE16`, then
  compare HTTP: 401/403 means the node exists, 404 means it does not.
- **Why:** the table proves the node; the HTTP status proves the routing and handler.
- **Break it, and:** you accept a filter popup as proof of absence.
- **Seen:** 1 · **Confidence:** medium · **Last confirmed:** 2026-11-13
- **Evidence:** `/sap/bc/rest/HCLInterface` 401, `/sap/bc/rest/NOPE123` 404, ping 200
