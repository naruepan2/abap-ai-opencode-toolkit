# SAP MCP launcher (versioned backup)

The live copies are in `~\.config\opencode\sap\` (outside git). This folder is the
backup of the generic scripts; **real** `profiles.json` (customer URLs, usernames)
stays local, and `profiles.example.json` shows the shape only.

| File | Purpose |
|---|---|
| `profiles.example.json` | profile shape: URL, client, user, system, destination, CA, package allowlist |
| `sap-cred.ps1` | Windows Credential Manager helper (`CredRead` / `CredWrite` / `CredDelete`) and the native sign-in dialog (`CredUIPromptForCredentials`) |
| `store-sap-secret.ps1` | store / list / remove the password for a profile |
| `sap-mcp.ps1` | launcher: `-Profile <name> -Engine ai-dev\|arc1`, `-AllowWrites`, `-DryRun`, `-PromptTest` |

## Password chain

1. `SAP_PASSWORD` in the process environment.
2. Windows Credential Manager target `sap-mcp:<profile>`.
3. The native Windows credential dialog (`SAP sign-in`, CredUI). What you type is
   written to Credential Manager, so the next start is silent. A named mutex makes
   two directories share one dialog instead of opening two.

The launcher verifies that the stored username matches the profile and refuses a
mismatch instead of trying the wrong account.

`mcp.timeout.startup` in `opencode.json` must allow time for the dialog: this
workspace sets 180000 ms (the default is 30 s). The value is global, not per entry;
the legacy `mcp.<name>` shape accepts only an integer `timeout` inside an entry, and
an object there makes the entry disappear.

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
