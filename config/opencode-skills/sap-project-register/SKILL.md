---
name: sap-project-register
description: Register a new SAP project in the OpenCode workspace: project folder, manifests, README/AGENTS, archive/sandbox, portfolio INDEX, optional disabled MCP profile. Use for "register new project", "onboard project". Asks for every unknown; never creates a program, deploys, or connects to SAP.
---

# SAP project register

Project-level scaffold only. One project per call. No program folder.

Read the shared contract in `abap-ai-opencode-toolkit/docs/catalog.md` §
"Registration contract — shared by both register skills", plus
`Projects/README.md` and `config/opencode-sap/profiles.example.json`.
If any is missing, stop and report it.

## Ask at invocation

Follow "Question mode" in the shared contract: one question at a time via the
`question` tool, restate known values first, validate each answer before the next,
and stop on a blocker. Batch answers only if the user asks for it. Never guess a
SID, URL, destination, test client, transport, or owner. Get explicit permission
before writing outside the current project.

## Create — `Projects/<PROJECT>/`

Only when the folder does not exist. If it exists, stop and tell the user to use
`sap-program-register` for a program inside it.

- `README.md` — System, Code client, Test client, Transport, and a Programs list
  (empty at first). Use `Projects/README.md` §"Project README template".
- `AGENTS.md` — scope, System table, empty Programs section, §Conventions with
  "add with date and decision; ask, do not infer", §Deploy "not yet approved",
  §Session start. Use the project-level template in
  `abap-ai-opencode-toolkit/templates/AGENTS.md`.
- `project.yaml` — `project`, `system`, `code_client`, `test_client`,
  `transport`, `owner`, `archive: _archive`, `sandbox: _sandbox`, `scope: project`.
- `_archive/README.md`, `_sandbox/README.md` — one line each. No shared
  archive/sandbox under `Projects`.

## INDEX and MCP profile

- Add the project row to the portfolio `INDEX.md` at `<portfolio>/INDEX.md`.
- For a new system only: add `<project>-<client>` to
  `~/.config/opencode/sap/profiles.json` using `profiles.example.json`; fields
  `url`, `client`, `user`, `system_id`, `destination`, `language`, `tls_ca`,
  `allowed_packages`. No password field.
- For each chosen engine add one **disabled** entry to
  `~/.config/opencode/opencode.json` using the existing `sap-mcp.ps1` shape:
  `-Profile <project>-<client> -Engine ai-dev` or `-Engine arc1`,
  `"enabled": false`.
- Run `python scripts\registry_check.py --refresh` in the toolkit repo, then
  `--check --brief`. Tell the user to store the password himself and restart the
  service daemon only when he wants to use the profile.

## Verify

```powershell
python scripts\closeout.py
python scripts\registry_check.py --check --brief
```

Registry 0 issues. No program was created; no SAP object was touched. Report the
exact files written and say: next step is `sap-program-register` for each program.

## Stop

Any blank answer, existing folder, missing permission, unresolved domain, or a
request to deploy/connect during registration.
