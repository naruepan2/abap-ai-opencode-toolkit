# ABAP Agent Workspace (OpenCode)

A portable workspace where the human and the AI grow together.

This repository is the backup and the operating manual for a small AI teammate:

- a **user profile** that teaches the AI how you work
- durable **lessons** and **corrections**
- **agent / skill / MCP registries**
- **project resume cards**
- lifecycle scripts (next)

It is harness-aware but not harness-locked: this repository is the **OpenCode**
side. Copilot keeps its own separate setup, so the two can be compared.

**Status:** v0.1 bootstrap — memory snapshot. Registry scanner is next.

## Layout

```
README.md
AGENTS.md                 # workspace rules for any agent opened here
SECURITY.md
memory/
  user-profile.md         # how the user communicates and decides
  lessons.md              # durable lessons (date | what | evidence | target)
  corrections.md          # what the AI got wrong and how it was fixed
  skill-candidates.md     # patterns that may become skills
  agent-registry.md       # who owns which agent (editable vs vendor)
  tool-map.md             # task -> authoritative tool -> fallback
  team-roster.md          # subagent roles and delegation rules
  projects/
    zmme011.md            # project resume card
registries/               # machine-readable registries (next)
scripts/                  # registry scanner (next)
templates/                # AGENTS.md / profile templates
docs/                     # design and lifecycle notes
```

## How it works

1. **Session start** — read `memory/user-profile.md`, `memory/lessons.md`,
   `memory/tool-map.md`, and the active project card.
2. **During work** — when the user corrects the AI, log it in `corrections.md`.
3. **Task close-out** — add a durable lesson to `lessons.md`; if the same pattern
   repeats, add a candidate to `skill-candidates.md`.
4. **Before editing** an agent or skill — check `agent-registry.md`; vendor files
   are read-only. Ask before editing an existing personal file.
5. **Never commit** credentials or customer data.

## Quick start on a new machine

1. Clone this repository.
2. Copy `memory/` to `~/.config/opencode/memory/` (or point your global
   `AGENTS.md` at this repository).
3. Add the pointer block from `templates/AGENTS.md` to the global `AGENTS.md`.

## Quick use

```bash
python scripts/registry_check.py --check --brief   # session-start summary
python scripts/registry_check.py --check           # full report
python scripts/registry_check.py --refresh         # merge new items
```

The report is written to `memory/reports/registry-report.md`.

## Roadmap

- [x] Bootstrap memory snapshot and project card
- [x] `scripts/registry_check.py` — skills / MCP / tools drift report
- [x] `registries/*.json` — machine-readable snapshot
- [ ] Tool snapshot automation (OpenCode session hook)
- [ ] Skill and MCP onboarding gates
- [ ] Compare OpenCode vs Copilot on the same task

## Privacy

Private repository. No credentials, tokens, or customer data. SAP system IDs and
client numbers are allowed only because this repository is private.
