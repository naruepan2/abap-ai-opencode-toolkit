# Changelog

## v0.6.0 — 2026-11-15

**The toolkit is installable: the instance moved out of git.**

- Layout: `workspace/` is the instance (memory, specs mirror, reports) and is
  git-ignored. `scripts/_paths.py` resolves it, with `ABAP_WORKSPACE`,
  `ABAP_PROJECTS_ROOT`, and `ABAP_INDEX` for an install outside the original
  portfolio. The scripts no longer assume `REPO.parent/Projects`.
- `install.ps1` — idempotent, `-DryRun`, `-Seed`, `-SkipAgents`, `-WithSap`: creates
  the instance, the memory junction, the tool-snapshot plugin entry, the AGENTS
  pointer block, and the registry baseline. It never touches SAP profiles, credentials,
  or MCP entries, and backs up every file it rewrites.
- `templates/instance/` seeds a fresh instance; the three schema READMEs are the
  canonical copies (they ship, `workspace/` does not).
- MIT licence. `SECURITY.md` splits what belongs to the toolkit from what may only
  live in the instance.
- Repository renamed `abap-agent-workspace-opencode` → `abap-ai-opencode-toolkit`;
  GitHub redirects the old URL, and `rename-workspace.ps1` moved the local folder,
  the junction, and every absolute path outside the repository.
- Known debt: the old `memory/` and `specs/` paths remain in git history. Purge them
  before the repository goes public.

## v0.5.20 — 2026-11-15

**SAP passwords can live in the OS keychain; plaintext stays forbidden.**

- `sap-cred.ps1` (CredRead/CredWrite/CredDelete) and `store-sap-secret.ps1`
  (store / list / remove, named `sap-mcp:<profile>`).
- `sap-mcp.ps1` resolves the password in order: `SAP_PASSWORD` environment ->
  Windows Credential Manager -> credential dialog. It verifies the stored username
  against the profile and refuses a mismatch; `-DryRun` prints only the source.
- `config/opencode-sap/` is the versioned backup of the scripts plus
  `profiles.example.json`; real profiles stay local (no customer data in git).
- AGENTS + tool-map: the OS keychain is allowed for MCP startup, plaintext is not;
  after a password change re-store and restart; a 401 means re-store, never retry.
- VS Code `mcp.json` is deliberately untouched.

## v0.5.19 — 2026-11-15

**ADT routing is written down.**

- `memory/tool-map.md`: task→path table (ai-dev = writer, arc1 = specialist) plus
  the one-writer and one-fact-one-source rules.
- Repo and workspace `AGENTS.md`: run `tools_now.py` before the first ADT call;
  when both engines are live and the task writes, ask which one to keep.
- `templates/plan.md`: a plan now records the `ADT path` (writer / verify /
  analyse) next to the contract.

## v0.5.18 — 2026-11-15

**MCP names now carry their engine.**

- `opencode.json`: `ds4-100` / `ds4-900` / `gsd-120` become `ai-dev-ds4-100` /
  `ai-dev-ds4-900` / `ai-dev-gsd-120`. `arc1-ds4-100` and `arc1-gsd-110` keep
  their names; every entry stays disabled.
- Updated every current reference: tool-map, tooling knowledge, the two DEMO cards,
  README, registry defaults, HCL program AGENTS. Historical CHANGELOG lines are
  left as written.
- `optional_namespaces` follows the new names, so toggling an ADT server is still
  not reported as registry drift.
- No tool change: the rename only affects the namespace prefix the model sees the
  next time an entry is enabled.

## v0.5.17 — 2026-11-15

**One ADT launcher and shared profiles; digest shows what is live.**

- `~/.config/opencode/sap/profiles.json` holds URL, client, user, CA and SAP Logon
  destination per system/client. `sap-mcp.ps1 -Profile ... -Engine ai-dev|arc1`
  prompts for the password at start (never on disk) and sets the engine-specific
  flags; `-DryRun` prints the resolved settings to stderr.
- `opencode.json`: `ds4-100` / `ds4-900` / `gsd-120` now call the launcher; added
  `arc1-ds4-100` and `arc1-gsd-110` disabled (16 MCP entries, 8 enabled).
- ARC-1 stays read-only unless `-AllowWrites` is passed; write session must close
  the ai-dev writer first.
- Digest prints `TOOLS 111 - ADT none` or the live servers with their role
  (`write` / `verify` / `read`), from `scripts/tools_now.py --json`.
- `optional_namespaces` now includes `gsd-120`, `arc1-ds4-100`, `arc1-gsd-110`, so
  toggling them on/off is not reported as registry drift.
- `arc-1@1.10.1` installed globally so the launcher can call `arc1.cmd` without
  npx stdout noise in the MCP channel.

## v0.5.16 — 2026-11-15

**Live toolset check: know which ADT server is actually connected.**

- `scripts/tools_now.py` reads the snapshot plugin's `registries/tools-full.json`
  and prints the live ADT namespaces, client role, available capabilities and the
  recommended path (`write=` / `verify=` / `analyse=`). It works before and after
  a toggle because the plugin refreshes on `mcp.*` / `tool.*` / `session.*` events
  (2 s, throttled to 60 s).
- `--check --expect <namespace>` fails when a namespace did not connect, when no
  ADT server is live, or when two code writers are enabled; `--json` is available
  for scripts.
- Roles are explicit: `arc1-*` is read-only, `ai-dev-*` / `ds4-*` / `gsd-*` is a
  writer on clients 100/110/120, and client 900 is the verify client.
- The snapshot timestamp is "last change", not a heartbeat: a quiet system keeps
  an old timestamp without being stale.
- `memory/tool-map.md` records the pre-call check.

## v0.5.15 — 2026-11-14

**One ADT path: the MCP; the old CLI is parked.**

- `skills/sap-engineering/sap-adt-cli` → `skills-parked/` (48 parked now). Catalog
  31 → 30 skills, prompt 36.0k → 35.9k.
- Removed the orphaned `~/.sap-adt-cli` profile (`luf-ds4-dev`, `allow_write: true`)
  and the Windows credential target `sap-adt-cli`; the binary was already gone, so
  the profile was a pre-authorized write path with no owner.
- Added a `tooling` knowledge entry: ADT via MCP `ds4-100` / `ds4-900`; the CLI is a
  fallback only, and reinstating it needs the overlap removed and the probes re-run.
- `RESTORE.md` records why it is parked and how to bring it back.

## v0.5.14 — 2026-11-14

**The program-file rules now live in the repository itself.**

- `AGENTS.md` gains "Program files (spec + changelog)": the spec/FS/changelog rules,
  the read-once policy and the mirror command. The change contract now starts by
  reading `spec.md` instead of asking whether one exists.
- Why: `SAP Projects\AGENTS.md` and the global OpenCode `AGENTS.md` are outside this
  repository, so a clone did not carry the rule; the design was documented but the
  operating instruction was not versioned.
- README layout now mentions `CHANGELOG.md` and the "FS is never committed" rule.

## v0.5.13 — 2026-11-14

**Changelog slimmed to the gap SAP actually leaves.**

- Four columns: `Ver | Date | What changed | Verified`. Dropped the artifact,
  md5 and rollback recipe - SAP version management snapshots a TR only when it is
  **released**, so this file covers the unreleased window; the bytes stay in
  `DECISIONS.md` and the build files.
- At release the block collapses to one line (`TR ... released ... - v1-vN`), so
  the file never grows past one transport.
- `closeout.py` now only checks the newest row against the spec
  `implemented_version` (the v12-vs-v20 drift); the artifact check is gone.

## v0.5.12 — 2026-11-14

**A deploy changelog per program, and the FS stays out of git.**

- `templates/CHANGELOG.md`: one table row per deploy (version, change, files,
  artifact + md5, active md5, verification) plus the rollback recipe. The why stays
  in `reports/DECISIONS.md`; this file is not a prose log.
- ZDEMO01 `CHANGELOG.md` backfills v12-v20. It records the real gap: the v12/v13
  artifacts were overwritten and their builders are gone, so the oldest
  artifact-backed version is v14 (the newest runtime-verified is v13).
- `closeout.py`: parses the changelog, warns when a named artifact no longer
  exists (rollback broken) or when `implemented_version` differs from the newest
  row (the v12-vs-v20 rot).
- `specs_sync.py` now mirrors `CHANGELOG.md` too - and **stops mirroring
  `spec/source/`**. The customer FS is the customer's document; the workspace rule
  is "never commit customer data". Spec and changelog are our own text.
- `spec.md` §7 renamed "Spec change log" so it cannot be confused with the deploy
  changelog; the program `AGENTS.md` deploy step now requires one row.

## v0.5.11 — 2026-11-14

**Specs and FS mirrored into the repository, with a drift check.**

- `scripts/specs_sync.py`: copies every `Projects/*/*/spec.md` and its
  `spec/source/*` into `specs/<PROJECT>/<PROGRAM>/`, writes a deterministic
  `specs/manifest.json` (version, status, sha256, bytes), supports `--list`,
  `--check` (default, exit 1 on drift) and `--write`.
- `closeout.py` imports the check and warns when the mirror is stale, so a spec
  edit that is not mirrored is caught before the session ends.
- `specs/README.md` states the rules: read the program copy, never edit the
  mirror, keep the repository private (the FS contains customer data).
- Why a mirror rather than `git init` on `Projects/`: the program folder is
  16 MB / 354 files of source dumps; the specs are 141 KB.
- `Projects/DEMO/ZDEMO01/reports/FS_QUESTIONS.md`: **optional** Thai copy of the 13
  open questions for the FS owner, with a blank answer table. Not part of the
  contract; safe to delete. `spec.md` links it as optional.

## v0.5.10 — 2026-11-14

**One `spec.md` per program: the contract the FS never was.**

- Added `templates/spec.md`: front matter (`program`, `spec_version`, `status`,
  `fs_version`, `fs_file`, `implemented_version`, `updated`) plus REQ / AC / DEV / Q
  tables, with the rule that the FS under `spec/source/` is immutable.
- ZDEMO01 migrated: the FS markdown moved from the Desktop to
  `Projects/DEMO/ZDEMO01/spec/source/FS_ZDEMO01_V4.0_20261018.md` (135,251 bytes,
  md5 unchanged), and `spec.md` now distils 12 requirements, 10 acceptance
  criteria, 4 approved deviations and 12 open questions from FS V4.0 + v1-v20.
- `closeout.py`: new spec check - front matter, `fs_file` exists, REQ/AC tables
  parse, unique IDs, allowed statuses, FS reference per requirement, stale spec
  warning. Output line: `spec v1.0: 12 req (5 pending-test), 10 ac, 12 open q`.
- `session_context.py`: one digest line (`SPEC ...`) so the contract is visible at
  session start without loading it (~90 chars).
- Rules updated in the global `AGENTS.md`, the SAP workspace `AGENTS.md`, and both
  project/program `AGENTS.md`: read the spec before the first edit; no spec on an
  older program → write one at the next change; never invent a requirement.
- Why program-level, not project-level, and why not the Kiro three-file layout:
  `docs/design.md` § "Program spec".
- The ZDEMO01 `program.yaml` / `README.md` pointers were stale (v11/v12); they now
  point at v20 and at the spec. The historical status list is left for the owning
  session to close out.

Follow-ups the same day (user approved all three options):

- **A - card closed out:** `memory/projects/DEMO/zmme011.md` now says v20, points at
  `spec.md` and the FS, and stays inside the 9,000-char budget (8,993).
- **B - HCL draft spec:** `HCL_INTERFACE_QA32/spec.md` (4 REQ, 4 AC, 5 Q, status
  `draft`, `fs_file: none`) built only from verified facts; the Q table is the
  scope. `closeout.py` treats `none`/`na`/`tbd` as "no FS" instead of a broken path.
- **C - FS revision guard:** the digest line now shows the FS version
  (`SPEC v1.0 · FS V4.0 · 12 req ...`), and `closeout.py` warns when the FS file is
  newer than `spec.md`, or when `fs_version` does not match the version in the
  file name.
- **Read policy** (the question behind it: do not pay for the spec every turn):
  once per session per program, then only the REQ/AC/Q row in play; skip it for
  navigation, status questions and formatting-only changes. Table in
  `docs/design.md` § "When the spec is read", one line in both `AGENTS.md`, and a
  `working-method` knowledge entry. No new skill or subagent - a guardrail that
  must always fire belongs in `AGENTS.md`, not in an opt-in skill.

## v0.5.9 — 2026-11-14

**`sap-ai-dev-toolkit` 0.9.9924 → 0.9.9926.**

- `npm install -g sap-ai-dev-toolkit@0.9.9926`; the pinned runtime binary was
  reinstalled by its postinstall. Node 26 trips the package's `EBADENGINE` warning
  (it declares `^20 … ^24`) but the install and the launcher work — recorded here so
  the warning is not re-investigated.
- npm skipped the postinstall on the first pass (`allow-scripts` policy). Re-ran
  `node scripts/postinstall.mjs` explicitly; it reported "MCP config was not changed"
  and only touched the Copilot side, so `opencode.json` stayed byte-identical
  (verified against a backup).
- The toolkit materialised 12 Copilot skills and 1 Copilot agent that had gone stale
  (`btp-platform-administration`, `datasphere-*`, `cloud-alm-operations`,
  `process-automation-development`, `bw-datasphere-migration`, and the integration and
  HANA-cloud set). Copilot registry 14 → 26 skills, 16 → 17 agents.
- **No OpenCode prompt cost**: the OpenCode catalog is unchanged at 31 skills / 19.8k
  chars, tools 111 / 16.1k, prompt 36.0k. Registry 0 issues / 4 warnings after
  `--refresh`.
- Parked skills were not re-created (10 folders still in the loaded catalog, 47 in
  `skills-parked`), which is the failure mode to check after every toolkit update.

## v0.5.8 — 2026-11-14

**Second wave: 18 duplicates and unused families parked. Fixed prompt 41.9k → 36.0k.**

- Parked: `rap-development`, `rap-service-delivery`, `cds-development`,
  `abap-development`, `abap-debugging`, `abap-testing-quality`, `sap-transport-release`,
  `sap-health-triage`, `sap-sdlc-orchestration`, `sap-standard-api-analysis`,
  `clean-core-extensibility`, `memory-management`, `open-computer-use`,
  `aicore-sdk-java`, `aicore-sdk-js`, `sap-fiori-ios`, `sap-integration-architect`,
  `integration-suite-delivery`. Each one is either a thinner duplicate of a skill that
  stays, or a family with no path in this workspace.
- Skills 49 → 31 entries / 25.8k → **19.8k chars**, now **inside the 20k budget**; the
  catalog warning is gone. Warnings 5 → 4 (only the unfixable vendor descriptions).
- Two waves total 47 skills / 21,909 chars out of every session. `RESTORE.md` covers
  both, with the reason per skill and restore-by-family commands.
- `design.md` records the three measured steps (73.3k → 57.9k → 41.9k → 36.0k).

## v0.5.7 — 2026-11-14

**29 Basis/DB skills parked: fixed prompt 57.9k → 41.9k chars (−27.6%).**

- Moved out of the loaded catalog: kernel patch, OS executables, SSCR keys,
  housekeeping, SAProuter, Web Dispatcher, Cloud Connector, system lifecycle, GUI
  landscape, HANA SR/XSA/lifecycle, Oracle DG, Db2/ASE/MaxDB/SQL Server HADR, DB
  commands, backup/recovery, space reclaim, crypto PSE, transport at OS level, client
  copy, dormant clients, software download, security patch, compliance docs, BTP CLI,
  NW Java/PI. 15,950 chars of description measured out of the prompt.
- Skills 78 → 49 entries / 41.7k → **25.8k chars**; tools unchanged at 111 / 16.1k.
- Restore in seconds, per skill or per family:
  `~\.config\opencode\skills-parked\RESTORE.md` (also pointed at from `tool-map.md`).
- `--refresh` also dropped 11 Copilot entries whose folders no longer exist under
  `~\.copilot\skills` — stale, not caused by the move (verified: paths absent before).
- Still 5.8k over the 20k skill budget. Next candidates are named in
  `docs/design.md` §Prompt budget: the duplicate RAP/CDS/troubleshooting pairs and the
  unused AI Core / Fiori iOS / Integration Suite family.

## v0.5.6 — 2026-11-14

**A config change that is not in effect is now visible.**

- `registry_check.py` warns when a server is disabled in the config but still present
  in the running catalog — the exact symptom of a daemon that was not restarted. The
  note names the server and says to restart the service, not the window.
- `knowledge/tooling.md`: the rule is generalised from "`policy.json` is read once" to
  "the service daemon holds the MCP servers, not the window", `Seen` 1 → 2, with the
  2026-11-14 evidence (daemon PID 33916 started 20:59, app 21:13, catalog still 170).
- `templates/probes.md`: the nine probes as paste-ready prompts for cold sessions,
  with the first-action pass condition and the scorecard update.
- Correction: `mcp.servers` in `opencode.json` is **not** a phantom entry — the
  scanner already flattens it and lists `browse` correctly. My earlier claim came from
  reading the raw config, not the registry.

## v0.5.5 — 2026-11-14

**The close-out is verified, and a task loads only its own domains.**

- `scripts/closeout.py`: the last call of a task. Read-only checks of the four things
  that rot — the inbox (open rows, age >7d, cap 40), the project card (the four
  contract answers, last update >14d), a referenced plan file (exists; open/blocked
  todos) and knowledge entries (unconfirmed >180d). Exit 1 only when something is
  broken (a plan is missing, a table does not parse).
- `session_context.py` reads `domains: [a, b]` from the card and prints only those
  knowledge files (`11 of 26 entries — this project's domains`); `--full` marks the
  rest as `not loaded`. A digest that fell back to the newest card says so and
  suggests `--project`.
- Cards declare `domains:` (ZDEMO01: `sap-abap, sap-data`; HCL: `sap-gui, tooling`);
  the card template carries the line.
- `AGENTS.md`, `memory/README.md`, `scripts/README.md` and the layout now name
  `closeout.py` as the close-out step.

## v0.5.4 — 2026-11-14

**Delegation is a decision, not a habit.** The lead is a team lead, not a dispatcher.

- `memory/team-roster.md`: default is now **do it yourself**. States the arithmetic —
  wall-clock = longest parallel branch + spawn + verify only when the lead has
  independent work; sequential work gains nothing and pays the overhead.
- Criterion changed from "how much work" to **parallelisable vs sequential**; added
  "do it inline" cases (continuous chains, tacit conversation context, memory writes,
  decisions already made) and the rule that a step depending on a child's result is
  done inline.
- Two named costs a small task pays when delegated: the child re-reads files the lead
  already has, and the lead must verify the evidence anyway.

## v0.5.3 — 2026-11-14

**Plan + todo became the checkpoint of a long run.**

- `templates/plan.md`: goal, acceptance test (= stop condition), the four contract
  answers, the approved scope, ≤12 verifiable todos, and a one-line-per-tick log.
  Four rules: one todo = one verifiable unit; approve once; the plan is a hypothesis;
  ≤12 items.
- `AGENTS.md` §Long runs: plan first and approve once, checkpoint every todo with
  evidence, a blocked step is a stop not a retry, and three explicit stop conditions.
- `memory/team-roster.md` §"A subagent has no channel to the user": the brief carries
  the contract and scope, and a child returns `BLOCKED: <question>` instead of asking,
  retrying or guessing.
- Project card template gains `Approved scope`, `Stop condition` and `Plan:` (the two
  live cards are untouched — another session is editing them).

## v0.5.2 — 2026-11-14

**The change contract: four answers before the first edit.**

- New reflex gate (workspace `AGENTS.md` + global `AGENTS.md` + digest `STYLE`):
  before creating or changing a program, ask for the **FS** (and where it is), the
  **change type** (bug fix / feature extension / change request), **production**
  status (+ dev sync), and the **target** (system, client, transport). Wait for the
  answers; if one is unknown, resolving it is the first task.
- Direction table added: bug fix = reproduce + smallest patch; extension = designed
  delta, backward compatible; CR = impact analysis + transport order; live on
  production = compare the dev source with production first, plan regression.
- No FS is a finding, not a licence: propose a one-page FS for approval.
- Project cards gain `FS`, `Change type`, `Production`, `Target`; both existing cards
  filled in, with `unknown — ask` wherever the evidence does not exist.
- Knowledge entry `working-method` §"Establish the change contract"; `docs/memory-model.md`
  §"Task kickoff"; probe 9 added to `memory/expertise.md` (9 probes total).

## v0.5.1 — 2026-11-14

**Expertise is the goal; notes are not.**

- `memory/expertise.md`: defines the end state (a rule is expertise when it is
  unprompted, not looked up, and testable), tracks three levels — **reflex** (printed
  into every session: 6), **enforced** (a check fails when it breaks: 3),
  **handbook** (correct only if read: 15 of 24) — and lists **8 cold probes** with
  pass conditions, plus the monthly loop and a scorecard.
- The first probe is the meta-probe: recognise the symptom and go to the evidence.
  Added as knowledge entry `working-method` §"Diagnose from the symptom".
- `memory_check.py` requires `expertise.md`; the digest lists it as an on-demand file.
- Honest status recorded: no probe has been run yet, so the 8/8 target is not claimed.

## v0.5 — 2026-11-14

**Memory became a knowledge base instead of a work log.** Design: `docs/memory-model.md`.

- `memory/knowledge/` — 24 entries across 5 domains (`working-method`, `tooling`,
  `sap-gui`, `sap-abap`, `sap-data`). One entry per rule with Rule / Why / Break it /
  Seen / Confidence / Evidence, edited in place. Growth is a merge, not an append.
- `corrections.md` is now the **inbox**: ≤240 chars per incident, status
  `open` → `drained`, archived monthly. It is a buffer, not a ledger.
- `lessons.md` is retired; a knowledge entry *is* the lesson. Both old tables are
  kept at `memory/_archive/v0-ledger/` (the 4 rows still marked `open` were
  implemented in ZDEMO01 v11/v12 and are recorded in the card).
- The close-out is a **consolidation gate** with four outcomes (merge / add /
  promote / drop), written into `AGENTS.md`, `config/opencode-AGENTS.md`,
  `memory/README.md` and `templates/AGENTS.md`.
- `memory_check.py` validates the entry schema (fields, confidence values), the
  per-domain cap (12), the entry size (1.2k), the inbox cap (40) and the row/scheme
  budgets. The knowledge check is negative-tested: a missing field fails with exit 1.
- `session_context.py` prints the inbox count and the knowledge inventory per domain
  instead of the corrections list (~2.4k chars brief, 0.8k `--tiny`).
- Project cards and `tool-map.md` now point at knowledge entries instead of
  `lessons.md`.

## v0.4.2 — 2026-11-14

**Tool diet: 211 → 111 tools, 73.3k → 57.9k chars per session.**

- `sap-gui` (59 tools), `playwright` (25) and `sap-docs` (9) moved to on-demand
  (`enabled: false`). `sap-gui` costs nothing extra in workflow: SAP work already
  needs one enable + restart for `ds4-100`.
- `rosa` removed from `opencode.json`. It is the SAP Cloudification Repository MCP
  (`npx @rosa-mcp/server`: Clean Core level, successor lookup, compliance check);
  never used here and the `atc-cloudification` skill covers the job. The exact
  restore snippet is in `memory/tool-map.md` §"Disabled or removed servers".
- `ds4-100` was left enabled in the steady state; both SAP clients are now off, as
  the on-demand rule requires.
- `optional_namespaces` now lists `sap-gui`, `sap-docs`, `playwright` so toggling
  them is not reported as drift.
- Measured after the change: tools 16.1k chars / 111 tools, under the 28k budget.
  The skill catalog (41.7k / 78) is now the only block over budget.

## v0.4.1 — 2026-11-14

**Measure the prompt, not just the memory.**

- `registry_check.py` now reports a **prompt budget**: the injected skill catalog
  (41.7k chars / 78 entries) and tool descriptions (31.5k / 211 tools) against
  budgets of 20k and 28k, with the top namespaces named. Measured on 2026-11-13,
  the two catalogs cost ~73k chars per session — 7x the memory files they replaced.
- `session_context.py --tiny`: light tier in 0.8k chars (project, status, next step,
  one style rule, open-correction count, health only when broken).
- `memory_check.py` also guards the project-card size (budget 9k chars).
- The global `AGENTS.md` SAP section is now rules + a pointer: the 13-line
  enable/disable procedure moved to `memory/tool-map.md` §"SAP on-demand", where it
  is read exactly when SAP work starts (4.99k → 4.42k chars, every session).
- `docs/design.md` records the measured prompt budget per block; `memory/README.md`
  points at it.
- Fixed a variable shadowing bug (`ns`) that broke the full report in v0.4.

## v0.4 — 2026-11-13

**Tiered context loading, and a gate that stops crying wolf.**

- Added `scripts/session_context.py`: one call replaces eight file reads plus two
  scanner runs. It prints the active project's resume card, memory and registry
  health, the open corrections, the curated tool rules from the `digest` block in
  `memory/tool-map.md`, and the size of every file that can be opened on demand.
  Measured **1.8k chars (~450 tokens)** against **26.6k chars** for the previous
  read-everything rule.
- Session start is now tiered (`light` / `task` / `deep`) in the global `AGENTS.md`,
  the workspace `AGENTS.md`, `memory/README.md`, `templates/AGENTS.md`, and
  `docs/design.md`. Nothing was removed from the `deep` tier.
- `registry_check.py` no longer reports designed states as failures:
  - an `optional_namespaces` server (on-demand SAP) with zero tools is a warning,
    not an issue, and is listed as "on-demand, idle (expected)";
  - the tool total is compared with the optional namespaces removed on both sides,
    so connecting/disconnecting SAP is not drift;
  - new assets and stale validations are warnings; only broken things (missing
    path, duplicate name, missing skill reference, missing server/tool, zero tools
    on a non-optional server) fail the gate.
  Result: a healthy idle session now exits `0` instead of `1` with three
  false positives.
- Added `promoted` to the allowed correction statuses in `memory_check.py`.
- Memory lifecycle: a correction keeps `status: open` and is **promoted** (status
  change + pointer), not copied into `lessons.md`; close-out is one batched edit
  per file; closed/promoted rows older than 30 days move to `memory/_archive/`.
- `team-roster.md`: added a delegation cost model — delegate only for read-only
  work of ≥15 tool calls or >5k tokens of output, one SAP GUI actor, at most 2-3
  children, and a brief of five lines plus a pointer.

## v0.3.2 — 2026-11-13

- ZDEMO01 `_save_history` now reads `MATDOC` instead of `MKPF` + `MSEG`.
  Header fields (`BUDAT`, `CPUDT`, `CPUTM`, `USNAM`, `BKTXT`) and item fields
  (`VBELN_IM`, `VBELP_IM`, `BWART`, material, plant, sloc, batch, quantity) come
  from one table.
- Deployment: `ZDEMO01_MODL` v10 (transport `DS4K904935`); syntax 0 findings,
  active, no inactive objects.

## v0.3.1 — 2026-11-13

- Scanner: flatten the V2 `mcp.servers` shape (the `browse` server is now in the
  MCP registry) and support `optional_namespaces` in the tool baseline.
- Marked `ds4-100` / `ds4-900` optional so enabling an on-demand SAP server does
  not produce false tool drift.
- Captured the ZDEMO01 v7–v9 debugging lessons: preload key mismatch (DO vs SO),
  `BAPI_OUTB_DELIVERY_CREATE_SLS` `NUM_DELIVERIES`, batch-split main-item
  control, `ZMMT014-UECHA`, and the SAP GUI custom-button focus caveat.
- Deployment: `ZDEMO01_MODL` v9 (transport `DS4K904935`); messages 033/041 now
  use “Post Goods Issue”, messages 044/045 added.

## v0.3 — 2026-11-13

- Added `plugins/tool-snapshot`: an OpenCode server plugin that writes
  `registries/tools-snapshot.json` and `registries/tools-full.json` from
  `ctx.tool.list()`. It refreshes on load and on MCP/tool/session events, and only
  rewrites when the tool set changes.
- The scanner now records tool IDs in `registries/tools.json` and reports new or
  missing tools.
- `--refresh` adds newly discovered assets with `status: new`; stale checks skip
  `new` rows.
- Updated `sap-ai-dev-toolkit` from 0.9.9922 to 0.9.9924. The npm install emitted
  a postinstall warning for `@sap/hana-client` (`checkbuild.js` missing); the core
  launcher and VSP binary still respond.
- The toolkit update added 6 Copilot skills and 5 Copilot agents (BTP,
  BW/DataSphere, Cloud ALM, DataSphere, process automation, DevOps observability).
  They are vendor assets and are recorded in the Copilot registry only.

## v0.2 — 2026-11-13

- Added the read-only registry scanner (`scripts/registry_check.py`).
- Added machine-readable registries for skills, agents, MCP servers, and tools.
- Added the session-start registry brief to the global `AGENTS.md`.
- Disabled the drifted `ds4-100` MCP server (SAP is on-demand).
- Split actionable issues from informational warnings.
- Added the team model, task lifecycle diagrams, and the comparison template.

## v0.1 — 2026-11-13

- Bootstrapped the workspace: user profile, lessons, corrections, skill
  candidates, agent registry, tool map, team roster, and the ZDEMO01 project card.
- Added `README.md`, `AGENTS.md`, `SECURITY.md`, and the design/lifecycle docs.
