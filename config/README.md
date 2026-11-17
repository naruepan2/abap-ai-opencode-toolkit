# Config backup

Snapshot copies of files that live outside this repository but are required for
the memory system to work. They are **backups, not the working copies**: OpenCode
reads the real files under `~/.config/opencode/`, never these.

## Files

| Snapshot | Live file | Purpose |
|---|---|---|
| `opencode-AGENTS.md` | `~/.config/opencode/AGENTS.md` | Global rules: SAP on-demand, workspace layout, memory read/write, registry and memory checks |

`~/.config/opencode/` is not a git repository, so without this snapshot a disk
loss or a fresh machine would silently drop the global rules while `memory/`
survived.

## Skills that ship (`config/opencode-skills/`)

Personal skills written for this toolkit — not vendor copies. `install.ps1` copies each
one into `~/.config/opencode/skills/<name>/` **only when that name is not there yet**,
so a reinstall restores them and never overwrites a newer local edit.

| Skill | Purpose |
|---|---|
| `sap-auditor` | audit → mentor → commentator over finished work; claims table with `path:line` evidence |
| `sap-mcp-upgrade` | bump an MCP version pin or add an entry from evidence; probe → approval → verify → restore disabled |
| `sap-project-register` | scaffold a new SAP project folder, manifests, INDEX, optional disabled MCP profile |
| `sap-program-register` | scaffold a new program under an existing project: spec, changelog, memory card |

Sync rule: the live copy is authoritative. After editing
`~/.config/opencode/skills/<name>/SKILL.md`, copy it back here in the same change —
the same rule as the AGENTS snapshot above.

## Sync rule

- After editing the live file, copy it here in the same change and commit both.
- Do not edit the snapshot by hand and expect it to take effect. Edit the live
  file, then refresh the snapshot.
- Restore = copy the snapshot back to the live path, then restart OpenCode.

## Refresh

```powershell
Copy-Item "$HOME\.config\opencode\AGENTS.md" `
  "config\opencode-AGENTS.md" -Force
```

## Never store credentials

These files contain rules only. No password, token, or key belongs here, or in
any memory file.
