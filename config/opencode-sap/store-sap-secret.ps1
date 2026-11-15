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
    [switch]$NoVerify,
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

function Test-SapAuth([string]$Url, [string]$UserName, [string]$Password, [string]$Client) {
    $pair = '{0}:{1}' -f $UserName, $Password
    $basic = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($pair))
    $probe = $Url.TrimEnd('/') + '/sap/bc/adt/discovery?sap-client=' + $Client
    try {
        $null = Invoke-WebRequest -Uri $probe -Headers @{ Authorization = "Basic $basic" } -UseBasicParsing -TimeoutSec 25
        return 'ok'
    } catch {
        $status = $null
        if ($_.Exception.Response) { $status = [int]$_.Exception.Response.StatusCode }
        if ($status -eq 401) { return 'denied' }
        if ($status) {
            $body = ''
            try {
                $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
                $body = $reader.ReadToEnd()
                $reader.Dispose()
            } catch { }
            $body = ($body -replace '\s+', ' ').Trim()
            if ($body.Length -gt 160) { $body = $body.Substring(0, 160) }
            return "http $status $body"
        }
        return 'unreachable'
    }
}

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

[Console]::Beep(1200, 250)
$result = [SapCred]::Prompt($target, 'SAP sign-in', "Store the SAP password for $Profile ($($p.user)) in Windows Credential Manager.", $p.user)
if ($null -eq $result) {
    [Console]::Error.WriteLine('cancelled; nothing stored')
    exit 1
}

$password = $result[1]
if (-not [SapCred]::Write($target, $result[0], $password)) {
    $code = [Runtime.InteropServices.Marshal]::GetLastWin32Error()
    [Console]::Error.WriteLine("store failed (win32 $code)")
    exit 1
}
Write-Output "stored $target for $($result[0])"

# Verify after storing, never before: only a clear 401 removes the credential again.
# A 400 or a network error is ambiguous (proxy, ICM, an endpoint that rejects the
# request shape), so it must not block a password the user asked to store.
if (-not $NoVerify) {
    $check = Test-SapAuth ([string]$p.url) $result[0] $password ([string]$p.client)
    if ($check -eq 'denied') {
        [SapCred]::Delete($target) | Out-Null
        [Console]::Error.WriteLine("SAP rejected that password for $($result[0]) on client $($p.client); credential removed again")
        exit 1
    }
    if ($check -eq 'ok') {
        Write-Output "verified against $($p.url) client $($p.client)"
    } else {
        Write-Output "warning: could not verify ($check); the credential is stored and the MCP will be the judge"
    }
}
exit 0
