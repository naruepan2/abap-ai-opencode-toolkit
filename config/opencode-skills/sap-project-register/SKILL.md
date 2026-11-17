---
name: sap-project-register
description: Register a new SAP project and/or program in the OpenCode toolkit workspace from the adopted design — folder scaffold, manifests, spec, memory card, INDEX, and optional MCP profile. Use for "register new project", "new program", "onboard project", "create program folder", "SUS new project". Asks for every unknown; never invents a system, FS, transport, or requirement. Does not deploy ABAP or connect to SAP.
---

# SAP project register

Scaffold only. Never guess a customer fact. One project or one program at a time.

This skill implements the layout in `Projects/README.md`, the spec contract in
`abap-ai-opencode-toolkit/templates/spec.md`, the memory-card template in
`workspace/memory/projects/README.md`, and the profile shape in
`config/opencode-sap/profiles.example.json`. Read those four first. If one is
missing, stop and report it.

## Ask before any write

Collect these from the user. A blank is a blocker, not a default:

- Project code (short uppercase, e.g. `SUS`) and program name (SAP object name,
  e.g. `ZMMX001`). One-line purpose.
- System SID/description, ADT URL, SAP Logon destination, SAP user, language,
  TLS CA path, allowed packages.
- Test client, if the project has one. Transport, if one exists.
- FS path. If there is no FS, say so and use the no-FS draft pattern below.
- Knowledge domains for the memory card (names must resolve under
  `workspace/memory/knowledge/*.md`).
- Which engines to register: `ai-dev`, `arc1`, or both.
- Explicit permission to create a new project folder, edit the portfolio
  `INDEX.md`, and edit `~/.config/opencode/opencode.json` and
  `~/.config/opencode/sap/profiles.json`.

Never ask the user to paste a password. After a profile is created, the user
stores it himself with `store-sap-secret.ps1 -Profile <profile>`.

## Project scaffold — `Projects/<PROJECT>/`

Create only when the folder does not exist. If it exists, ask whether to add a
program instead.

Files:

- `README.md` — project table (System, Code client, Test client, Transport)
  and a program list; use `Projects/README.md` §"Project README template".
- `AGENTS.md` — project-level rules: scope, System table, Programs list,
  §Conventions with "ask, do not infer", and §Session start. Use the
  project-level template in `abap-ai-opencode-toolkit/templates/AGENTS.md`.
- `project.yaml`:
  `project`, `system`, `code_client`, `test_client`, `transport`, `owner`,
  `archive: _archive`, `sandbox: _sandbox`, `scope: project`.
- `_archive/README.md` and `_sandbox/README.md` — one line each. Never create
  shared archive/sandbox folders under `Projects`.

## Program scaffold — `Projects/<PROJECT>/<PROGRAM>/`

Copy from `abap-ai-opencode-toolkit/templates/` and fill placeholders.

- `README.md` — one-line purpose, Status, Pointers, Test focus.
- `AGENTS.md` — program-level rules: scope, System, Constraints, Session start.
  Add §Deploy only when the user has approved a concrete writer/transport;
  otherwise write "not yet approved".
- `program.yaml` — `program`, `project`, `status`, `spec`, `changelog`, `fs`,
  `fs_version`, `decisions`, `memory`, `scope: program`.
- `spec.md` — from `templates/spec.md`. Set `program`, `project`,
  `spec_version: 1.0`, `status: draft`, `fs_version`, `fs_file`, `owner`,
  `updated`, `implemented_version: -`.
- `CHANGELOG.md` — from `templates/CHANGELOG.md`, with one row
  `| v0 | <date> | scaffold created | pending |`. Do not claim a deploy.
- `spec/source/` — copy the user's FS here only if one was supplied. It is
  immutable; a new FS is a new file plus a new `fs_version`.
- `reports/DECISIONS.md` — header plus `D-01` recording the scaffold decision.

### No FS yet

Use the HCL_INTERFACE_QA32 pattern: `fs_version: none`, `fs_file: none`,
`status: draft`, and say in §1 that open questions are the scope. closeout still
needs at least one REQ and one AC — use process gates only, marked as such, e.g.
REQ-01 "no implementation before Q-01 is answered", AC-01 "agent asks instead of
guessing". Never invent a customer requirement.

## Memory card and INDEX

- Create `workspace/memory/projects/<PROJECT>/<program>.md` from the template in
  `workspace/memory/projects/README.md`. Set the `domains:` line to names that
  resolve. Fill the resume card with `FS`, `Change type`, `Production`, `Target`,
  `Approved scope`, `Stop condition`, `Plan`.
- Add the project and program rows to the portfolio `INDEX.md` at
  `<portfolio>/INDEX.md`; `memory_check.py` checks card stems there.
- Run `python scripts\specs_sync.py --write` from the toolkit repo.

## MCP profile — optional, only for a new system

- Add `<project>-<client>` to `~/.config/opencode/sap/profiles.json` using the
  shape in `profiles.example.json`: `url`, `client`, `user`, `system_id`,
  `destination`, `language`, `tls_ca`, `allowed_packages`. No password field.
- In `~/.config/opencode/opencode.json`, add one disabled entry per chosen engine,
  using the existing `sap-mcp.ps1` launch shape:
  `-Profile <project>-<client> -Engine ai-dev` or `-Engine arc1`.
  Set `"enabled": false`. Do not enable at registration time.
- Run `python scripts\registry_check.py --refresh` in the toolkit repo, then
  `--check --brief`. Tell the user to store the password and restart the service
  daemon only when he wants to use the profile.

## Verify before claiming done

From the toolkit repo:

```powershell
python scripts\closeout.py --project <PROJECT>/<PROGRAM>
python scripts\memory_check.py --brief
python scripts\registry_check.py --check --brief
python scripts\tools_now.py
```

Clean closeout (warnings are human decisions), memory 0 issues, registry
0 issues, and `tools_now.py` still showing only the already-enabled engines.
No SAP object was touched. Report the exact files created and the values that
came from the user.

## Stop

Stop and ask if any required answer is blank, if a file already exists and would
be overwritten, if a domain name does not resolve, if permission for an outside
folder is missing, or if the user wants to deploy or connect during registration.
