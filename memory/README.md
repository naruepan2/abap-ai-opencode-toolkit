# Memory system (A-scope)

> What this is: a small, durable memory that makes the AI know Pongg and the
> project without re-explaining every session. It does **not** edit any vendor
> agent or skill.

## Read at session start

1. `user-profile.md` — how Pongg communicates and decides
2. `lessons.md` — what we already learned (don't repeat mistakes)
3. `tool-map.md` — which MCP/tool owns which job
4. Active project's `memory/active-context.md` (if it exists)

## Write at task close-out

- A durable lesson → `lessons.md`
- A repeated pattern → `skill-candidates.md`
- A non-obvious tool choice → `tool-map.md`
- A decision with consequences → project `memory/decisions.md` or `reports/DECISIONS.md`

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
