# Lessons

> One terse row per lesson, ≤240 chars. A lesson is created by **promoting** a
> correction, so do not restate the correction's detail here — point at the card.
> A lesson becomes a skill candidate only after the same correction appears twice
> (or once if the risk is high).

| Date | What happened | Evidence | Generalizable? | Target |
|---|---|---|---|---|
| 2026-11-13 | History rows and actionable rows must be separate, else 041 blocks the remaining qty | card §Decisions v6 | yes | skill cand `sap-ztable-history-persistence` |
| 2026-11-13 | Check Thai characters after a CLI source dump; ADT avoids the problem | v6: 1,986 chars + md5 | yes | memory rule (done) |
| 2026-11-13 | ADT for source/DDIC, SAP GUI for runtime; fewer guesses | session ZDEMO01 | yes | tool-map (done) |
| 2026-11-13 | Name a key by its source, not its shape (DO vs SO) | debug line 5290 | yes | skill cand |
| 2026-11-13 | `BAPI_OUTB_DELIVERY_CREATE_SLS` returns an empty `DELIVERY` when `NUM_DELIVERIES > 1`; recover from LIPS | DO 1041100092 | yes | memory (done) |
| 2026-11-13 | Batch split needs the main item in `ITEM_CONTROL` with `CHG_DELQTY = 'X'` | debug `lt_item_control` | yes | skill cand |
| 2026-11-13 | A GUI custom button needs OS focus; ALV buttons still work | windows-mcp | yes | tool-map (done) |
| 2026-11-13 | `MATDOC` replaces `MKPF` + `MSEG` in S/4HANA | MATDOC DDIC | yes | memory (done) |
| 2026-11-13 | `sap-gui` reads `policy.json` once at start; restart the `serve --service` daemon, not the window | audit 20:52 vs 20:54 | yes | tool-map (done) |
| 2026-11-13 | Never kill an MCP process; the tool namespace disappears mid-session | `sap-gui` gone 19:45 | yes | memory rule (done) |
| 2026-11-13 | SICF: select the parent node before F5; the F9 wizard popup is unreadable | popup title | yes | skill cand `sap-sicf-service-create` |
| 2026-11-13 | The SICF tree is an ALV tree: no node API, no coordinate click | tool errors on `cntlALV_TREE` | yes | tool-map |
| 2026-11-13 | Never conclude "absent" from a filter popup; verify in a table or over HTTP | node existed | yes | memory rule (done) |
| 2026-11-13 | Arrow keys sent through open-computer-use land in whatever window has focus | keys hit VS Code | yes | tool-map |
| 2026-11-13 | Verify a SICF service with `SE16` + `curl` (401/404), no ADT needed | 401/404/ping | yes | skill cand |

## How to add

- Date `YYYY-MM-DD`; one line, ≤240 chars; the evidence is a pointer, not a story.
- Target: `memory` / `agent` / `skill` / `check` / `AGENTS.md`.
- If the row is long, the detail belongs in the project card — shorten the row.
