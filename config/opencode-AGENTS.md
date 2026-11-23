# Global rules

## SAP is on-demand only

- Never enable the `ai-dev-ds4-100` / `ai-dev-ds4-900` / `sap-gui` / `playwright`
  MCP servers and never call `sap_connect` / `sap_connect_existing` at session
  start. Opening opencode must never pop the SAP credential dialog.
- Connect only when the user explicitly asks for SAP work ("เข้า SAP", "เข้า DS4",
  "ทำงาน SAP", an ABAP/RAP/CDS task on a named system and client).
- **Before enabling a server**, read the procedure in
  `abap-ai-opencode-toolkit\workspace\memory\tool-map.md` §"SAP on-demand": which server
  to enable, the one restart, who types the password, and how to turn it off again.
- Never write `SAP_PASSWORD` (or any token) to disk. Usernames only, and only in
  the existing `%APPDATA%\sap-ai-dev-toolkit\ai-dev-ds4-100-user.txt` / `ai-dev-ds4-900-user.txt`.
- `sap-gui` work: call `sap_list_connections`, then `sap_connect_existing` if a
  session exists. If the session dropped, stop and ask the user to log on manually
  before retrying once.

## Workspace layout

- Portfolio root: `<portfolio>` — read `INDEX.md` first
- SAP workspace: `<portfolio>\SAP Projects`
- Toolkit, memory, agents, skills: `SAP Projects\abap-ai-opencode-toolkit`
- SAP project files: `SAP Projects\Projects\<PROJECT>\<PROGRAM>` (e.g.
  `SAP Projects\Projects\DEMO\ZDEMO01`)
- Every project/program has `README.md`, `AGENTS.md`, and
  `project.yaml`/`program.yaml`
- Each project owns `_archive` and `_sandbox`; a portfolio-level `_archive` is
  used only when a whole project is retired
- Access: read/write outside the current project requires explicit user
  permission; never recursively scan `SAP Projects` or `<portfolio>`

## Before creating or changing a program

Ask, and wait, before the first edit:

1. **Is there a functional spec?** Where? No FS → say so and propose a one-page FS
   for approval; never invent the requirement.
2. **Bug fix, feature extension, or change request?** Bug fix → reproduce, smallest
   patch, no refactor. Extension → design the delta, stay backward compatible.
   CR → impact analysis over every consumer, then transport order.
3. **Is it live on production, and is the dev object in sync with it?** Live →
   compare the dev source with production first, plan regression; diverged → stop and
   report. Never test on production.
4. **Target: system, client, transport?**

Record the answers in the project card. If an answer is unknown, resolving it is the
first task. The full table lives in the workspace `AGENTS.md`.

## Memory (one call at session start)

Run, from `<portfolio>\SAP Projects\abap-ai-opencode-toolkit`:

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
`memory/`): `user-profile.md`, `corrections.md` (the inbox), `tool-map.md`,
`team-roster.md`, `skill-candidates.md`, `agent-registry.md`, and the durable
`knowledge/<domain>.md`. Open one only when the tier calls for it; the digest already
shows the open inbox rows, so a known correction is not repeated.

**Capture at the moment of correction.** When the user corrects a mistake, add the
row to `corrections.md` immediately — do not wait for task close-out, because a
session can end mid-task. One line per column: what the AI did, the correct
behavior, the root cause, the fix level (`architecture` → `type/check` → `lint/CI`
→ `test` → `memory/AGENTS` → `skill`), evidence, status `open`. **One row of at most
240 characters** — the detail belongs in the project card.

At task close-out, **consolidate** each open row into exactly one outcome: merge it
into `memory/knowledge/<domain>.md` and raise `Seen`, add a new entry, promote it to
an `AGENTS.md` line or a skill, or drop it as a one-off. Set the row `drained` and
update the project resume card. The knowledge base grows by *editing* entries, never
by appending a log. One edit per file, batched.

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
