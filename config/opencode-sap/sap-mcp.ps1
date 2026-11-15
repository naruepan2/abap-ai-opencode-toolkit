# sap-mcp.ps1 - one launcher for the ADT MCP engines, one connection profile.
#
# The MCP entry chooses the engine; the profile holds URL/user/client/CA once.
# Nothing credential-like is written to disk: the password is asked for by the
# standard Windows credential dialog at every server start and lives only in the
# process environment.
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
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'sap-cred.ps1')

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
            [Console]::Beep(1200, 250)
            $cred = Get-Credential -UserName $p.user -Message "SAP $Profile ($Engine)"
            if ($null -eq $cred) {
                [Console]::Error.WriteLine('credential dialog cancelled; server not started')
                exit 1
            }
            $password = $cred.GetNetworkCredential().Password
        }
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

