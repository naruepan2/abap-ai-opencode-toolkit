---
name: sap-program-unregister
description: Unregister an existing program from the SAP OpenCode workspace: remove its folder, spec mirror, memory card, INDEX row and project README line, with an explicit user choice of local _archive or hard delete. Use for "unregister program", "remove program scaffold", "delete program registration". Confirm target and mode every invocation; never touches SAP objects, transports, credentials or other programs.
---

# SAP program unregister

Program-level teardown only. One program per call. The project must already exist.

Read `abap-ai-opencode-toolkit/docs/catalog.md` §"Unregistration contract — shared
by both unregister skills" and §"Registration contract — shared by both register
skills". If either is missing, stop and report it. Follow the confirmation rules
there exactly: Q1 chooses the mode, Q2 confirms, every invocation.

## 1. Resolve the target

- Ask for the project code and program name. Match case-sensitively
  (`LUF` ≠ `LuF`) and reject names containing `/`, `\`, `..` or wildcards.
- Require both `Projects/<PROJECT>/` and `Projects/<PROJECT>/<PROGRAM>/` to exist
  and the program `program.yaml` to be readable. If not, report and stop.
- Read `program.yaml` for `transport`, `fs`, `fs_version` and `memory`.
- If `transport` is a real TR, state now: **the SAP object and the transport are
  not touched; only local registration is removed.** Never change a TR.

## 2. Show the removal set

List before asking:

```
program folder   Projects/<PROJECT>/<PROGRAM>/                 (<n> files)
spec mirror      workspace/specs/<PROJECT>/<PROGRAM>/
memory card      workspace/memory/projects/<PROJECT>/<program>.md
INDEX row        <portfolio>/INDEX.md  — the row whose path is the program folder
README line      Projects/<PROJECT>/README.md §Programs — the <PROGRAM> line
```

Use the exact line text for INDEX and README. Show it in the answer. Nothing is
changed at this point.

## 3. Ask — every invocation

**Q1 — mode** (one `question` call, no hidden default):

- `A` — move the folder to
  `Projects/<PROJECT>/_archive/<PROGRAM>-unregistered-<YYYYMMDD>/` (recoverable).
  Require that `_archive/` exists; if it does not, stop and ask permission to
  create it.
- `B` — hard delete. Say in a full sentence before Q2: the program folder, spec
  mirror and memory card will be deleted permanently and cannot be recovered.

**Q2 — final confirm** (one `question` call): restate project, program, chosen
mode, the removal set and what remains (SAP object, TR, other programs). Options
`confirm` / `cancel`, default `cancel`. Execute only after `confirm`. A cancel at
either question stops the skill with no writes.

## 4. Execute, in this order

Only after Q2 = `confirm`. Use `-LiteralPath` for every move or delete; never a
wildcard and never a recursive scan outside the listed targets.

1. Remove the program row from portfolio `INDEX.md` — only the exact row shown in
   the removal set. Do not edit any other row.
2. Remove the `<PROGRAM>` line from `Projects/<PROJECT>/README.md` §Programs.
3. Remove the memory card `workspace/memory/projects/<PROJECT>/<program>.md`.
4. Remove the spec mirror `workspace/specs/<PROJECT>/<PROGRAM>/`.
5. For mode `A`, move the program folder to the archive path and write a short
   `README.md` there with the date, original path, chosen mode, and the TR (if
   any) that still exists in SAP. For mode `B`, delete the program folder.
6. From the toolkit repo run `python scripts\specs_sync.py --write` to rebuild the
   mirror manifest. Never mirror `spec/source/`; never push `_archive` to git.

If a step fails, stop and report the completed steps. Do not retry a destructive
step automatically — restart the skill from Q1.

## 5. Verify and report

```powershell
python scripts\memory_check.py --brief
python scripts\registry_check.py --check --brief
python scripts\specs_sync.py
python scripts\closeout.py
```

Expect memory 0 issues, registry 0 issues, spec mirror in sync. Report the exact
paths removed, the chosen mode, whether the archive README was written, and that
the SAP object / TR remain untouched. Report any file that could not be removed.

## Stop

Missing project or program, unreadable `program.yaml`, ambiguous name, no
`_archive` for mode `A`, cancel at Q1 or Q2, failure mid-run, or any request to
change SAP, a transport, MCP config, or another program.
