# sap-mcp.ps1 - one launcher for the ADT MCP engines, one connection profile.
#
# The MCP entry chooses the engine; the profile holds URL/user/client/CA once.
# Nothing credential-like is written to disk: the password comes from SAP_PASSWORD,
# then Windows Credential Manager, then a top-most dialog that stores what you type
# (so the next start is silent). The keychain entry is a DPAPI-protected generic
# credential named sap-mcp:<profile>.
#
#   powershell -NoProfile -ExecutionPolicy Bypass -File sap-mcp.ps1 `
#       -Profile luf-ds4-100 -Engine ai-dev
#   ... -Engine arc1 -AllowWrites        # ARC-1 writes, use one writer per task
#   ... -DryRun                          # print the resolved settings to stderr
#
param(
    [Parameter(Mandatory = $true)][string]$Profile,
    [Parameter(Mandatory = $true)][ValidateSet('ai-dev', 'arc1')][string]$Engine,
    [switch]$AllowWrites,
    [switch]$DryRun,
    [switch]$PromptTest
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'sap-cred.ps1')

function Show-SapPrompt {
    param([string]$ProfileName, [string]$UserName, [string]$EngineName, [string]$SystemUrl)

    [Console]::Beep(1200, 250)
    $message = "SAP $ProfileName ($EngineName)`r`n$UserName - $SystemUrl"
    $result = [SapCred]::Prompt("sap-mcp:$ProfileName", 'SAP sign-in', $message, $UserName)
    if ($null -eq $result) { return $null }
    return $result[1]
}

$profilesPath = Join-Path $PSScriptRoot 'profiles.json'
if (-not (Test-Path $profilesPath)) {
    [Console]::Error.WriteLine("profiles.json not found next to sap-mcp.ps1")
    exit 1
}
$all = (Get-Content $profilesPath -Raw | ConvertFrom-Json).profiles
$p = $all.$Profile
if ($null -eq $p) {
    [Console]::Error.WriteLine("unknown profile: $Profile")
    exit 1
}

if ($PromptTest) {
    $entered = Show-SapPrompt $Profile $p.user $Engine ([string]$p.url)
    if ($null -eq $entered) {
        [Console]::Error.WriteLine('prompt cancelled; nothing stored')
        exit 1
    }
    [Console]::Error.WriteLine("prompt ok: $($entered.Length) characters, not stored")
    exit 0
}

$target = "sap-mcp:$Profile"
$passwordSource = ''
$password = $null
if ($env:SAP_PASSWORD) {
    $password = $env:SAP_PASSWORD
    $passwordSource = 'env'
} else {
    $storedUser = $null
    $stored = [SapCred]::ReadPassword($target, [ref]$storedUser)
    if ($stored) {
        if ($storedUser -and $storedUser -ne $p.user) {
            [Console]::Error.WriteLine("credential stored for '$storedUser' but profile expects '$($p.user)'; re-store with store-sap-secret.ps1 -Profile $Profile")
            exit 1
        }
        $password = $stored
        $passwordSource = 'credential-manager'
    } else {
        $passwordSource = 'dialog'
        if ($DryRun) {
            $password = '<would-prompt>'
        } else {
            # Only one dialog per profile: a second directory starts the same server
            # and must wait for the first one to store the credential instead of
            # opening a duplicate window.
            $mutex = New-Object System.Threading.Mutex($false, "Local\sap-mcp-prompt-$Profile")
            $haveLock = $false
            try {
                try {
                    $haveLock = $mutex.WaitOne([TimeSpan]::FromSeconds(110))
                } catch [System.Threading.AbandonedMutexException] {
                    $haveLock = $true
                }
                $storedUser = $null
                $stored = [SapCred]::ReadPassword($target, [ref]$storedUser)
                if ($stored -and (-not $storedUser -or $storedUser -eq $p.user)) {
                    $password = $stored
                    $passwordSource = 'credential-manager'
                } elseif (-not $haveLock) {
                    [Console]::Error.WriteLine('credential dialog is open in another window and did not finish; server not started')
                    exit 1
                } else {
                    $entered = Show-SapPrompt $Profile $p.user $Engine ([string]$p.url)
                    if ($null -eq $entered) {
                        [Console]::Error.WriteLine('credential dialog cancelled; server not started')
                        exit 1
                    }
                    $password = $entered
                    if ([SapCred]::Write($target, $p.user, $entered)) {
                        $passwordSource = 'dialog+stored'
                        [Console]::Error.WriteLine("password stored as $target; the next start will not ask")
                    }
                }
            } finally {
                if ($haveLock) { $mutex.ReleaseMutex() }
                $mutex.Dispose()
            }
        }
    }
}

# Always say where the password came from: a stale SAP_PASSWORD in the parent
# process silently overrides the keychain, and that is invisible in the MCP logs.
[Console]::Error.WriteLine("sap-mcp: profile=$Profile engine=$Engine password=$passwordSource")
if ($passwordSource -eq 'env') {
    $storedUser = $null
    $stored = [SapCred]::ReadPassword($target, [ref]$storedUser)
    if ($stored -and $stored -ne $password) {
        [Console]::Error.WriteLine("warning: SAP_PASSWORD differs from the credential stored for $target; the environment wins. Unset SAP_PASSWORD to use the keychain.")
    }
}

$env:SAP_URL = [string]$p.url
$env:SAP_USER = [string]$p.user
$env:SAP_PASSWORD = $password
$env:SAP_CLIENT = [string]$p.client
$env:SAP_LANGUAGE = [string]$p.language
if ($p.tls_ca) { $env:NODE_EXTRA_CA_CERTS = [string]$p.tls_ca }

if ($Engine -eq 'ai-dev') {
    $env:SAP_ALLOW_TRANSPORTABLE_EDITS = 'true'
    $env:SAP_AI_DEV_TOOLKIT_DESTINATION_SOURCE = 'sap-gui-local'
    $env:SAP_AI_DEV_TOOLKIT_DESTINATION = [string]$p.destination
    $env:SAP_SYSTEM_ID = [string]$p.system_id
    $env:SAP_AUTH_MODE = 'basic'
    $env:SAP_AI_DEV_TOOLKIT_VERSION = '0.9.9928'
    if ($p.tls_ca) {
        $env:SAP_TLS_SERVER_NAMES = ([uri]$p.url).Host
        $env:SAP_TLS_CA_FILE = [string]$p.tls_ca
        $env:SAP_AI_DEV_TOOLKIT_TLS_CA_FILE = [string]$p.tls_ca
    }
    if ($DryRun) {
        [Console]::Error.WriteLine("profile=$Profile engine=$Engine url=$($p.url) client=$($p.client) user=$($p.user) destination=$($p.destination) password=$passwordSource writes=env-managed")
        exit 0
    }
    & 'sap-ai-dev.cmd'
    exit $LASTEXITCODE
}

$env:SAP_ALLOWED_PACKAGES = [string]$p.allowed_packages
if ($AllowWrites) {
    $env:SAP_ALLOW_WRITES = 'true'
} else {
    $env:SAP_ALLOW_WRITES = 'false'
}
$env:SAP_ALLOW_TRANSPORT_WRITES = 'false'
$env:SAP_ALLOW_DATA_PREVIEW = 'false'
$env:SAP_ALLOW_FREE_SQL = 'false'
$env:SAP_ALLOW_GIT_WRITES = 'false'
$env:ARC1_TOOL_MODE = 'standard'

if ($DryRun) {
    [Console]::Error.WriteLine("profile=$Profile engine=$Engine url=$($p.url) client=$($p.client) user=$($p.user) password=$passwordSource writes=$($env:SAP_ALLOW_WRITES) packages=$($env:SAP_ALLOWED_PACKAGES)")
    exit 0
}

& "$env:APPDATA\npm\arc1.cmd"
exit $LASTEXITCODE

