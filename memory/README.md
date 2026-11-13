# Memory system (A-scope)

> What this is: a small, durable memory that makes the AI know Pongg and the
> project without re-explaining every session. It does **not** edit any vendor
> agent or skill.

## Read at session start

1. `user-profile.md` — how Pongg communicates and decides
2. `lessons.md` — what we already learned (don't repeat mistakes)
3. `corrections.md` — the specific mistakes and what "right" looked like
4. `tool-map.md` — which MCP/tool owns which job
5. Active project's `memory/active-context.md` (if it exists)

A lesson that is written but never read is not learning. `corrections.md` is on this
list for exactly that reason — do not skip it.

## Write immediately (do not wait for close-out)

- **A user correction** → one row in `corrections.md`: what the AI did, the correct
  behavior, the root cause, and the fix level. A session can end mid-task, so waiting
  for close-out loses the correction.
- A decision that cannot be cheaply reversed → project `memory/decisions.md` or
  `reports/DECISIONS.md`

## Write at task close-out

- A durable lesson → `lessons.md` (promoted from a `corrections.md` row)
- A repeated pattern → `skill-candidates.md`
- A non-obvious tool choice → `tool-map.md`
- A rule that must bind the next session → the `AGENTS.md` of the level where the
  mistake happened (program → project → workspace). A skill is for a multi-step
  procedure, not for a one-line rule.

## Promotion ladder

```
memory rule → AGENTS.md line → personal agent prompt → skill → script/check
```

Rule of 2: a lesson becomes a skill candidate only after the same correction
appears twice (or once if the risk is high).

## Ownership

- `*-by-pongg` agents: editable with approval
- vendor agents/skills: read-only
- new personal skills: allowed, but test on a real task before promoting

## Registry check

The workspace scanner lives in `scripts/registry_check.py`. It writes
`memory/reports/registry-report.md` and never changes the system. Run
`--check --brief` at session start; run `--refresh` only when new skills, agents,
or MCP servers are installed.

## Where project memory lives

For a real project, create `<project>/memory/` with:

```
active-context.md
decisions.md
lessons.md
skill-candidates.md
```

and add one line to that project's `AGENTS.md`:

> Project memory lives in `memory/`. Read `memory/active-context.md` at session
> start; update it at session end.
