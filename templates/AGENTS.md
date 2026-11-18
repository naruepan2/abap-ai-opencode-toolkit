# AGENTS.md pointer template

`install.ps1` writes this block into `~\.config\opencode\AGENTS.md` automatically,
with the real paths filled in. This file is the reference copy: use it when wiring a
machine by hand, or when you want the block in a project `AGENTS.md` instead of the
global one.

```markdown
## Memory (one call at session start)

From the workspace repository, run the digest instead of reading every file:

    python scripts\session_context.py

It prints the active project's resume card, memory + registry health, the open inbox
rows, the knowledge inventory, and the curated tool rules. Then pick a tier:

| Tier | When | Read |
|---|---|---|
| `light` | a question, an analysis, a review | the digest only |
| `task` | any code, file, or SAP work | digest + the project card |
| `deep` | new project, incident, design | digest + every memory file |

Capture a correction in `corrections.md` the moment it happens (status `open`, ≤240
chars). At task close-out, consolidate each row into `knowledge/<domain>.md` — merge
into the existing rule (`Seen +1`), add a new entry, promote to `AGENTS.md`/a skill,
or drop it — and set the row `drained`. The knowledge base grows by editing entries,
never by appending a log. Do not edit vendor agents or skills; only `*-by-pongg`
files and newly created personal skills may be edited, and only after approval.
```

## Checks at session start

The digest runs both scanners for you (`registry_check.py --check --brief` and
`memory_check.py --brief`). An **issue** means something is broken now — show the
short summary and propose a fix. A **warning** is a human decision or a designed
state (new asset, stale date, idle on-demand SAP server) — no turn needed. Do not
auto-fix, enable/disable an MCP server, or edit a registry without approval.

## Program-level spec template

```markdown
# <program> rules

## Session start

1. Read `program.yaml`.
2. Read `spec.md` - requirements, acceptance criteria, deviations, open questions.
   It is the contract; `README.md` is the status history.
3. Confirm the SAP target and scope.
4. Ask before reading or writing anything outside `<program>`.

## Spec

The customer FS is `spec/source/<file>` (immutable). Change a `REQ`/`AC` in
`spec.md` before changing code; a deviation needs a decision reference and the
user's approval. `python scripts\closeout.py --project <PROJECT>/<PROGRAM>` checks
the front matter, the FS file, and the REQ/AC tables.

For a large FS keep a read map in `spec/FS_INDEX.md` (see `templates/spec-index.md`).
Declare `fs_lines` and `fs_bytes` **only in `spec.md` front matter** — `closeout.py`
compares them with the FS file, so the index never carries a second copy of the
fingerprint. A change means the functional sent a new revision: rebuild the index
before using any of its line ranges.

## Rollback

- TR **released**: SAP version management owns the source (`SAPRead(type="VERSIONS")`).
- TR **still open**: SAP has no version of the pre-change source. Before the first
  activation of an object in that TR, copy its **active** source to
  `.baseline/<OBJ>_<TR>.abap`; delete that file when the TR is released. A saved but
  inactive source is not a rollback. The why and the evidence stay in
  `reports/DECISIONS.md`, not in `CHANGELOG.md`.

## Co-edit

Before any write or activation, follow `docs/catalog.md` §"Co-edit contract":
sync-on-touch (one TR list probe; plus `INACTIVE_OBJECTS` and impact for a large
RAP stack), then confirm the TR with the user before the activation run. The
anchor lives in `spec.md` front matter (`last_tr_check` / `last_tr_seen`).
An external edit found in SAP adds a **new** CHANGELOG row with its TR and Scope —
never rewrites an old one. If no signal exists and the user cannot name the TR,
stop; an unreported open-TR edit is not detectable from local data.
```


## Project-level template

```markdown
# <project> rules

Project memory lives in `memory/projects/<project>/<program>.md`. Read that card at
session start and update its resume card at session end. A long task gets
`plan-<task>.md` next to the program (`templates/plan.md`), pointed at by the card.

## Conventions

Rules every program in this project follows — naming prefixes, object types, transport
rules, client split. These are **this project's** rules, not SAP's: another project may
choose differently, so they are not in the shared knowledge base. Add one with its date
and the decision behind it; if a rule is missing, ask instead of inferring it.
```
