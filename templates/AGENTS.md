# AGENTS.md pointer template

Add a block like this to the global `AGENTS.md` (OpenCode) or to a project
`AGENTS.md`. Adjust the paths if the workspace lives elsewhere.

```markdown
## Memory (read at session start)

- User profile: `~/.config/opencode/memory/user-profile.md`
- Lessons: `~/.config/opencode/memory/lessons.md`
- Corrections: `~/.config/opencode/memory/corrections.md`
- Skill candidates: `~/.config/opencode/memory/skill-candidates.md`
- Agent/skill ownership: `~/.config/opencode/memory/agent-registry.md`
- Tool routing: `~/.config/opencode/memory/tool-map.md`
- Team roster: `~/.config/opencode/memory/team-roster.md`

Read the user profile and the active project's `memory/projects/<name>.md` at
session start. Update `lessons.md` at task close-out. Do not edit vendor agents or
skills; only `*-by-pongg` files and newly created personal skills may be edited,
and only after approval.
```

## Registry check at session start

If the workspace repository exists, run the read-only scanner once per session:

```powershell
cd "<portfolio>\SAP Projects\abap-agent-workspace-opencode"
python scripts\registry_check.py --check --brief
```

Show the short summary only when it reports issues (exit code 1). Do not auto-fix,
enable/disable an MCP server, or edit a registry without approval.

## Project-level template

```markdown
# <project> rules

Project memory lives in `memory/projects/<project>.md`. Read it at session start
and update its resume card at session end.
```
