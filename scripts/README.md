# Scripts

Most checks are read-only, but three commands write local files:
`specs_sync.py --write`, `registry_check.py --init/--refresh` and `coedit_baseline.py`.
`compatibility_check.py` imports `yaml`/`ruamel.yaml`; the rest use the standard library.
None connects to SAP, calls an MCP tool, or edits an agent/skill. Python 3.8+.

## Where the instance lives — `_paths.py`

Every script imports its paths from `_paths.py` instead of assuming this folder:

| Variable | Default | Override |
|---|---|---|
| `WORKSPACE` | `<repo>/workspace` | `ABAP_WORKSPACE` |
| `MEM` | `<workspace>/memory` | — |
| `SPECS` | `<workspace>/specs` | — |
| `PROJECTS` | `<repo>.parent/Projects` | `ABAP_PROJECTS_ROOT` |
| `INDEX` | `<projects root>.parent.parent/INDEX.md` | `ABAP_INDEX` |

Relative overrides resolve against the current directory. A missing directory is a
readable message, not a traceback.

## `session_context.py` — the one call at session start

Prints a compact digest (~2.6k chars, ~0.8k with `--tiny`) so the agent does not read
eight files
before starting work:

- the active project's resume card (status / next step / do not / working dir)
- memory and registry health, one line each (it runs both scanners for you)
- the **open** corrections, with their fix level
- the curated tool rules from the `digest` block in `workspace/memory/tool-map.md`
- the size and row count of every file that can be opened on demand
- git branch and uncommitted count

```bash
python scripts/session_context.py                          # brief (default)
python scripts/session_context.py --tiny                   # light tier, ~0.8k chars
python scripts/session_context.py --full                   # + file map + raw checks
python scripts/session_context.py --project DEMO/ZDEMO01    # pin the card
python scripts/session_context.py --no-checks              # skip both scanners
```

`--tiny` prints only the project, its status and next step, one style rule, the
open-correction count, and health **only when there is an issue** — use it for a
question, an analysis, or a review, where the tool rules do not matter.

The active card defaults to the most recently modified card under
`workspace/memory/projects/*/`. Exit `0` means the digest printed; `1` means a
required memory file is missing.

## `closeout.py` — the last call of a task

Read-only check of the things that rot between sessions: the inbox (open rows, their
age, the cap), the project card (the four change-contract answers and how old it is),
a referenced plan file (exists; how many todos are open or blocked), knowledge entries
(none unconfirmed for 180 days), the program spec/changelog, shipped-file portability,
and the memory-audit line in the card.

```bash
python scripts/closeout.py                          # newest card
python scripts/closeout.py --project DEMO/ZDEMO01
```

Exit `0` means no issue; `1` means an issue from any checked area — a missing plan, an
unparsable table, a malformed memory-audit line, or a spec/changelog/portability failure.
Warnings (an old open row, a missing contract answer, a blocked todo, a stale entry) are
human decisions and do not fail the check.

## `coedit_baseline.py` — local pre-image store

Content-addressed pre-images for the co-edit contract. `save` writes a gzip blob
under `<root>/.baseline/blobs/sha256/` and one manifest entry per intent;
`attach` records the post-hash after a verified write; `get` restores a blob to
stdout; `list` shows the index. It verifies `--pre-hash` before storing and
refuses to store a duplicate intent. This is local-only state — `.baseline/` is
git-ignored because source can contain customer data.

```bash
python scripts/coedit_baseline.py save --root <program> --object DS4/100/CLAS/ZCL_X/implementations \
    --engine ai-dev --intent CHG-1 --tr DEVK900123 --source-file pre.abap --pre-hash sha256:...
python scripts/coedit_baseline.py attach --root <program> --object DS4/100/CLAS/ZCL_X/implementations \
    --intent CHG-1 --post-hash sha256:...
python scripts/coedit_baseline.py get --root <program> --hash <sha256>
python scripts/coedit_baseline.py list --root <program>
```

Exit `1` means bad input, hash mismatch, missing entry, or missing blob — never
silently write a pre-image that does not match the observed source.

## `registry_check.py`

Read-only scanner for skills, agents, MCP servers, and the tool snapshot. It never
enables a server, promotes a skill, or edits an agent.

```bash
# one-time baseline (writes registries/*.json)
python scripts/registry_check.py --init

# merge newly discovered items into the existing registries
python scripts/registry_check.py --refresh

# compare and write workspace/memory/reports/registry-report.md
python scripts/registry_check.py --check

# short summary for a session start
python scripts/registry_check.py --check --brief
```

Exit code is `0` when nothing is broken, `1` when there is an issue. The split
matters:

| Result | Meaning | Action |
|---|---|---|
| issue | broken now: missing path, duplicate name, agent pointing at a missing skill, missing tool/server, zero tools on a non-optional server | propose a fix |
| warning | needs a human decision or is a designed state: new asset, stale validation, over-budget description, idle on-demand SAP server | none now |

Namespaces in `optional_namespaces` (the on-demand SAP servers) are excluded from
tool drift and from the zero-tools issue on both sides, so connecting or
disconnecting SAP no longer looks like drift.

## `memory_check.py`

Read-only integrity check for the memory system: required files, table columns,
row evidence, credential-like strings, allowed status values (`open`, `drained`),
promoted skill candidates with a real skill folder, and
project cards reachable from the portfolio `INDEX.md`. Run it after a close-out.

```bash
python scripts/memory_check.py            # full report
python scripts/memory_check.py --brief    # one-line summary
```

## Tool snapshot

`registries/tools-snapshot.json` and `registries/tools-full.json` are written by
the OpenCode plugin at `plugins/tool-snapshot`. The plugin calls `ctx.tool.list()`
in the OpenCode server, so it sees MCP and built-in tools without a manual step.

The scanner compares the full tool IDs with the baseline in `registries/tools.json`
and reports new or missing tools. Run `--refresh` only when you want to accept the
new list into the baseline.
