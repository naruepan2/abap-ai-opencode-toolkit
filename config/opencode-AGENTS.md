# Global rules

## SAP is on-demand only

- Do NOT enable the `ds4-100` / `ds4-900` MCP servers (or call `sap_connect` /
  `sap_connect_existing` / other SAP logon tools) at session start.
- Opening opencode must never pop the "SAP logon - DEMO DEV
  [NEW] (client 100)" or "(client 900)" PowerShell credential dialog.
- Only connect to SAP when the user explicitly asks for SAP work
  (e.g. "เข้า SAP", "เข้า DS4", "ทำงาน SAP", ABAP/RAP/CDS tasks
  against a named SAP system).
- When SAP work is requested:
  1. Temporarily set only the requested server (`"ds4-100"` for client 100,
     `"ds4-900"` for client 900) to `"enabled": true` in
     `~/.config/opencode/opencode.json` — keep the other one `false`
  2. Ask the user to restart/reconnect opencode once
  3. The credential dialog will appear once; the user enters
     username + password manually. Never store the password.
  4. After the SAP work is done, set `"enabled": false` again
     (both `ds4-100` and `ds4-900`) and ask the user to restart opencode.
- For `sap-gui` work, first call `sap_list_connections`, then
  `sap_connect_existing` if a session exists. If the session is
  dropped, stop, notify the user, and ask them to log on to SAP
  GUI manually before retrying once.
- Do not store SAP usernames or passwords in files, `.env`, or
  config, except the existing username-only memory files already
  used by `luf-ds4-100.ps1` / `luf-ds4-900.ps1`
  (`%APPDATA%\sap-ai-dev-toolkit\ds4-100-user.txt` /
  `%APPDATA%\sap-ai-dev-toolkit\ds4-900-user.txt`).
  Never write `SAP_PASSWORD` to disk.

## Workspace layout

- Portfolio root: `<portfolio>` — read `INDEX.md` first
- SAP workspace: `<portfolio>\SAP Projects`
- Framework, memory, agents, skills: `SAP Projects\abap-agent-workspace-opencode`
- SAP project files: `SAP Projects\Projects\<PROJECT>\<PROGRAM>` (e.g.
  `SAP Projects\Projects\DEMO\ZDEMO01`)
- Every project/program has `README.md`, `AGENTS.md`, and
  `project.yaml`/`program.yaml`
- Each project owns `_archive` and `_sandbox`; a portfolio-level `_archive` is
  used only when a whole project is retired
- Access: read/write outside the current project requires explicit user
  permission; never recursively scan `SAP Projects` or `<portfolio>`

## Memory (one call at session start)

Run, from `<portfolio>\SAP Projects\abap-agent-workspace-opencode`:

```powershell
python scripts\session_context.py
```

It prints the active project's resume card, the memory + registry health, the open
corrections, and the curated tool rules. Then pick a tier:

| Tier | When | Read |
|---|---|---|
| `light` | a question, an analysis, a review | the digest only |
| `task` | any code, file, or SAP work | digest + the active project card |
| `deep` | new project, incident, design | digest + every memory file |

The full files live in `~/.config/opencode/memory/` (a junction to the workspace
`memory/`): `user-profile.md`, `lessons.md`, `corrections.md`, `tool-map.md`,
`team-roster.md`, `skill-candidates.md`, `agent-registry.md`. Open one only when the
tier calls for it; the digest already shows the open corrections, so a known
correction is not repeated.

**Capture at the moment of correction.** When the user corrects a mistake, add the
row to `corrections.md` immediately — do not wait for task close-out, because a
session can end mid-task. One line per column: what the AI did, the correct
behavior, the root cause, the fix level (`architecture` → `type/check` → `lint/CI`
→ `test` → `memory/AGENTS` → `skill`), evidence, status `open`.

At task close-out, promote anything durable from `corrections.md` into `lessons.md`
and set the source row to `promoted` (do not copy the same text into both), then
update the active project's resume card. One edit per file, batched. If a rule needs
to bind the next session, put it in the `AGENTS.md` of the level where the mistake
happened; use a skill only for a multi-step procedure that repeats.

Do not edit vendor agents/skills; only `*-by-pongg` files and newly created personal
skills may be edited, and only after approval.

### Checks

The digest runs `scripts/registry_check.py --check --brief` and
`scripts/memory_check.py --brief` for you.

- An **issue** means something is broken now (missing path, duplicate name, agent
  pointing at a missing skill, missing tool/server, zero tools on a server that is
  not optional): show the short summary and propose a fix. Do not auto-fix, enable
  or disable an MCP server, or edit a registry without approval.
- A **warning** is a human decision or a designed state (a newly installed asset, a
  stale validation date, an over-budget description, an idle on-demand SAP server).
  Do not spend a turn on it.
- `--refresh` only after installing a new skill, agent, or MCP server.
