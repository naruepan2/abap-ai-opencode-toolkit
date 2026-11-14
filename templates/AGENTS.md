# AGENTS.md pointer template

Add a block like this to the global `AGENTS.md` (OpenCode) or to a project
`AGENTS.md`. Adjust the paths if the workspace lives elsewhere.

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
```


## Project-level template

```markdown
# <project> rules

Project memory lives in `memory/projects/<project>/<program>.md`. Read that card at
session start and update its resume card at session end. A long task gets
`plan-<task>.md` next to the program (`templates/plan.md`), pointed at by the card.
```
