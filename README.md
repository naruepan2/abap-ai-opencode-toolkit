# ABAP AI OpenCode Toolkit

A portable AI teammate for ABAP work: memory that compounds, a contract per program,
and checks that keep OpenCode honest about which tools it can actually call.

**Two layers. Keep them apart:**

| Layer | What it is | Where |
|---|---|---|
| Toolkit | scripts, templates, docs, plugin, SAP launcher | this repo (git-tracked) |
| Instance | your cards, knowledge, specs mirror, reports | `workspace/` (never committed) |

Clone, run `install.ps1`, restart OpenCode. The instance is yours; a colleague gets
their own empty one.

## Why

- **Memory that compounds.** Incidents land in an inbox; at close-out each becomes one
  edited knowledge entry — or a check, if the rule repeats. No append-only log.
- **A contract per program.** `spec.md` holds requirements and acceptance criteria;
  `CHANGELOG.md` holds one row per deploy — the window SAP version management misses.
- **Cheap starts.** One command prints the resume card, health, inbox, and tool rules.
  Then read only what the task needs.

## Requirements

- Windows 10/11, PowerShell 5.1+
- Python 3.8+ (the scripts use only the standard library)
- [OpenCode](https://opencode.ai)
- Optional: an SAP ADT MCP server (`ai-dev`, `arc1`) and the SAP GUI for the launcher

## Install

```powershell
git clone https://github.com/naruepan2/abap-ai-opencode-toolkit.git
cd abap-ai-opencode-toolkit
.\install.ps1 -DryRun      # show every action
.\install.ps1 -Seed        # do it
```

Restart OpenCode once, then:

```powershell
python scripts\session_context.py
```

`install.ps1` is idempotent. It seeds `workspace\`, links
`~\.config\opencode\memory` to it, registers the tool-snapshot plugin, adds a marked
block to global `AGENTS.md`, copies new personal skills, and baselines the registries.
With `-WithSap` it also copies the launcher and an example profile — never a password.

It never touches SAP profiles, credentials, or MCP entries. Rewrites get a timestamped
`.bak`. Skip switches: `-SkipAgents`, `-SkipRegistry`.

## Layout

```
abap-ai-opencode-toolkit\          # this repository
├── install.ps1                    # one command: instance, junction, plugin, AGENTS
├── scripts\                       # digest, closeout, registry and memory checks
├── templates\                     # spec, changelog, plan, probes, instance seed
├── plugins\tool-snapshot\         # OpenCode plugin that captures the tool catalog
├── config\opencode-sap\           # SAP launcher + Windows keychain helper
├── config\opencode-skills\        # personal skills the installer copies in
├── registries\                    # machine snapshots, regenerated per machine
└── workspace\                     # YOUR instance - git-ignored
    ├── memory\                    #   cards, knowledge, inbox, tool map
    └── specs\                     #   mirror of Projects\**\spec.md
```

`workspace\` is what `~\.config\opencode\memory` points at. To keep the instance in
its own private repository, clone it elsewhere and set `ABAP_WORKSPACE` to that
path; the toolkit never needs to know.

The scripts assume a portfolio that keeps SAP work in `Projects\<PROJECT>\<PROGRAM>\`
with an `INDEX.md` above it. Neither is required: `ABAP_PROJECTS_ROOT` and
`ABAP_INDEX` point the checks at any tree.

For a map of every folder and which files are committed vs generated, see
`docs/catalog.md`.

## Daily use

```bash
python scripts\session_context.py      # start: card + health + inbox + tool rules
python scripts\closeout.py             # end: inbox + card + plan + knowledge dates
python scripts\registry_check.py --check --brief   # tool catalog + prompt cost
python scripts\memory_check.py         # memory integrity
```

Add `--tiny` to the digest for the light tier, `--project DEMO/ZDEMO01` to closeout
for one program. `--refresh` only after installing a skill, agent, or MCP server.
`specs_sync.py --write` mirrors program specs into the instance.

Exit `0` = nothing broken; `1` = an issue. Warnings (new asset, stale date, budget,
idle server) are human decisions, not fixes. Full report:
`workspace/memory/reports/registry-report.md`.

## Memory model

| Tier | When | Read |
|---|---|---|
| `light` | a question, an analysis, a review | the digest only |
| `task` | code, file, or SAP work | digest + the project card + its knowledge domains |
| `deep` | new project, incident, design | digest + every memory file |

An incident is captured in `workspace/memory/corrections.md` the moment it happens
(one row, ≤240 characters, status `open`). At close-out each row gets exactly one
outcome: merged into `workspace/memory/knowledge/<domain>.md` (Seen +1), added as a
new entry, promoted to `AGENTS.md` or a skill, or dropped as a one-off. The row is
then marked `drained`. The history is git, not a second log.

## The spec contract

Every program folder carries `spec.md` — requirements, acceptance criteria,
approved deviations, open questions — and `CHANGELOG.md`, one table row per deploy
(`Ver | Date | What changed | Verified`). The customer FS lives in `spec/source/`,
is immutable, and is never committed. The spec is written at the program level
because that is where a requirement is signed off.

`scripts/closeout.py` checks the front matter, the FS file and the REQ/AC tables, and
warns when the newest changelog row is behind `implemented_version`.

## SAP MCP (optional)

`config/opencode-sap/` holds a launcher that turns one profile into either engine:

| File | Purpose |
|---|---|
| `sap-mcp.ps1` | `-Profile <name> -Engine ai-dev\|arc1`, `-AllowWrites`, `-AllowDataPreview`, `-AllowFreeSql`, `-AllowTransportWrites -AllowedTransports <list>`, `-AllowGitWrites`, `-DryRun`, `-PromptTest` |
| `sap-cred.ps1` | Credential Manager (`CredRead`/`CredWrite`) plus the native sign-in dialog |
| `store-sap-secret.ps1` | store / list / remove a password for a profile |
| `profiles.example.json` | the shape of a profile: URL, client, user, system, CA, package allowlist |

Every `-Allow*` defaults to off, matching the engine's own "blocked by default" table.
Transport and Git writes are refused without `-AllowWrites`, and transport writes
without `-AllowedTransports` warn loudly: transport **release has no package check**, so
an empty list means every transport in the system.

Running more than one engine? `docs/mcp-capability-matrix.md` says which engine can do
which job; `docs/mcp-orchestration.md` says what is safe when two run at once, how
posture is armed, and why the rule is "one object, one writer".

The password is resolved in this order: `SAP_PASSWORD` in the process environment →
Windows Credential Manager (`sap-mcp:<profile>`) → the native Windows sign-in
dialog, which stores what you type so the next start is silent. Nothing is written
to a JSON file. A 401 means the password is wrong: re-store it, never retry it.

The launcher prints one line to stderr on every start naming the password source.
Trust that line before blaming SAP — a stale `SAP_PASSWORD` inherited by a running
app overrides the keychain.

Give the MCP startup time when a dialog can appear: `mcp.timeout.startup` in
`opencode.json` (180000 ms here; the default is 30 s).

## Team model

Main agent = lead. Specialists = subagents. Lead owns the answer and writes memory;
specialists return evidence, not conclusions.

- User gives goal + approval → lead makes plan + brief → specialist returns evidence.
- Specialists: `abap-developer`, `abap-runtime-debugger`, `sap-solution-architect`,
  `rap-service-developer`, `explore` / `general`.
- Lead reads and writes memory; registries are read-only checks; skills are playbooks.
- Tool map routes a specialist to an MCP engine. No specialist writes the same object
  as another — "one object, one writer, one session".

## Principles

| Action | Gate |
|---|---|
| Read-only inspection | proceed |
| SAP write, activate, or transport | explicit approval with target + transport |
| Edit a personal `*-by-pongg` file | propose, then wait for approval |
| Edit a vendor agent or skill | never; wrap or fork into a personal file |
| Enable or disable an MCP server | propose, then wait for approval |

1. **Evidence over guesses.** Unknown means "unknown" plus a read-only check.
2. **One owner per artifact.** Never parallel-write the same file or object.
3. **Read before write.** Re-read the live source; the local copy may be stale.
4. **Verify before claim.** Saved is not activated; activated is not tested.
5. **Ask before irreversible.** SAP writes, transports, and deletions.
6. **Vendor files are read-only.** Personal work lives in `*-by-pongg` files.

## Working with other people

- Each person runs `install.ps1` in their own clone and gets an empty instance.
- `workspace/` never leaves your machine through this repository. Keep it in its own
  private repository (and set `ABAP_WORKSPACE`) if you want it backed up.
- `registries/*.json` describe **one machine**. A colleague's `--refresh` will
  conflict with yours; take your side and refresh again.
- The toolkit is MIT. Your instance — memory, cards, mirrored specs — is yours, and
  may contain customer material: keep it private.

## Measured on the author's machine

Snapshot: 2026-11-18. Re-measure with `python scripts\registry_check.py --check --brief`;
these numbers move with every install. Current release: **v0.7.7** — see
[Releases](https://github.com/naruepan2/abap-ai-opencode-toolkit/releases).

| Area | Count | Notes |
|---|---|---|
| Skills | 122 | opencode 34, agents 40, claude 25, copilot 23 |
| Agents | 24 | 4 editable, 20 vendor |
| MCP servers | 18 | 14 enabled, 4 disabled/on-demand |
| Tools | 363 | 12 namespaces; ADT share: ai-dev ×3 (75 each), arc1 ×2 (8/9) |

Prompt cost: **73.1k chars per session** (skills 20.7k + tools 52.5k). Both catalogs
are over budget (skills 20k, tools 28k) — a human decision about which server or
skill to park, not a broken install. SAP servers stay on-demand. See
`docs/design.md` §"Prompt budget".

## Roadmap

- [x] Tiered context loading, memory and registry checks
- [x] Issue vs warning split so a healthy session exits 0
- [x] Tool snapshot automation (`plugins/tool-snapshot`)
- [x] Instance separated from the toolkit (`workspace/`, `ABAP_WORKSPACE`)
- [x] One-command install (`install.ps1`)
- [ ] `uninstall.ps1` and a non-Windows launcher
- [ ] Git history purged of customer data before the repository goes public
- [ ] Skill and MCP onboarding gates

## Privacy and license

Toolkit: MIT (see `LICENSE`). Instance: yours — `workspace/` is git-ignored, so
memory cards and mirrored specs never leave your machine through this repository. No
credentials, tokens, or customer data belong in the toolkit. See `SECURITY.md` and
`CHANGELOG.md`.
