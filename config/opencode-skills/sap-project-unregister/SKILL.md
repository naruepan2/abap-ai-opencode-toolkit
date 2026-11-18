---
name: sap-project-unregister
description: Unregister an existing SAP project from the OpenCode workspace: remove its folder, portfolio INDEX row and the MCP profile/entries created at registration, with an explicit user choice of local _archive or hard delete. Use for "unregister project", "remove project scaffold", "delete project registration". Confirm target and mode every invocation; refuses while programs remain, never touches SAP or another project.
---

# SAP project unregister

Project-level teardown only. One project per call. Never deletes a program folder.

Read `abap-ai-opencode-toolkit/docs/catalog.md` §"Unregistration contract — shared
by both unregister skills" and §"Registration contract — shared by both register
skills". If either is missing, stop and report it. Follow Q1 (mode) and Q2 (final
confirm) exactly, every invocation.

## 1. Resolve and guard

- Ask for the project code. Match case-sensitively; reject `/`, `\`, `..` and
  wildcards. Require `Projects/<PROJECT>/` and its `project.yaml` to exist.
- List every child folder of the project. If any program folder exists —
  anything except `_archive` and `_sandbox` — **refuse** and list them. Tell the
  user to run `sap-program-unregister` for each one first. No cascade.
- Read `project.yaml` for `system`, `code_client`, `test_client` and
  `allowed_packages`. Derive candidate profile names `<project>-<client>`; do not
  guess an URL, user or password.

## 2. Show the removal set

List before asking:

```
project folder   Projects/<PROJECT>/                          (<n> files)
INDEX row        <portfolio>/INDEX.md — the <PROJECT> row
MCP entries      ~/.config/opencode/opencode.json — entries whose command contains -Profile <profile>
profile keys     ~/.config/opencode/sap/profiles.json — profiles referenced only by those entries
```

Never include a program folder. State that SAP objects, transports and the stored
Credential Manager entry are not touched. If a profile is referenced by another
MCP entry, mark it "keep — still in use". If that cannot be proven, mark it
"keep — uncertain" and leave it.

## 3. Ask — every invocation

**Q1 — mode** (one `question` call, no hidden default):

- `A` — move the project folder to `<portfolio>/_archive/<PROJECT>-unregistered-<YYYYMMDD>/`.
  The portfolio `_archive` may be created only for this whole-project retirement,
  as the workspace rules allow. Recoverable.
- `B` — hard delete. Say in a full sentence before Q2: the project folder will
  be deleted permanently and cannot be recovered; the INDEX row and any unused
  MCP entries will also be removed.

**Q2 — final confirm** (one `question` call): restate project, mode, removal set,
programs already absent, and what remains (SAP, TR, stored credential, profiles
kept). Options `confirm` / `cancel`, default `cancel`. Execute only after
`confirm`. Cancel at either question stops with no writes.

## 4. Execute, in this order

Only after Q2 = `confirm`. Use `-LiteralPath` on validated exact paths; no
wildcards, no recursive scan outside the target.

1. Remove the project row from portfolio `INDEX.md` — only the exact row shown.
2. Remove each unused MCP entry from `opencode.json`. Then remove the matching
   profile from `profiles.json` only if no remaining entry references it. Leave
   uncertain ones and report them. Do not enable, disable or restart any server.
   Do not delete a stored credential; report its name so the user can decide.
3. For mode `A`, move the project folder to the portfolio archive path and write
   a short `README.md` there with date, original path, chosen mode and the config
   entries removed. For mode `B`, delete the project folder.
4. From the toolkit repo run `python scripts\registry_check.py --refresh`, then
   `--check --brief`. Never push `_archive` to git.

If a step fails, stop and report completed steps. Do not retry a destructive step
automatically — restart the skill from Q1.

## 5. Verify and report

```powershell
python scripts\tools_now.py
python scripts\memory_check.py --brief
python scripts\registry_check.py --check --brief
python scripts\specs_sync.py
python scripts\closeout.py
```

Expect unchanged tool namespaces (registration entries were disabled), registry
0 issues, memory 0 issues, mirror in sync. Report exact paths removed, chosen
mode, profiles kept or removed, and that SAP/credentials were untouched.

## Stop

Missing project, ambiguous name, any program folder still present, cancel at Q1
or Q2, failure mid-run, or any request to change SAP, a transport, a stored
credential, another project, or to push the archive to GitHub.
