---
name: sap-mcp-upgrade
description: Check and upgrade MCP servers installed in OpenCode in one pass. Use for "upgrade MCP", "bump pin", "check MCP version", "what needs updating", "MCP pin drift". OpenCode-only, standalone: no other harness, no skill install suggestions.
---

# SAP MCP upgrade

**Batch-first + OpenCode-only.** Scan the MCP entries in the OpenCode config and
their backing packages, compare with upstream in one pass, present one report,
ask one approval, apply all non-breaking updates, restart the daemon once,
verify once, restore once. The live OpenCode config is the target; upstream
release data is the source of truth. Memory of a last version is not evidence.

The catalog plan lives in `docs/plan-mcp-pins.md`. Until it is executed, use the
manual commands below. Do not call a script that does not exist.

## Manual-only trigger

Never run this skill at session start, from the digest, on a timer, or as
background maintenance. Invoke it **only** when the user explicitly asks to
check or upgrade something ("upgrade MCP", "bump pin", "check MCP version",
"what needs updating"). A passing mention is not an invocation — ask first.
No cron, no scheduled task, no auto-update daemon.

The one-pass scan is read-only, but it still costs tool calls and tokens. That
cost is paid only on an explicit user request.

## Scope — OpenCode MCP only

In scope:

- `mcp` entries in `~/.config/opencode/opencode.json`
- the package or hosted endpoint backing each of those entries

Out of scope — do not scan, report as updatable, or suggest installing:

- skills or agents from VS Code / Copilot / Claude / other harnesses
- parked skills, personal skills, or any skill install
- agents of any harness
- npm/uvx/uv tools that do not back an OpenCode MCP entry

If such an item appears incidentally, say "not managed by this skill" and move
on. Never ask whether to install a skill from another harness.

## Stop first

Ask before any of these:

- editing `~/.config/opencode/opencode.json`
- installing or upgrading a package
- restarting the opencode service daemon
- connecting to SAP
- adding a new MCP entry to the registry below

Never kill an MCP process to force a reload — the namespace disappears for the
rest of the session. A task-scoped server stays `enabled:false` in the steady
state; enable it only for the task that needs it, then set it back.

## Known-MCP registry (static fallback)

Use this table to avoid asking "which one?". An MCP entry not listed here is
found by discovery (below) and added only with approval.

| MCP entry(ies) | Pin location | Probe (read-only) | Source |
|---|---|---|---|
| `ai-dev-*` (ds4-100/900, sus-100, gsd-120) | env `SAP_AI_DEV_TOOLKIT_VERSION` in `sap-mcp.ps1` (0.9.9928) | `https://registry.npmjs.org/sap-ai-dev-toolkit/latest` | github.com/grknylmz/sap-ai-dev-toolkit |
| `arc1-*` (ds4-100, sus-100, gsd-110) | npm global, unpinned (1.10.1) | `https://registry.npmjs.org/arc-1/latest` | github.com/arc-mcp/arc-1 |
| `sap-gui` | `mcp-sap-gui[screenshots]==0.6.1` in config command | `https://pypi.org/pypi/mcp-sap-gui/json` | github.com/kts982/mcp-sap-gui |
| `sap-abap-docs` (replaced `sap-docs`/`sap-ui5-docs`) | hosted HTTP, no local pin | endpoint status / release notes | github.com/marianfoo/abap-mcp-server |
| `playwright` | npm global, unpinned | `https://registry.npmjs.org/@playwright/mcp/latest` | github.com/microsoft/playwright-mcp |
| `open-computer-use` | npm global, unpinned | `https://registry.npmjs.org/open-computer-use/latest` | github.com/iFurySt/open-computer-use |
| `windows-mcp` (disabled) | uv tool, unpinned (0.9.0) | `https://pypi.org/pypi/windows-mcp/json` | github.com/CursorTouch/Windows-MCP; OpenCode 2.4.0 rejects its MCP handshake |
| `browse` | self-updating CLI (`browse --version`) + npm `@opencode/browse` | `browse status`, Anomaly release channel | github.com/anomalyco/browse |
| `opencode_console`, `browser`, built-ins | none | n/a | github.com/anomalyco/opencode |

One package can back several MCP entries (e.g. `ai-dev-*`). Upgrade the package
**once**, not once per entry.

Remote HTTP MCP entries must use `"type": "remote"` plus `url`. A `"type": "http"` entry
is silently ignored by OpenCode — it does not appear even in `opencode mcp list`. Verify an
addition with `opencode mcp list` before recording it as installed.

## 1. One-pass discovery + scan — read only

```powershell
python scripts\registry_check.py --check --brief
python scripts\tools_now.py
# read the mcp object from ~/.config/opencode/opencode.json
npm ls -g --depth=0
uv tool list          # only to resolve versions of backing packages above
browse --version      # only for the browse MCP entry
```

For each **OpenCode MCP entry** record:

```
name | current | latest | source | probe | severity | status | action
```

- status `KNOWN`: in the registry above → probe upstream.
- status `NEW` (an MCP entry in opencode.json with no registry row) →
  `UNVERIFIED`; group all such entries into **one** question asking for their
  source. Never ask one by one, and never offer to install a skill.
- parked/disabled MCP entries are reported but never enabled by the scan.
- if the pending-restart state file lists this entry, status becomes
  `RESTART_PENDING` regardless of version — resolve that first (below).

### Severity tiers

Classify from the changelog/advisory, never from the version number alone:

| Severity | Trigger | Batch rule |
|---|---|---|
| `security` | CVE / GHSA / security advisory / "security fix" | **never batched** — separate explicit approval |
| `breaking` | renamed/removed tool or argument | **never batched** — separate approval + possible tool/KB edit |
| `routine` | bugfix, feature, dependency bump | included in the one batch |

If the changelog is silent or ambiguous, mark `routine?` with `UNVERIFIED` —
do not silently promote an unknown update to `security`.

**Terminal case:** if no MCP entry is behind and no new MCP entry needs a source:
- pending restart exists → report "restart pending for N entries" and ask only
  the restart question;
- otherwise → report "all OpenCode MCP entries current, no new entries" with the
  table and STOP.

Do not ask "update anything else?" — that question is what this design removes.

## 1b. Present the pre-update report — read only

Before asking any approval question, show the full report so the user can
cross-check every claim:

```text
## MCP upgrade report — read-only, nothing changed yet

| MCP entry | current | latest | severity | status | source | probe URL | changelog URL |
|---|---|---|---|---|---|---|---|
| sap-gui | 0.6.1 | 0.6.1 | - | CURRENT | github.com/kts982/mcp-sap-gui | https://pypi.org/pypi/mcp-sap-gui/json | .../CHANGELOG.md |
| playwright | 0.0.85 | 0.0.86 | routine? | UPDATE | github.com/microsoft/playwright-mcp | https://registry.npmjs.org/@playwright/mcp/latest | .../releases/tag/v0.0.86 |
```

- Include **every** OpenCode MCP entry, not only the ones behind — the user
  needs the "current" rows to trust the scan.
- Group by action: `UPDATE` / `CURRENT` / `UNVERIFIED` / `RESTART_PENDING` /
  `HOSTED`.
- Show the exact probe URL and changelog URL that produced each version claim.
  A GitHub repo link alone is not enough for cross-checking.
- State explicitly: **"No file, package or config has changed yet."**
- If the user wants detail on any row before deciding, show the read-only probe
  result or a short changelog excerpt. Do not apply anything during that step.

Only after this report is shown may the batch question in section 2 be asked.

## 1c. Safety ranking — computed automatically, never asked

From the evidence already gathered, assign each upgrade unit a safety rank and
show it before approval. No user input is needed for this step.

| Rank | Auto-assigned when | Meaning for the user |
|---|---|---|
| 1 — lowest | package-only, no config token, straightforward rollback | safe to batch; other clients using the same package also get the new version |
| 2 | preflight failed / skipped | not applied; reason shown, no re-ask |
| 3 | one package backs several MCP entries | must move as one unit; never select a single entry |
| 4 | a config token / pin must change | requires the config backup; token edited only after package resolves |
| 5 — highest | `security`, `breaking`, or `routine?` | never in `Upgrade all` — separate explicit approval |

Show a compact table with: `rank | unit | blast radius | config change |
rollback | confidence | impact note`. State the auto apply order:

```
preflight all → install package units (lowest rollback cost first)
→ edit config tokens after resolve → one daemon restart → verify per item
```

Never ask the user to rank safety or supply impact data — derive it from the
probe/changelog/config evidence. This step costs zero additional questions.

## 2. Approval — radio mode first, checkbox only if selected

**Question budget:** 1 question for `Upgrade all`; 2 only if the user chooses
`Upgrade selected`. Safety ranking (section 1c) adds zero questions. Do not ask
anything else before section 3, and never ask again after a terminal result.

**Question 1 (radio, always asked):** `will you upgrade all, or select units?`

- `Upgrade all (Recommended)` — apply every **verified `routine`** unit that
  passed preflight, plus confirmed new registry rows. No second question:
  proceed straight to section 3. Recommended because it avoids an extra
  interaction/token cost when nothing needs a human decision.
- `Upgrade selected` — go to question 2 (checkbox) below.
- `Cancel` — end immediately; write no state and change nothing.

Never bundled into either mode: `routine?` (changelog ambiguous → needs an
explicit human choice), `security`, `breaking`, and `RESTART_PENDING`. Show them
in the report with the reason; they are not silently included in `Upgrade all`.

**Question 2 (checkbox, only when `Upgrade selected` was chosen):**

- List **upgrade units**, not individual MCP entries — one package can back
  several entries, so they move together.
- Pre-check only units that are `routine` + preflight-passed + not pending
  restart. Show disabled rows for `routine?` / `security` / `breaking` /
  `RESTART_PENDING` with the reason.
- Buttons: `Apply selected` / `Back`. `Back` returns to question 1 with no
  change. If no unit is selected, `Apply selected` is disabled.
- Selection is still one confirmation — do not ask per unit.

Other rules:

- `security` or `breaking` → separate dedicated approval per entry; a breaking
  tool/argument change may need a knowledge-base edit before its pin moves.
- Any `RESTART_PENDING` entry blocks new upgrades until resolved — ask once to
  restart the daemon first, then re-scan.
- Hosted/self-updating entries are reported, never manually bumped.

## 3. Apply once

1. Back up the live config once:

   ```powershell
   $cfg = "$env:USERPROFILE\.config\opencode\opencode.json"
   Copy-Item $cfg "$cfg.bak"
   ```

2. Edit **only** version tokens. Keep `enabled`, URL, profile and every other
   field exactly as they were.
3. Install/resolve with the manager already in the command. For `uvx`:

   ```powershell
   cmd /c "uvx mcp-sap-gui[screenshots]==0.6.1 --help >nul 2>&1"
   "EXIT=$LASTEXITCODE"
   ```

   Exit 0 means the package resolves, not that the server is connected.
4. Add approved registry rows to this file in the same change.
5. Ask once for an opencode **service daemon** restart. Restarting the window
   does not reload MCP entries.

## Pending-restart state

Machine-local state, never in the repo:
`~/.config/opencode/sap-mcp-upgrade-state.json`.

```json
{
  "generated_at": "2026-11-20T00:00:00Z",
  "entries": {
    "sap-gui": {
      "from": "0.6.1",
      "to": "0.7.0",
      "changed_at": "2026-11-20T00:00:00Z",
      "restart_pending": true,
      "verified": false
    }
  }
}
```

- After apply (step 3), write one entry per changed MCP entry with
  `restart_pending:true`, `verified:false`.
- On every scan, read this file **first**. `RESTART_PENDING` wins over version
  comparison and blocks new upgrades.
- After the daemon restart and step 4 pass, set `restart_pending:false`,
  `verified:true`; keep the entry with `changed_at` as history.
- Never drop history silently — prune only with explicit approval.

## 4. Verify all changed MCP entries in one pass

For every changed server, all four must pass before claiming success:

- catalog: expected namespace and tool count (`registry_check.py --check --brief`)
- process: running command line contains the new pin
  (`Get-CimInstance Win32_Process | Where-Object CommandLine -like '*<pkg>*'`)
- package metadata: installed distribution reports the new version
- one read-only call from that server (e.g. `sap_list_connections` for sap-gui)

A server that needs SAP requires user logon; then use `sap_connect_existing`.
A read-only answer is not proof a write will be confirmed.

Write the state file back with `restart_pending:false` and `verified:true` only
for entries that passed. Any failure stays `RESTART_PENDING` / `verified:false`
and is reported, not hidden.

## 5. Finish once

- `registry_check.py --refresh` only if the tool list changed.
- Update the evidence line in memory from old version to new.
- Set every task-scoped server back to `enabled:false`; ask for one final daemon
  restart if their state changed.
- Report: per-entry before/after, severity, source URL and verification results.
- If any state entry still has `restart_pending:true`, end with
  **"restart pending for N entries"** plus the single restart question — not the
  all-clear.
- Only when the state file has no pending entries, end with the explicit
  **"no further upgrades pending"** so the user does not ask what is next.

## Add a new MCP entry

Take command, package, pin, transport and tool count from vendor docs. Add the
entry with `enabled:false`; do not enable it until a task asks. Add a row to the
registry table above, then follow steps 1, 3, 4 and 5. Registries describe one
machine — refresh the baseline in the same change.

## Never

- bump a pin because a probe says newer, without reading the changelog
- ask which server to upgrade when the OpenCode config already answers it
- ask again after reporting "all current" — that is the terminal result
- ask the user to rank safety or supply impact data — it is computed in 1c
- exceed the question budget (1 for all, 2 only for selected)
- scan or propose skills/agents from VS Code, Copilot, Claude or any harness
- suggest installing a skill from another harness
- report an unrelated npm/uv tool as updatable unless it backs an OpenCode MCP entry
- enable every server "to be safe"
- call `--help` success a connection test
- put `security` or `breaking` updates into the routine batch silently
- apply a new upgrade while `RESTART_PENDING` is unresolved
- clear a pending-restart flag before verification actually passed
- leave a task-scoped server enabled after the task
