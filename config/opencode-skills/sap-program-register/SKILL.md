---
name: sap-program-register
description: Register a new program under an existing SAP project: program folder, manifests, draft spec, changelog, memory card. For a new PROG object, asks once which template to use (existing SE38 template, bundled YSMILE SALV, or plain class-first). Use for "register new program", "new program folder", "new Z program". Asks for every unknown; never creates a project, deploys, or connects to SAP.
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

### Object lookup (read-only)

After the object name is known, follow "Object lookup" in the shared contract:
run `python scripts\tools_now.py` from the toolkit repo, confirm the project's
system/client, then use that project's live `arc1-*` engine (never hardcode an
engine name):

- `SAPSearch(searchType="tadir_lookup", names=[<name>], objectTypes=[<types>])`
  for existence and package.
- `SAPTransport(action="list")` (then `get` if needed) for the TR holding it.

Report the result, then continue with Transport below. If the engine is not live,
the call fails, or the result is inconclusive, ask the user — never say "does not
exist" and never invent a package or TR.

### Object type and template gate — new PROG only

Do not run this gate when explaining, modifying, or migrating an existing report.
For a **new** object, ask **one** question unless the answer is already in the
conversation, and restate the known object name first:

> ประเภท object ใหม่คืออะไร?
> 1. `PROG` + มี template เดิมใน SE38 — ระบุชื่อโปรแกรม template
> 2. `PROG` + ใช้ Built-in YSMILE SALV template
> 3. `PROG` + ไม่ใช้ SALV — report แบบ class-first ธรรมดา
> 4. `CLAS` / `FUNC` / อื่น ๆ — ไม่ต้องเลือก template
> 5. `RAP` — ไม่ต้องเลือก template

Record `object_type` and `template` in `reports/DECISIONS.md` (a `D-xx` row) and
one line in the program README. Do **not** add a field to `program.yaml`.

- **Option 1** — search only sources genuinely available: the project's live
  ADT/MCP engine, a workspace export, or source the user supplied. If the name
  is not found, or no SAP-capable tool exists, stop and offer option 2 or a
  corrected name. Never silently switch to the built-in. After two failed
  lookups, ask for an export or accept option 2. Never claim "does not exist"
  from a failed call.
- **Option 2** — load `references/salv-template/template.md`, then read all five
  base `.abap` files as one version-consistent set. Scan comments/descriptions,
  build the hook map (`_S01`, `handle_pbo`, `handle_pai`, `start`, `select_data`,
  `process_data`, `display_alv`) before writing business logic. Read a variant
  only for the feature it supplies; never copy demo row conditions. If any
  required source is unavailable, say so — never report a full scan.
- **Option 3** — plain class-first report: thin `PROG` shell, no new
  `FORM`/`PERFORM`, business logic in classes, value-based tests.
- **Options 4-5** — no template gate; continue normally.

Scope note: use the same `L1`/`L2`/`G` decision as `prog-local-class-methodology.md`.
The built-in YSMILE pattern is `L1` — cohesive local classes for report-only behavior
with no external consumer. Move shared or reusable logic to a global owner only for
`L2`/`G` (another consumer, stable API, lifecycle, security boundary or test ownership),
keeping SALV as the presentation layer. Thresholds trigger design review, not automatic
global classes.

### Transport (optional)

Read `allowed_packages` from the project's `project.yaml`.

- If the field is **missing or empty** (older scaffold): ask the user once with the
  `question` tool — "ใช้ package อะไร? ($TMP / ระบุ package ที่ transport ได้ / ไม่แน่ใจ)"
  — and use the answer for this program only. Do **not** edit the project's
  `project.yaml`; that belongs to `sap-project-register`. Record the value and its
  source in `reports/DECISIONS.md` (e.g. `D-02`).
- If the lookup already returned a package and a TR, reuse them — ask only for
  what is still missing.
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
  `changelog`, `fs`, `fs_version`, `decisions`, `memory`, `scope: program`,
  `kind: classic | rap`, `object_count: <n>`, `complexity: light | high`.
  Ask `kind` with one question. If `rap`, ask the object count; derive
  `complexity: high` when it is 20 or more, otherwise `light`. For `classic`
  default `object_count: 1` and `complexity: light` unless the user names a
  superclass chain or another reason to raise it. Record the reason in
  `reports/DECISIONS.md` when the user overrides the derived value.
  These fields drive the co-edit path in `docs/catalog.md` §"Co-edit contract".
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
the portfolio. Ask for domains in **one** question with three bundles, not a
five-item multi-select:

- `sap-abap, working-method` — recommended default for an ABAP program/class/FM.
- `sap-abap, sap-data, working-method` — when it reads tables or verifies FM data.
- "choose myself" — only then show the real names (`sap-abap`, `sap-data`,
  `sap-gui`, `tooling`, `working-method`).

Prefill the recommendation from the purpose the user already gave. Every name
must resolve under `workspace/memory/knowledge/*.md`; `memory_check.py` reports an
unknown name as an issue. Fill `FS`, `Change type`, `Production`, `Target`,
`Approved scope`, `Stop condition`, `Plan`. Then run
`python scripts\specs_sync.py --write` from the toolkit repo.

## Verify

```powershell
python scripts\closeout.py --project <PROJECT>/<PROGRAM>
python scripts\memory_check.py --brief
python scripts\registry_check.py --check --brief
python scripts\tools_now.py
```

Clean closeout (warnings are human decisions), memory 0 issues and 0 warnings,
registry 0 issues, tools unchanged. No SAP object was created or modified — the
lookup is read-only. Report the exact files written and the lookup result.

## Stop

Any blank answer, existing folder, missing project, unresolved domain, missing
permission, or a request to deploy/connect during registration.
