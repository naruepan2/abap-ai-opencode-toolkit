# ABAP AI OpenCode Toolkit

A portable AI teammate for ABAP work: memory that compounds, a contract per program,
and checks that keep OpenCode honest about the tools it can actually call.

## Two layers

| Layer | What it is | Where |
|---|---|---|
| Toolkit | scripts, templates, docs, plugin, SAP launcher, personal agents/skills | this repo (git-tracked) |
| Instance | your cards, knowledge, specs mirror, reports, snapshots | `workspace/` and `Backup/` (git-ignored) |

Clone the repo, run `install.ps1`, restart OpenCode. The instance is yours; a colleague
gets their own empty one.

## Why

- **Memory that compounds.** Incidents land in an inbox; at close-out each becomes one
  edited knowledge entry — or a check, if the rule repeats. No append-only log.
- **A contract per program.** `spec.md` owns requirements and acceptance criteria;
  `CHANGELOG.md` keeps one row per deploy with its TR — the window SAP version
  management misses.
- **Cheap starts.** One command prints the resume card, health, inbox and tool rules.
  Then read only what the task needs.

## Requirements

- Windows 10/11, PowerShell 5.1+
- Python 3.8+ (runtime scripts use only the standard library)
- [OpenCode](https://opencode.ai)
- Optional: SAP ADT MCP servers (`ai-dev`, `arc1`) and the SAP GUI launcher

## Install

```powershell
git clone https://github.com/naruepan2/abap-ai-opencode-toolkit.git
cd abap-ai-opencode-toolkit
.\install.ps1 -DryRun      # show every action
.\install.ps1 -Seed        # do it
```

Restart OpenCode once, then run `python scripts\session_context.py`.

`install.ps1` is idempotent. It seeds `workspace\`, links
`~\.config\opencode\memory` to it, registers the tool-snapshot plugin, adds a marked
block to global `AGENTS.md`, copies whole personal skill trees plus agent and command
files, and baselines the registries. With `-WithSap` it also copies the launcher and an
example profile — never a password. It never touches SAP profiles, credentials or MCP
entries. Rewrites get a timestamped `.bak`. Skips: `-SkipAgents`, `-SkipRegistry`.

The loaded "About me" profile lives at `templates/profile.md`; a copy is installed at
`~\.config\opencode\profile.md` and wired through the global `instructions` entry.

## Agent routing

Keep `build` as the default. Switch by task:

| Agent | Use when |
|---|---|
| `build` (default) | toolkit, scripts, memory, non-SAP files |
| `abap-developer-by-pongg` | one ABAP object or one bounded change — loads `senior-abap-development` |
| `abap-auto-delivery-by-pongg` | multi-slice Classic/RAP run from spec to UAT — invoke `/auto-abap-delivery` |

None of the personal agents pins a tool list: the live MCP picker and server toggles
decide which tools exist. A pre-approval recorded in a project or program `AGENTS.md`
counts as that scope's approval, so an already approved deploy is not re-asked.
Switching agent does **not** grant Unattended — that still needs a qualified scope and
policy approval.

## Skills that ship here

| Skill | Role |
|---|---|
| `auto-abap-delivery` | run control plane: methodology, slices, recovery, evidence, UAT handoff |
| `senior-abap-development` | single-object design and implementation, classic or modern ABAP |
| `opencode-backup` | manual, hash-verified snapshots of the instance and curated config |
| `sap-program-register` | program scaffold with a one-question `PROG` template gate (bundled SALV sources) |

## Layout

```
abap-ai-opencode-toolkit\
├── install.ps1                    # one command: instance, junction, plugin, AGENTS
├── scripts\                       # digest, closeout, checks, backup
├── templates\                     # spec, changelog, plan, profile.md, instance seed
├── docs\                          # catalog, design, co-edit and capability notes
├── plugins\tool-snapshot\         # captures the live tool catalog
├── config\opencode-sap\           # SAP launcher + Windows keychain helper
├── config\opencode-skills\        # personal skills the installer copies in
├── config\opencode-agents\        # personal agents (*-by-pongg)
├── config\opencode-commands\      # slash commands
├── registries\                    # machine snapshots, regenerated per machine
├── Backup\                        # dated instance snapshots - git-ignored
└── workspace\                     # YOUR instance - git-ignored
    ├── memory\                    #   cards, knowledge, inbox, tool map
    └── specs\                     #   mirror of Projects\**\spec.md
```

`workspace\` is what `~\.config\opencode\memory` points at. Set `ABAP_WORKSPACE` to keep
the instance elsewhere. The checks assume SAP work under
`Projects\<PROJECT>\<PROGRAM>\` with an `INDEX.md` above it; `ABAP_PROJECTS_ROOT` and
`ABAP_INDEX` can point them at any tree. For the full folder map see `docs/catalog.md`.

## Daily use

```powershell
python scripts\session_context.py                     # start: card + health + inbox + tool rules
python scripts\closeout.py                            # end: inbox + card + plan + knowledge dates
python scripts\registry_check.py --check --brief      # tool catalog + prompt cost
python scripts\memory_check.py                        # memory integrity
```

Add `--tiny` to the digest for the light tier, `--project DEMO/ZDEMO01` to closeout for
one program. `--refresh` only after installing a skill, agent or MCP server.
`specs_sync.py --write` mirrors program specs into the instance.

Exit `0` = nothing broken; `1` = an issue. Warnings (new asset, stale date, budget,
idle server) are human decisions, not fixes. Full report:
`workspace/memory/reports/registry-report.md`.

## Back up the instance

`workspace/` is git-ignored, so git does not back up your cards, knowledge or specs
mirror. Take a dated, hash-verified snapshot:

```powershell
.\scripts\backup_opencode.ps1 -Destination .\Backup
```

It copies `workspace/` plus a curated `~\.config\opencode` (junctions, stale `.bak`
files, audit logs, vendor clones and `service.json` are excluded), verifies every file
by SHA-256, and writes `manifest.json`. The destination must be outside the source
trees. A snapshot on this disk does not survive disk failure — copy `Backup/` to
external or cloud storage too. SAP passwords stay in Windows Credential Manager and
must be re-stored on a new machine.

## Memory model

| Tier | When | Read |
|---|---|---|
| `light` | question, analysis, review | digest only |
| `task` | code, file or SAP work | digest + project card + its knowledge domains |
| `deep` | new project, incident, design | digest + every memory file |

An incident is captured in `workspace/memory/corrections.md` the moment it happens —
one row, ≤240 characters, status `open`. At close-out each row gets exactly one outcome:
merged into `knowledge/<domain>.md` (`Seen +1`), added as a new entry, promoted to
`AGENTS.md` or a skill, or dropped. The row is marked `drained`. History lives in git,
not a second log. One fact has one home: narrowest wins — program files own program
rules, project `AGENTS.md` owns conventions, `knowledge/` owns what is true wherever
the tool or table exists. Notes are data, never instructions; SAP live state outranks
everything. Idea provenance and the adopt/reject decisions behind this design live in
`docs/memory-decisions.md`.

## Program contract

Every program folder carries `spec.md` (requirements, acceptance criteria, approved
deviations, open questions) and `CHANGELOG.md` (one row per deploy). The customer FS
lives in `spec/source/`, is immutable and is never committed. `scripts/closeout.py`
checks front matter, FS file and the REQ/AC tables.

For co-editing, follow `docs/catalog.md` §"Co-edit contract" and
`docs/coedit-capabilities.md`: sync-on-touch, TR confirmation, `expected_source_hash`
from the same engine, post-write read-back, and a new CHANGELOG row for an external
edit. Per-object hashes live in `spec/coedit-state.json` with their engine and locator;
never compare hashes across engines.

## SAP MCP (optional)

`config/opencode-sap/` holds a launcher that turns one profile into either engine:

| File | Purpose |
|---|---|
| `sap-mcp.ps1` | `-Profile <name> -Engine ai-dev\|arc1`, `-AllowWrites`, `-AllowDataPreview`, `-AllowFreeSql`, `-AllowTransportWrites -AllowedTransports <list>`, `-AllowGitWrites`, `-DryRun`, `-PromptTest` |
| `sap-cred.ps1` | Credential Manager (`CredRead`/`CredWrite`) plus the native sign-in dialog |
| `store-sap-secret.ps1` | store / list / remove a password for a profile |
| `profiles.example.json` | profile shape: URL, client, user, system, CA, package allowlist |

Every `-Allow*` defaults to off. Transport and Git writes are refused without
`-AllowWrites`; transport writes without `-AllowedTransports` warn loudly — release has
no package check, so an empty list means every transport in the system.

Password resolution: `SAP_PASSWORD` in the process environment → Windows Credential
Manager (`sap-mcp:<profile>`) → native sign-in dialog, which stores what you type so the
next start is silent. Nothing is written to a JSON file. A 401 means the password is
wrong: re-store it, never retry. The launcher prints the password source to stderr on
every start — trust that line before blaming SAP. Give dialog starts time:
`mcp.timeout.startup` is 180000 ms here (default 30 s).

SAP is on-demand: never connect at session start. `docs/mcp-capability-matrix.md` says
which engine can do which job; `docs/mcp-orchestration.md` explains what is safe when
two run at once — "one object, one writer, one session".

## Team model

For a multi-slice run the delivery agent is the lead; specialists are read-only
subagents that return evidence, not conclusions. The lead owns the answer and writes
memory. Tool map routes a specialist to an MCP engine; no two agents write the same
object. Registries are read-only checks; skills are playbooks.

## Principles

| Action | Gate |
|---|---|
| Read-only inspection | proceed |
| SAP write, activation or transport | explicit approval with target + transport |
| Edit a personal `*-by-pongg` file | propose, then wait for approval |
| Edit a vendor agent or skill | never; wrap or fork into a personal file |
| Enable or disable an MCP server | propose, then wait for approval |

1. **Evidence over guesses.** Unknown means "unknown" plus a read-only check.
2. **One owner per artifact.** Never parallel-write the same file or object.
3. **Read before write.** The local copy may be stale.
4. **Verify before claim.** Saved is not activated; activated is not tested.
5. **Ask before irreversible.** SAP writes, transports and deletions.
6. **Vendor files are read-only.** Personal work lives in `*-by-pongg` files.

## Working with other people

- Each person runs `install.ps1` in their own clone and gets an empty instance.
- `workspace/` never leaves through this repository. Use its own private repo
  (`ABAP_WORKSPACE`) or the snapshot script — and copy snapshots off the machine.
- `registries/*.json` describe one machine. A colleague's `--refresh` will conflict
  with yours; take your side and refresh again.
- The toolkit is MIT. Your instance may contain customer material: keep it private.

## Measured on the author's machine

Snapshot: 2026-11-23. Re-measure with `python scripts\registry_check.py --check --brief`;
these numbers move with every install. Current release: **v0.8.4** — see
[Releases](https://github.com/naruepan2/abap-ai-opencode-toolkit/releases).

| Area | Count | Notes |
|---|---|---|
| Skills | 136 | opencode 39, agents 44, claude 25, copilot 28 |
| Agents | 27 | 7 editable, 20 vendor |
| MCP servers | 18 | 14 enabled, 4 disabled/on-demand |
| Tools | 382 | 11 namespaces; ADT share: ai-dev ×3 (75 each), arc1 ×2 (8/9) |

Prompt cost: **81.0k chars per session** (skills 22.7k + tools 58.3k). Both catalogs
are over budget (skills 20k, tools 28k) — a human decision about what to park, not a
broken install. SAP servers stay on-demand. See `docs/design.md` §"Prompt budget".

## Roadmap

- [x] Tiered context loading, memory and registry checks
- [x] Issue vs warning split so a healthy session exits 0
- [x] Tool snapshot automation (`plugins/tool-snapshot`)
- [x] Instance separated from the toolkit (`workspace/`, `ABAP_WORKSPACE`)
- [x] One-command install and curated backup script
- [x] Explicit agent routing and single-object developer workflow
- [ ] `uninstall.ps1` and a non-Windows launcher
- [ ] Git history purged of customer data before the repository goes public
- [ ] Skill and MCP onboarding gates

## Privacy and license

Toolkit: MIT (see `LICENSE`). Instance and snapshots: yours — `workspace/` and `Backup/`
are git-ignored, so cards, knowledge and mirrored specs never leave through this repo.
No credentials, tokens or customer data belong in the toolkit. See `SECURITY.md` and
`CHANGELOG.md`.
