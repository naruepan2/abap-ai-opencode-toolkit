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

## Memory (read at session start)

- User profile: `~/.config/opencode/memory/user-profile.md`
- Lessons: `~/.config/opencode/memory/lessons.md`
- Corrections ledger: `~/.config/opencode/memory/corrections.md`
- Skill candidates: `~/.config/opencode/memory/skill-candidates.md`
- Agent/skill ownership: `~/.config/opencode/memory/agent-registry.md`
- Tool routing: `~/.config/opencode/memory/tool-map.md`

Read the user profile, `corrections.md`, and the active project's
`memory/active-context.md` at session start, so a known correction is not repeated.

**Capture at the moment of correction.** When the user corrects a mistake, add the
row to `corrections.md` immediately — do not wait for task close-out, because a
session can end mid-task. Record what the AI did, the correct behavior, the root
cause, and the fix level (`architecture` → `type/check` → `lint/CI` → `test` →
`memory/AGENTS` → `skill`).

At task close-out, promote anything durable from `corrections.md` into `lessons.md`,
and update the active project's `memory/active-context.md`. If a rule needs to bind
the next session, put it in the `AGENTS.md` of the level where the mistake happened;
use a skill only for a multi-step procedure that repeats.

Do not edit vendor agents/skills; only `*-by-pongg` files and newly created personal
skills may be edited, and only after approval.

### Registry check at session start

If `<portfolio>\SAP Projects\abap-agent-workspace-opencode\scripts\registry_check.py`
exists, run it once per session from that folder:

```powershell
python scripts\registry_check.py --check --brief
```

If it reports issues (exit code 1), show the short summary and propose a fix. Do not
auto-fix, enable/disable an MCP server, or edit a registry without approval. If it is
clean, do not mention it.
