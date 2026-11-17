---
name: sap-program-register
description: Register a new program under an existing SAP project: program folder, manifests, draft spec, changelog, memory card. Use for "register new program", "new program folder", "new Z program". Asks for every unknown; never creates a project, deploys, or connects to SAP.
---

# SAP program register

Program-level scaffold only. One program per call. The project must already exist.

Read the shared contract in `abap-ai-opencode-toolkit/docs/catalog.md` §
"Registration contract — shared by both register skills", plus
`Projects/README.md`, `abap-ai-opencode-toolkit/templates/spec.md`,
`abap-ai-opencode-toolkit/templates/CHANGELOG.md`, and
`workspace/memory/projects/README.md`. If any is missing, stop and report it.

## Ask at invocation

Follow "Question mode" in the shared contract: one question at a time via the
`question` tool, restate known values first, validate each answer before the next,
and stop on a blocker. Batch answers only if the user asks for it. Never guess a
program name, purpose, FS, or domain set. If the project folder does not exist,
stop and tell the user to run `sap-project-register` first.

### Transport (optional)

Read `allowed_packages` from the project's `project.yaml`.

- If it is `$TMP` only: do **not** ask about a TR. Set `transport: none` and note in
  `AGENTS.md` that the program uses `$TMP` and needs no transport.
- Otherwise ask with the `question` tool: "มี TR (ระบุหมายเลข)" / "ยังไม่มี TR —
  ตั้ง none" / "ใช้ $TMP — ไม่ต้องการหมายเลข TR". Never invent a TR number.
- Record `transport: <TR> | none` in `program.yaml` and in the program
  `AGENTS.md` §Deploy / System table.

## Create — `Projects/<PROJECT>/<PROGRAM>/`

Only when the folder does not exist.

- `README.md` — one-line purpose, Status, Pointers, Test focus.
- `AGENTS.md` — program scope, System (with the transport or "$TMP — no
  transport"), Constraints, Session start. §Deploy stays "not yet approved" until
  the user names a writer; a `$TMP` program needs no transport.
- `program.yaml` — `program`, `project`, `status: draft`, `transport`, `spec`,
  `changelog`, `fs`, `fs_version`, `decisions`, `memory`, `scope: program`.
- `spec.md` — copy from `templates/spec.md`; set `program`, `project`,
  `spec_version: 1.0`, `status: draft`, `fs_version`, `fs_file`, `updated`,
  `implemented_version: -`.
- `CHANGELOG.md` — copy from `templates/CHANGELOG.md`, one row
  `| v0 | <date> | scaffold created | pending |`. Do not claim a deploy.
- `spec/source/` — copy the supplied FS here. It is immutable; a new FS is a new
  file plus a new `fs_version`. Set `fs_version` to the `V<n>` token in the file
  name — closeout warns when they disagree. Do not rename the FS to make them match.
- `reports/DECISIONS.md` — header plus `D-01` recording the scaffold decision.

## INDEX and project README

`memory_check.py` checks every program card stem against the portfolio `INDEX.md`,
so a program without its own row is flagged. Do only these two writes:

- Add one row to the portfolio `INDEX.md` at `<portfolio>/INDEX.md`:
  `| <PROGRAM> | <path to the program folder> | scaffold created |`.
  Do not edit any other row.
- Add one line to `Projects/<PROJECT>/README.md` §Programs:
  `- [<PROGRAM>](<PROGRAM>/README.md) — <one-line purpose>`.

### No FS

Use the `HCL_INTERFACE_QA32` pattern: `fs_version: none`, `fs_file: none`,
`status: draft`; say in §1 that open questions are the scope. closeout needs at
least one REQ and one AC — process gates only, marked as such, e.g. REQ-01 "no
implementation before Q-01 is answered", AC-01 "agent asks instead of guessing".
Never invent a customer requirement. Set `spec_version: 0.1` for a no-FS draft
(`1.0` is for a spec written from an FS). Every REQ row must have a non-empty FS
cell — use `none`; closeout reports an empty cell as an issue.

## Memory card

Create `workspace/memory/projects/<PROJECT>/<program>.md` from the template in
`workspace/memory/projects/README.md`. Name the file exactly `<program>.md` (the
folder name in lowercase) so closeout can resolve the spec path from the stem. If
you add a `Working directory:` line, use the absolute path — closeout passes it to
`Path()` as-is; a repo-relative path would resolve against the toolkit repo, not
the portfolio. Set `domains:` to names that resolve under
`workspace/memory/knowledge/*.md`. Fill `FS`, `Change type`, `Production`,
`Target`, `Approved scope`, `Stop condition`, `Plan`. Then run
`python scripts\specs_sync.py --write` from the toolkit repo.

## Verify

```powershell
python scripts\closeout.py --project <PROJECT>/<PROGRAM>
python scripts\memory_check.py --brief
python scripts\registry_check.py --check --brief
python scripts\tools_now.py
```

Clean closeout (warnings are human decisions), memory 0 issues and 0 warnings,
registry 0 issues, tools unchanged. No SAP object was touched. Report the exact
files written.

## Stop

Any blank answer, existing folder, missing project, unresolved domain, missing
permission, or a request to deploy/connect during registration.
