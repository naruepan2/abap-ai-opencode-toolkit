# store-sap-secret.ps1 - store / list / remove the SAP password for a profile.
#
#   .\store-sap-secret.ps1 -Profile luf-ds4-100     # store or update
#   .\store-sap-secret.ps1 -List                    # profiles that have a secret
#   .\store-sap-secret.ps1 -Profile luf-ds4-100 -Remove
#
# The password goes to Windows Credential Manager (DPAPI) under
#   sap-mcp:<profile>
# Nothing is written to a JSON or text file. Run this after an SAP password
# change, then restart the MCP server (toggle the entry or restart OpenCode).
param(
    [string]$Profile,
    [switch]$List,
    [switch]$Remove,
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'sap-cred.ps1')

$profilesPath = Join-Path $PSScriptRoot 'profiles.json'
$all = (Get-Content $profilesPath -Raw | ConvertFrom-Json).profiles

function TargetOf([string]$name) { "sap-mcp:$name" }

if ($List) {
    $found = 0
    foreach ($name in $all.PSObject.Properties.Name) {
        $user = $null
        $null = [SapCred]::ReadPassword((TargetOf $name), [ref]$user)
        if ($user) {
            Write-Output ("{0,-16} {1}  ({2})" -f $name, (TargetOf $name), $user)
            $found++
        }
    }
    if ($found -eq 0) { Write-Output 'no stored SAP secrets' }
    exit 0
}

if (-not $Profile) {
    [Console]::Error.WriteLine('use -Profile <name>, -List, or -Profile <name> -Remove')
    exit 1
}
$p = $all.$Profile
if ($null -eq $p) {
    [Console]::Error.WriteLine("unknown profile: $Profile")
    exit 1
}

$target = TargetOf $Profile

if ($Remove) {
    if ($DryRun) { [Console]::Error.WriteLine("would delete $target"); exit 0 }
    if ([SapCred]::Delete($target)) {
        Write-Output "removed $target"
        exit 0
    }
    $code = [Runtime.InteropServices.Marshal]::GetLastWin32Error()
    if ($code -eq 1168) { Write-Output "no secret stored for $target"; exit 0 }
    [Console]::Error.WriteLine("delete failed (win32 $code)")
    exit 1
}

if ($DryRun) {
    [Console]::Error.WriteLine("would store $target for user $($p.user)")
    exit 0
}

$cred = Get-Credential -UserName $p.user -Message "SAP $Profile - store in Windows Credential Manager"
if ($null -eq $cred) {
    [Console]::Error.WriteLine('cancelled; nothing stored')
    exit 1
}

$password = $cred.GetNetworkCredential().Password
if ([SapCred]::Write($target, $cred.UserName, $password)) {
    Write-Output "stored $target for $($cred.UserName)"
    exit 0
}
$code = [Runtime.InteropServices.Marshal]::GetLastWin32Error()
[Console]::Error.WriteLine("store failed (win32 $code)")
exit 1
