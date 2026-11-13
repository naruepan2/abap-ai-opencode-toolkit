# Lifecycle: agents, skills, MCP tools

## Principle

Every agent, skill, and MCP server is an asset with a registry row, an owner, a
status, a version, and a `last_validated` date. No registry row -> not used.

## Registries

Planned machine-readable files under `registries/`:

- `agents.json`
- `skills.json`
- `mcp-servers.json`
- `tools.json`
- `tools-snapshot.json` (generated from the live tool catalog)

Minimum fields:

| Asset | Fields |
|---|---|
| Agent | `id, path, harness, owner, editable, status, version, scope, skills, last_validated` |
| Skill | `id, path, source, owner, status, version, hash, desc_chars, triggers, agents_using, last_validated` |
| MCP server | `server, type, enabled, command_or_url, systems, read_write, tools_count, version, last_validated` |
| Tool | `capability, preferred, fallback, read_write, scope, token_cost, last_verified` |

## Onboarding

### Agent

1. Define scope and the work it must not take.
2. Record owner, harness, tools, skills, and memory access.
3. Write the input/output/evidence contract.
4. Draft it; do not route work to it yet.
5. Test three tasks: normal, ambiguous, risky.
6. Compare with the existing owner using the scorecard.
7. Promote to v1, add routing and changelog. Otherwise archive with a reason.

### Skill

1. Scan finds a new `SKILL.md`; add it as `new`.
2. Record hash, description length, and trigger words.
3. Check duplicate names/triggers and overlap.
4. Read it; propose `draft` or `reject` with evidence.
5. Test on two real tasks; promote to `active` and add it to agent routing.

### MCP server

1. Scan finds a new server in the config; add it as `new`.
2. Enumerate tools and save `tools-snapshot.json`.
3. Classify read-only / write / admin, and record systems and clients.
4. Smoke test: one safe read and one error path.
5. Compare with existing tools; choose `preferred` or `fallback`.
6. Enable only for the tasks that need it; add rows to `tool-map.md`.

## Offboarding

- **Agent:** mark `deprecated` with an end date; migrate work, lessons, and skills;
  update routing and fallback; archive the prompt and eval results; write a
  tombstone (date, reason, replacement).
- **Skill:** path missing -> `missing`; find a fallback; update the agents that
  reference it; archive; never delete immediately.
- **MCP server:** config removed or zero tools -> `unavailable`; update the
  tool map to a fallback; report affected tasks.

## Vendor updates

- Store the hash of each vendor `SKILL.md` and the version of each MCP package.
- After an update, re-check: tools still exist, skills still exist, the eval set
  still passes.
- If a check fails, use the declared fallback and report it. Never edit vendor files.

## Automation levels

| Level | Action | Approval |
|---|---|---|
| L1 | Scan, diff, and report | automatic |
| L2 | Propose registry/tool-map patches | AI proposes, human approves |
| L3 | Auto-apply metadata (hash, last_seen, tool_count, `new`) | automatic + changelog |
| L4 | Promote, disable, or delete | **human only** |

## Scanner checks

1. Skill on disk but not in the registry.
2. Registry path missing.
3. Agent references a missing skill.
4. MCP enabled but zero tools (drift).
5. Tool in the tool map but not in the catalog.
6. New tool not classified.
7. Duplicate capability (two `preferred` tools).
8. Duplicate skill name or trigger.
9. `last_validated` older than 90 days.
10. Skill description over the context budget.

## Cadence

- Per change: registry + changelog + eval.
- Monthly: roster review and stale check.
- Quarterly: re-baseline the eval set after model or tool changes.
