# SAP MCP launcher (versioned backup)

The live copies are in `~\.config\opencode\sap\` (outside git). This folder is the
backup of the generic scripts; **real** `profiles.json` (customer URLs, usernames)
stays local, and `profiles.example.json` shows the shape only.

| File | Purpose |
|---|---|
| `profiles.example.json` | profile shape: URL, client, user, system, destination, CA, package allowlist |
| `sap-cred.ps1` | Windows Credential Manager helper (`CredRead` / `CredWrite` / `CredDelete`) |
| `store-sap-secret.ps1` | store / list / remove the password for a profile |
| `sap-mcp.ps1` | launcher: `-Profile <name> -Engine ai-dev\|arc1`, `-AllowWrites`, `-DryRun` |

## Password chain

1. `SAP_PASSWORD` in the process environment.
2. Windows Credential Manager target `sap-mcp:<profile>`.
3. Credential dialog (fallback; the MCP startup has ~30 s).

The launcher verifies that the stored username matches the profile and refuses a
mismatch instead of trying the wrong account.

```powershell
~\.config\opencode\sap\store-sap-secret.ps1 -Profile luf-ds4-100
~\.config\opencode\sap\store-sap-secret.ps1 -List
~\.config\opencode\sap\store-sap-secret.ps1 -Profile luf-ds4-100 -Remove
```

After an SAP password change: re-store, then restart the MCP server (toggle the
entry or restart OpenCode). A 401 means re-store; never retry the old password.

## Security

- No plaintext password in `opencode.json`, `profiles.json`, or a dotenv file.
- Windows DPAPI protects the credential at rest; any process running as the same
  Windows user can still read it, as with any keychain.
- If a password was ever in a plaintext file, rotate it in SAP first.
