#Requires -Version 5.1
<#
.SYNOPSIS
    Back up the OpenCode instance data and user config to a dated folder.

.DESCRIPTION
    Three sources, one snapshot folder:

      1. workspace/ (memory cards, corrections, knowledge, specs mirror, reports)
         - the instance data that git ignores and is most likely to be lost.
      2. ~/.config/opencode, minus the memory junction, stale .bak files,
         vendor clones and the SAP GUI audit log (all re-creatable or stale).
      3. optional: the OpenCode session database (three files together).

    Every copied file is hash-verified against its source. A manifest with
    counts and failures (names/hashes only, no file contents) is written to
    the snapshot root. Nothing is deleted from the sources.

.PARAMETER Destination
    Parent folder for the snapshot. Defaults to ~/Backups/opencode.

.PARAMETER ConfigDir
    OpenCode config directory. Defaults to ~/.config/opencode.

.PARAMETER IncludeSessions
    Also copy opencode.db, opencode.db-wal and opencode.db-shm. Close OpenCode
    first, or the SQLite WAL may be inconsistent.

.PARAMETER DryRun
    Print the plan, change nothing.

.EXAMPLE
    .\scripts\backup_opencode.ps1 -DryRun

.EXAMPLE
    .\scripts\backup_opencode.ps1 -Destination E:\Backup\opencode -IncludeSessions

.NOTES
    Restore order: clone the repo -> install.ps1 -Seed -> restore workspace/
    at the same path (or set ABAP_WORKSPACE) -> restore config files without
    overwriting newer ones -> recreate junctions listed in manifest.json
    (New-Item -ItemType Junction -Path <source> -Target <target>; the skill
    targets are separate git repos) -> restore session/ files -> re-store SAP
    secrets with sap\store-sap-secret.ps1 -> session_context.py + registry_check.py.
#>
[CmdletBinding()]
param(
    [string]$Destination = (Join-Path $HOME 'Backups\opencode'),
    [string]$ConfigDir = (Join-Path $HOME '.config\opencode'),
    [switch]$IncludeSessions,
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$workspace = if ($env:ABAP_WORKSPACE) { (Resolve-Path $env:ABAP_WORKSPACE).Path }
             else { Join-Path $repoRoot 'workspace' }
$dataDir = Join-Path $HOME '.local\share\opencode'
$configExcludeDirs = @('memory', 'memory.live-backup-*', 'abap-skills', 'open-computer-use', 'plugins')
$configExcludeFiles = @('*.bak*', 'sap-gui-audit.jsonl')
$sessionFiles = @('opencode.db', 'opencode.db-wal', 'opencode.db-shm')

function Copy-Tree([string]$src, [string]$dst, [string[]]$xd, [string[]]$xf) {
    if (-not (Test-Path -LiteralPath $src)) { throw "missing source: $src" }
    if ($DryRun) { Write-Host "  would  robocopy $src -> $dst"; return }
    New-Item -ItemType Directory -Force -Path $dst | Out-Null
    # /XJ: junctions in skills/ point at separate git repos; copy the link, not the target.
    $args = @($src, $dst, '/E', '/XJ', '/R:1', '/W:1', '/NFL', '/NDL', '/NJH', '/NJS', '/NP')
    if ($xd) { $args += @('/XD') + $xd }
    if ($xf) { $args += @('/XF') + $xf }
    & robocopy @args | Out-Null
    $rc = $LASTEXITCODE
    if ($rc -ge 8) { throw "robocopy failed ($rc): $src -> $dst" }
    Write-Host ("  copy   {0} -> {1}" -f (Split-Path $src -Leaf), (Split-Path $dst -Leaf))
}

function Verify-Copy([string]$src, [string]$dst) {
    if ($DryRun) { return @() }
    $bad = @()
    foreach ($f in (Get-ChildItem -LiteralPath $dst -Recurse -File -Force)) {
        $rel = $f.FullName.Substring($dst.Length + 1)
        $origin = Join-Path $src $rel
        if (-not (Test-Path -LiteralPath $origin)) {
            $bad += "orphan: $rel"
            continue
        }
        $a = (Get-FileHash -LiteralPath $origin -Algorithm SHA256).Hash
        $b = (Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256).Hash
        if ($a -ne $b) { $bad += "hash: $rel" }
    }
    return $bad
}

$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$snap = Join-Path $Destination "opencode-$stamp"
Write-Host "backup   $stamp"
Write-Host "from     $workspace"
Write-Host "from     $ConfigDir"
Write-Host "to       $snap"

Copy-Tree $workspace (Join-Path $snap 'workspace') @() @()
Copy-Tree $ConfigDir (Join-Path $snap 'config') $configExcludeDirs $configExcludeFiles

$sessionBad = @()
$sessionUnverified = @()
if ($IncludeSessions) {
    $sessDst = Join-Path $snap 'session'
    if (-not $DryRun) { New-Item -ItemType Directory -Force -Path $sessDst | Out-Null }
    foreach ($name in $sessionFiles) {
        $srcFile = Join-Path $dataDir $name
        if (Test-Path -LiteralPath $srcFile) {
            if ($DryRun) { Write-Host "  would  copy $name" }
            else {
                try { Copy-Item -LiteralPath $srcFile -Destination (Join-Path $sessDst $name) -Force }
                catch { $sessionBad += "copy failed: session\$name"; continue }
                try {
                    $a = (Get-FileHash -LiteralPath $srcFile -Algorithm SHA256).Hash
                    $b = (Get-FileHash -LiteralPath (Join-Path $sessDst $name) -Algorithm SHA256).Hash
                    if ($a -ne $b) { $sessionBad += "hash: session\$name" }
                } catch {
                    $sessionUnverified += "session\$name (source locked - OpenCode still running)"
                }
                Write-Host "  copy   session\$name"
            }
        } else {
            Write-Host "  skip   session\$name (not present)"
        }
    }
}

$wsBad = Verify-Copy $workspace (Join-Path $snap 'workspace')
$cfgBad = Verify-Copy $ConfigDir (Join-Path $snap 'config')
$ok = ($wsBad.Count -eq 0 -and $cfgBad.Count -eq 0 -and $sessionBad.Count -eq 0)

# Junctions are not copied. Record them so a restore can recreate them; all of
# these targets are separate git repos except the memory junction.
$junctions = @()
foreach ($root in @($ConfigDir, $workspace)) {
    foreach ($j in (Get-ChildItem -LiteralPath $root -Recurse -Force -ErrorAction SilentlyContinue | Where-Object { $_.LinkType })) {
        $junctions += [ordered]@{
            source = $j.FullName.Substring($root.Length + 1)
            target = (@($j.Target) -join '; ')
        }
    }
}

if (-not $DryRun) {
    $manifest = [ordered]@{
        created_at       = (Get-Date).ToString('o')
        destination      = $snap
        workspace_source = $workspace
        config_source    = $ConfigDir
        included_session = [bool]$IncludeSessions
        config_excludes  = $configExcludeDirs + $configExcludeFiles
        junctions        = $junctions
        session_unverified = $sessionUnverified
        workspace_files  = (Get-ChildItem -LiteralPath (Join-Path $snap 'workspace') -Recurse -File -Force).Count
        config_files     = (Get-ChildItem -LiteralPath (Join-Path $snap 'config') -Recurse -File -Force).Count
        failures         = @($wsBad) + @($cfgBad) + @($sessionBad)
        ok               = $ok
        note             = 'SAP credentials live in Windows Credential Manager; re-store on the new machine. A session copy taken while OpenCode runs may be inconsistent; close it first.'
    }
    $manifest | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $snap 'manifest.json') -Encoding UTF8
}

Write-Host ("manifest {0}" -f (Join-Path $snap 'manifest.json'))
Write-Host ("verified {0}" -f $(if ($DryRun) { 'dry run' } elseif ($ok) { 'OK' } else { 'FAILED - see manifest' }))
if (-not $DryRun -and -not $ok) { exit 1 }
