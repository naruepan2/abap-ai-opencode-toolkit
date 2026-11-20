#Requires -Version 5.1
<#
.SYNOPSIS
    Wire the ABAP AI OpenCode Toolkit into a Windows OpenCode installation.

.DESCRIPTION
    Idempotent installer. It does seven things and nothing else:

      1. create the instance directory (<root>\workspace) and seed it
      2. point ~\.config\opencode\memory at <root>\workspace\memory (a junction)
      3. register plugins\tool-snapshot in ~\.config\opencode\opencode.json
      4. add a pointer block to ~\.config\opencode\AGENTS.md
      5. copy the personal skills in config\opencode-skills when the name is new
      6. write the registry baseline (registry_check.py --init)
      7. copy the SAP launcher and an example profile (-WithSap)

    It never touches your SAP profiles, credentials, or MCP entries.
    Every file it rewrites gets a timestamped .bak next to it.

.PARAMETER Root
    Toolkit root. Defaults to the folder this script lives in.

.PARAMETER ConfigDir
    OpenCode config directory. Defaults to ~\.config\opencode.

.PARAMETER Seed
    Copy templates\instance into the workspace when a file is missing.

.PARAMETER SkipRegistry
    Do not run registry_check.py --init.

.PARAMETER DryRun
    Print every action, change nothing.

.EXAMPLE
    .\install.ps1 -DryRun

.EXAMPLE
    .\install.ps1 -Seed
#>
[CmdletBinding()]
param(
    [string]$Root = $PSScriptRoot,
    [string]$ConfigDir = (Join-Path $HOME '.config\opencode'),
    [switch]$Seed,
    [switch]$SkipRegistry,
    [switch]$WithSap,
    [switch]$SkipAgents,
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
function WriteText([string]$path, [string]$text, [switch]$Append) {
    if ($Append) { [System.IO.File]::AppendAllText($path, $text, $utf8NoBom) }
    else { [System.IO.File]::WriteAllText($path, $text, $utf8NoBom) }
}

function Say([string]$text) { Write-Host $text }
function Act([string]$text) { if ($DryRun) { Write-Host "  would  $text" } else { Write-Host "  ok     $text" } }
function MoveAside([string]$path) {
    if ($DryRun) { Say "  would  back up $path"; return }
    $bak = "$path.bak-{0:yyyyMMdd-HHmmss}" -f (Get-Date)
    Copy-Item $path $bak -Force
    Say "  backup $bak"
}

# ---------------------------------------------------------------- preconditions
if (-not $Root) { $Root = (Get-Location).Path }
if (-not (Test-Path (Join-Path $Root 'scripts\session_context.py'))) {
    throw "not a toolkit root: $Root (scripts\session_context.py is missing)"
}
$Root = (Resolve-Path $Root).Path
if (-not (Test-Path $ConfigDir)) {
    if ($DryRun) { Say "  would  create $ConfigDir" } else { New-Item -ItemType Directory -Force -Path $ConfigDir | Out-Null }
}

$workspace = Join-Path $Root 'workspace'
$memory = Join-Path $workspace 'memory'
$slashRoot = $Root -replace '\\', '/'

Say "toolkit  $Root"
Say "config   $ConfigDir"
if ($DryRun) { Say "mode     dry run" }

# ------------------------------------------------------------------- 1. instance
Say ''
Say '[1/7] instance'
if (-not (Test-Path $memory)) {
    if ($DryRun) { Say "  would  create workspace\memory" }
    else {
        New-Item -ItemType Directory -Force -Path $memory | Out-Null
        New-Item -ItemType Directory -Force -Path (Join-Path $workspace 'specs') | Out-Null
        Say '  mkdir  workspace\memory, workspace\specs'
    }
} else {
    Say '  ok     workspace\memory'
}
$seedSource = Join-Path $Root 'templates\instance'
if ($Seed -and (Test-Path $seedSource)) {
    Get-ChildItem $seedSource -Recurse -File | ForEach-Object {
        $rel = $_.FullName.Substring($seedSource.Length + 1)
        $dst = Join-Path $workspace $rel
        if (Test-Path $dst) { Say "  keep   workspace\$rel" }
        elseif ($DryRun) { Say "  would  seed workspace\$rel" }
        else {
            New-Item -ItemType Directory -Force -Path (Split-Path -Parent $dst) | Out-Null
            Copy-Item $_.FullName $dst
            Say "  seed   workspace\$rel"
        }
    }
} elseif (-not (Test-Path (Join-Path $memory 'README.md'))) {
    Say '  note   workspace\memory has no README.md; run again with -Seed'
}

# ------------------------------------------------------------------- 2. junction
Say ''
Say '[2/7] memory junction'
$link = Join-Path $ConfigDir 'memory'
if (Test-Path $link) {
    $item = Get-Item $link -Force
    if ($item.LinkType -ne 'Junction') {
        throw "$link exists and is not a junction; move it away, then run this installer again"
    }
    $current = @($item.Target)[0]
    if ($current -ieq $memory) {
        Say '  ok     already points at this workspace'
    } else {
        Say "  change $current -> $memory"
        if (-not $DryRun) {
            [System.IO.Directory]::Delete($link)
            New-Item -ItemType Junction -Path $link -Target $memory | Out-Null
        }
    }
} else {
    Act "junction $link -> $memory"
    if (-not $DryRun) { New-Item -ItemType Junction -Path $link -Target $memory | Out-Null }
}

# --------------------------------------------------------------------- 3. plugin
Say ''
Say '[3/7] tool-snapshot plugin'
$configPath = Join-Path $ConfigDir 'opencode.json'
$package = "$slashRoot/plugins/tool-snapshot"
$config = $null
if (Test-Path $configPath) {
    try {
        $config = Get-Content $configPath -Raw -Encoding UTF8 | ConvertFrom-Json
    } catch {
        Say "  skip   cannot parse $configPath (JSON with comments?); add the plugin by hand:"
        Say "         { `"package`": `"$package`", `"options`": { `"workspace`": `"$slashRoot`" } }"
    }
} elseif (-not $DryRun) {
    $config = [pscustomobject]@{ '$schema' = 'https://opencode.ai/config.json' }
}
if ($null -ne $config) {
    $plugins = @()
    if ($config.PSObject.Properties.Name -contains 'plugins') { $plugins = @($config.plugins) }
    $hit = $plugins | Where-Object { $_.package -eq $package }
    if ($hit) {
        if ($hit.options -and $hit.options.workspace -eq $slashRoot) {
            Say '  ok     already registered'
        } elseif ($DryRun) {
            Say '  would  update options.workspace'
        } else {
            MoveAside $configPath
            $hit | Add-Member -Force -NotePropertyName options -NotePropertyValue ([pscustomobject]@{ workspace = $slashRoot })
            $config | Add-Member -Force -NotePropertyName plugins -NotePropertyValue $plugins
            WriteText $configPath ($config | ConvertTo-Json -Depth 20)
            Say '  update options.workspace'
        }
    } elseif ($DryRun) {
        Say "  would  register $package"
    } else {
        if (Test-Path $configPath) { MoveAside $configPath }
        $plugins += [pscustomobject]@{ package = $package; options = [pscustomobject]@{ workspace = $slashRoot } }
        $config | Add-Member -Force -NotePropertyName plugins -NotePropertyValue $plugins
        WriteText $configPath ($config | ConvertTo-Json -Depth 20)
        Say "  register $package"
    }
}

# ---------------------------------------------------------------------- 4. AGENTS
Say ''
Say '[4/7] global AGENTS.md pointer'
$agentsPath = Join-Path $ConfigDir 'AGENTS.md'
$marker = '<!-- abap-ai-opencode-toolkit -->'
$endMarker = '<!-- /abap-ai-opencode-toolkit -->'
$blockTemplate = @'
__MARKER__
## Memory (one call at session start)

The toolkit is at `__ROOT__`. Its digest is the first call of a session:

    python "__ROOTWIN__\scripts\session_context.py"

It prints the active project's resume card, memory and registry health, the open
inbox rows, the knowledge inventory, and the curated tool rules. Then pick a tier:

| Tier  | When                              | Read                       |
|-------|-----------------------------------|----------------------------|
| light | question, analysis, review        | the digest only            |
| task  | code, file, or SAP work           | digest + the project card  |
| deep  | new project, incident, design     | digest + every memory file |

Capture a correction in `workspace\memory\corrections.md` the moment it happens.
At close-out, consolidate each row into `workspace\memory\knowledge\<domain>.md`
and run `python "__ROOTWIN__\scripts\closeout.py"`.
__END__
'@
$block = $blockTemplate.Replace('__MARKER__', $marker).Replace('__END__', $endMarker).Replace('__ROOTWIN__', $Root).Replace('__ROOT__', $slashRoot)
if ($SkipAgents) {
    Say '  skip   -SkipAgents'
} elseif (Test-Path $agentsPath) {
    $text = Get-Content $agentsPath -Raw -Encoding UTF8
    if ($text -like "*$marker*") {
        Say '  ok     pointer block present'
    } elseif ($DryRun) {
        Say '  would  append the pointer block'
    } else {
        MoveAside $agentsPath
        WriteText $agentsPath "`r`n$block" -Append
        Say '  append the pointer block'
    }
} elseif ($DryRun) {
    Say "  would  create $agentsPath with the pointer block"
} else {
    WriteText $agentsPath $block
    Say '  create AGENTS.md with the pointer block'
}

# ---------------------------------------------------------------------- 5. skills
# Personal skills written for this toolkit, not vendor copies. They ship in the repo so
# a fresh machine gets them back; an existing name is kept, never overwritten.
Say ''
Say '[5/7] skills, agents and commands'
$skillsSrc = Join-Path $Root 'config\opencode-skills'
$skillsDst = Join-Path $ConfigDir 'skills'
if (Test-Path $skillsSrc) {
    if (-not (Test-Path $skillsDst) -and -not $DryRun) {
        New-Item -ItemType Directory -Force -Path $skillsDst | Out-Null
    }
    foreach ($skill in Get-ChildItem $skillsSrc -Directory) {
        $dstDir = Join-Path $skillsDst $skill.Name
        $dstFile = Join-Path $dstDir 'SKILL.md'
        if (Test-Path $dstFile) {
            Say "  keep   skills\$($skill.Name)"
        } elseif ($DryRun) {
            Say "  would  copy skills\$($skill.Name) (all files)"
        } else {
            New-Item -ItemType Directory -Force -Path $dstDir | Out-Null
            # A skill can ship references/ and scripts/ beside SKILL.md; copy the whole tree.
            Get-ChildItem $skill.FullName -Recurse -File | Where-Object { $_.FullName -notmatch '__pycache__' } | ForEach-Object {
                $rel = $_.FullName.Substring($skill.FullName.Length + 1)
                $target = Join-Path $dstDir $rel
                New-Item -ItemType Directory -Force -Path (Split-Path -Parent $target) | Out-Null
                Copy-Item -LiteralPath $_.FullName -Destination $target -Force
            }
            Say "  copy   skills\$($skill.Name) (all files)"
        }
    }
}

# Agent and command files: same "new name only" rule, so a user edit is never overwritten.
foreach ($pair in @(
    @{ src = 'config\opencode-agents'; dst = 'agents' },
    @{ src = 'config\opencode-commands'; dst = 'commands' }
)) {
    $srcDir = Join-Path $Root $pair.src
    $dstDir = Join-Path $ConfigDir $pair.dst
    if (-not (Test-Path $srcDir)) { continue }
    if (-not (Test-Path $dstDir) -and -not $DryRun) { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
    foreach ($file in Get-ChildItem $srcDir -Filter '*.md' -File) {
        $target = Join-Path $dstDir $file.Name
        if (Test-Path $target) {
            Say "  keep   $($pair.dst)\$($file.Name)"
        } elseif ($DryRun) {
            Say "  would  copy $($pair.dst)\$($file.Name)"
        } else {
            Copy-Item -LiteralPath $file.FullName -Destination $target -Force
            Say "  copy   $($pair.dst)\$($file.Name)"
        }
    }
}

# ------------------------------------------------------------------- 6. registry
if (-not $SkipRegistry) {
    Say ''
    Say '[6/7] registry'
    if ($DryRun) {
        Say '  would  run registry_check.py --init'
    } else {
        Push-Location $Root
        try {
            python (Join-Path $Root 'scripts\registry_check.py') --init
        } finally {
            Pop-Location
        }
    }
}

# ------------------------------------------------------------------------ 7. SAP
if ($WithSap) {
    Say ''
    Say '[7/7] SAP launcher'
    $sapSrc = Join-Path $Root 'config\opencode-sap'
    $sapDst = Join-Path $ConfigDir 'sap'
    if (-not (Test-Path $sapDst) -and -not $DryRun) { New-Item -ItemType Directory -Force -Path $sapDst | Out-Null }
    foreach ($file in @('sap-cred.ps1', 'store-sap-secret.ps1', 'sap-mcp.ps1')) {
        $dst = Join-Path $sapDst $file
        if (Test-Path $dst) { Say "  keep   sap\$file" }
        elseif ($DryRun) { Say "  would  copy sap\$file" }
        else { Copy-Item (Join-Path $sapSrc $file) $dst; Say "  copy   sap\$file" }
    }
    $profiles = Join-Path $sapDst 'profiles.json'
    if (-not (Test-Path $profiles)) {
        if ($DryRun) { Say '  would  create sap\profiles.json from the example' }
        else { Copy-Item (Join-Path $sapSrc 'profiles.example.json') $profiles; Say '  create sap\profiles.json (edit it: url, client, user)' }
    } else {
        Say '  keep   sap\profiles.json'
    }
    Say '  next   store the password: sap\store-sap-secret.ps1 -Profile <name>'
}

# ------------------------------------------------------------------------- done
Say ''
if ($DryRun) {
    Say 'dry run: nothing was changed.'
} else {
    Say 'done. Restart OpenCode once, then run:'
    Say "  python `"$Root\scripts\session_context.py`""
}
