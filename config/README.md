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
