# Changelog

## v0.8.6 — 2026-11-23

- Resolved F-12: parked all five SAP MCP servers (`ai-dev-ds4-100/900`, `ai-dev-sus-100`,
  `arc1-ds4-100/sus-100`) to `enabled:false`, restarted once, and verified `opencode mcp list`
  shows all five disabled. `sap-abap-docs` remains on (no credential prompt). Registry is
  0 issues at **126 tools / 7 namespaces**, MCP 18 (8 on / 10 off), prompt **42.7k**.
  The tool catalog is now inside its 28k budget; the skill catalog is still over 20k.
  `README.md`, `docs/design.md` and `tool-map.md` updated to match.

## v0.8.5 — 2026-11-23

- Full audit (5 read-only checker agents, report in `workspace/memory/reports/audit-20261123-report.md`):
  corrected stale snapshot numbers in `README.md`/`docs/design.md`/`tool-map.md`, fixed
  `scripts/README.md` status values and read-only/stdlib claims, removed a false exit-code
  claim in `tools_now.py`, made the closeout audit regex case-insensitive, removed an L0
  term leak, narrowed three decision homes, deduplicated the D-28 rule, fixed the spec
  "one run" wording, and reworded two CHANGELOG overclaims. Parked count is now 50 in
  `RESTORE.md`/`tool-map.md`, and the `opencode mcp list` cwd caveat is documented.
- ZMME011 (local audit only, no SAP connection): marked `patched_MODL_v22.abap` /
  `patched_VIEW.abap` as stale v22/v23 navigation copies in `program.yaml`, `README.md`
  and `AGENTS.md`, and added a mandatory active-version read-back gate to the pre-approved
  deploy procedure. F-12 (on-demand docs vs 5 enabled SAP servers) is deferred to a user decision.


- Closed the five remaining consistency findings: full cross-skill reference path, a
  definition of `run`, a fast path that distinguishes SAP-object specs from toolkit files,
  an enforced memory-audit line in `closeout.py`, and a corrected docstring. `.mcp.json` is
  now git-ignored.
- Disabled `windows-mcp` (19 tools): OpenCode self-upgraded 2.3.2 → 2.4.0 and rejects its
  MCP initialize handshake. Both suggested `protocol` values were tried without success;
  the binary has no protocol flag and 0.9.0 is the latest release. `open-computer-use` and
  `browse` remain available. Registry is back to 0 issues at 369 tools.

- Bounded `sap-abap-docs` as a SAP knowledge channel for both `*-by-pongg` agents and the
  senior/auto delivery skills: `DOC_EVIDENCE` vs `SYS_EVIDENCE`, docs MCP before general web
  for release/API facts, re-verify on the target, public-cloud metadata is not on-prem proof.
  Recorded as D-28. The rule was removed from both AGENTS on-demand lists and recorded in
  `templates/profile.md`, both agents, `senior-abap-development/SKILL.md`,
  `released-alternatives.md`, `capability-and-intake.md` and `engineering-judgment.md`;
  no hard gate was added.

- Replaced the docs MCP `sap-docs`/`sap-ui5-docs` with `sap-abap-docs`
  (`https://mcp-abap.marianzeis.de/mcp`, marianfoo/abap-mcp-server, 9 tools incl. `abap_lint`);
  `ui5_version_diff` was dropped. Remote HTTP MCP entries require `"type": "remote"` —
  `"type": "http"` is silently ignored by OpenCode. Removed `sap-docs` from both AGENTS
  on-demand lists, updated `tool-map.md`, the `sap-mcp-upgrade` registry table,
  `registry_check.py` optional namespaces and the registry snapshots. No daemon restart was
  needed: changes were picked up live.

## v0.8.4 — 2026-11-23

- Rule diet and parking policy: `auto-abap-delivery/SKILL.md` now keeps six hard gates
  and points to `references/non-negotiable-rules.md` for the full list; `docs/design.md`
  documents an explicit, human-approved parking order for skills and task-scoped MCP
  servers. Recorded as D-27 in `docs/memory-decisions.md`.
- Resolved eight consistency findings: the scope-order gate is limited to one run;
  memory close-out is named apart from run completion; decision homes and lesson
  capture paths are stated explicitly; freshness authority is live SAP hash > content
  fingerprint > TTL; the fast path keeps the change contract; agent handoff on growth
  is explicit; and the SALV template gate uses the same `L1`/`L2`/`G` vocabulary as the
  delivery skill.
- Added `docs/memory-decisions.md`: a provenance/decision register for the memory
  and context ideas received from several sources, a vocabulary map for the
  competing tier/state/confidence terms, lesson ownership, and a list of
  deliberately absent mechanisms. `docs/memory-model.md` and `workspace/memory/README.md`
  point at it; neither rulebook was duplicated.
- Round B: per-file byte budgets and a personal-skill contract gate in
  `registry_check.py` (name=dir, description present, bounded length); a bounded
  `templates/subagent-brief.md`; and `scripts/evidence_fingerprint.py` with
  order-independent, engine/locator-scoped content hashes plus a four-case
  boundary/known-bad test suite (`tests/`).
- OpenViking ideas folded in: one-line `> Abstract:` per domain/card shown in the
  digest for declared domains; a memory-audit line at close-out with stable skip
  reasons; a gated history-import rule; and a "never echo a credential" rule in
  global `AGENTS.md`.
- Round A of the context-engineering review (rules only, no new scripts): scope-order
  gate and external-effect fail-policy declaration in global `AGENTS.md`; three-way
  read outcomes and `UNAVAILABLE`-fails-the-gate in `docs/catalog.md` and
  `evidence-and-uat.md`; decision coverage for approved deviations; lazy-read and
  plan-quality discipline in `auto-abap-delivery`; plan preconditions/reversibility/
  thinnest first slice; artifact-derived `Next step` and card rebuild.
- README refreshed for the current setup: three-agent routing, loaded profile,
  curated backup script, installer copying whole skill trees, and the latest
  registry counts/date.
- `auto-abap-delivery` now recognizes a pre-approval recorded in project/program
  `AGENTS.md` as the approval for that exact scope (no re-ask on an already approved
  deploy), and has a fast path that routes one-to-three-step local changes to the
  developer skill instead of initializing a full run. Agent descriptions and the
  loaded profile now state the routing: `build` for toolkit/general work,
  `abap-developer-by-pongg` for one object/change, `abap-auto-delivery-by-pongg`
  for multi-slice runs to UAT. The last stale version label was removed.
- The developer agent and skill now treat a pre-approval recorded in a project or
  program `AGENTS.md` (for example LUF/ZMME011 end-to-end deploy) as the Pre-Flight
  approval for that exact scope, so a pre-approved deploy is not re-asked. Any change
  to target, objects, package/transport or operation still requires reconfirmation.
- Added the OpenCode `abap-developer-by-pongg` agent and `senior-abap-development`
  skill, adapted from the Copilot agent and `~/.agents/skills` source: Copilot-only
  tool lists, roster and lesson paths were dropped; skill routing was mapped to
  installed OpenCode skills; released-alternatives and cloud restrictions were
  added as a reference. The skill is for one bounded object/change and defers
  multi-slice runs to `auto-abap-delivery`.
- Improvements to `auto-abap-delivery` from `abap-skills-main`: RAP guardrail that a
  clean ATC result does not authorize a non-`transactional-consistent` classic API,
  lowest Clean Core Level rule, wrapper/exemption strategy, and compact AUnit
  mechanics without overriding the value-based test gate. Low-value/bloat and
  contradictory source material was not copied.
- Core improvement to `auto-abap-delivery` and its agent from the complete
  delivery bundle and eight exercise summaries: three new unversioned
  references — `methodology-resolution.md` (profiles with a pre-write dependency
  gate), `prog-local-class-methodology.md` (L1 local-only / L2 hybrid / G global,
  so class-first no longer means "must create SE24"), and
  `repository-reliability.md` (action contract, per-type postconditions, no blind
  replay). Updated capability intake with client/phase gates, state recovery with
  the action-contract schema, engineering judgment with local-class choice and
  cast evidence, evidence handoff with `NOT_RUN_BY_AUNIT_TOOL` / `NOT_REPORTED`
  / unpublished-binding states, and the workflow with methodology resolution.
  `FORM`/`PERFORM` is no longer a blanket ban: class-based is the first choice,
  with a recorded fallback for proven legacy/framework/toolchain/compatibility cases.
  No duplicate second brain, no design-roadmap content, no new scripts, and no
  version labels in new names; stale labels were stripped in touched files.
- Moved the "one fact, one home / narrowest wins" routing table from the
  rationale (`docs/memory-model.md`) into the operating rules
  (`workspace/memory/README.md`), leaving a pointer instead of a duplicate. The
  program-card template now links its Evidence section to the V9
  `docs/evidence/<run-id>/` package. No new vault, learning-candidate file or
  digest filter was added.
- Added a short `templates/profile.md` ("About me — ABAP Developer by Pongg")
  as the canonical, harness-neutral persona. A copy lives at
  `~/.config/opencode/profile.md` and is loaded via a new `instructions` entry
  in the existing global `opencode.json`. The 598-line Copilot agent was not
  copied: its tool names, roster, lesson paths and memory layout belong to the
  other harness; the profile keeps only durable working rules and points to
  `AGENTS.md`, `tool-map.md`, `docs/catalog.md` and `auto-abap-delivery`.
- Folded `build-salv-template` v1.1.0 into `sap-program-register` instead of
  adding a second skill: one question resolves object type + template (`PROG`
  with an existing SE38 template / bundled YSMILE SALV / plain class-first;
  `CLAS`/`FUNC`/`RAP` skip the gate). The full workflow and all 15 ABAP sources
  are bundled under `references/salv-template/`; the choice is recorded in
  `reports/DECISIONS.md` and the README, with no `program.yaml` schema change.
  A scope note keeps YSMILE local classes to small non-reusable reports.
  Copilot-kit was deliberately left untouched.
- Memory/second-brain polish: optional `Applies to` / `Release` / `Verified on
  system` bullets on landscape-specific knowledge entries, plus global rules
  that memory notes are data not instructions and facts carry a source tier.
  Instance data lives in git-ignored `workspace/`, so a fresh `Backup/` snapshot
  is needed to persist it off this machine.
- P0 patch to `auto-abap-delivery` from the two exercise results and the V9
  analysis: class-first new development (no new `FORM`/`PERFORM`, thin
  `PROG`/`FUNC` shells, Object Responsibility Plan + test-artifact placement),
  value-based optional unit tests with a `DIAGNOSTIC_DRIVER` taxonomy and no
  permanent test-driver program, per-object verification and repository
  reconciliation (`GHOST` gate), scoped owner confirmation, local-package and
  unpublished-service terminal rules, and a minimum post-run evidence package
  with `pending_human_review` learning candidates. Agent + skill live/repo
  copies match. V9 dynamic team planner, evidence scripts and qualification
  schema changes remain deferred pending a separate decision.
- Added the V8 `auto-abap-delivery` **control-plane skill** (11 references, 5
  scripts), the `abap-auto-delivery-by-pongg` coordinator agent, the
  `/auto-abap-delivery` command, `config/auto-abap-delivery/` (qualification
  schema + validator) and `docs/auto-abap-delivery/IDEA-V8.md`. The runtime
  qualification config stays `status: draft` with `qualified_scopes: []`, so the
  effective default is Attended Standard — no unattended write is unlocked.
- The V8 `opencode.fragment.json` was **not merged verbatim**: it uses the V1
  `permission` shape, a broad `python scripts/*` allow and puts `SKILL.md` in
  `instructions`, which breaks the explicit-invocation contract. OpenCode v2.3.2
  already discovers the skill/agent/command, so no config change was needed.
- `install.ps1` now copies whole skill trees (not just `SKILL.md`) and the
  `config/opencode-agents` / `config/opencode-commands` files, keeping existing
  names. `registry_check.py` lists `auto-abap-delivery` as a personal skill so
  it stays editable.
- Added the manual-only `opencode-backup` skill and `/opencode-backup` command.
  The skill is hidden from auto-invocation (`opencode/autoinvoke: false`,
  `disable-model-invocation: true`) and documents the dry-run → verify manifest
  → optional archive-only cleanup → restore handoff workflow.
- Backup hardening: `service.json` is excluded (it holds a plaintext OpenCode
  service credential) and the script now rejects a destination inside either
  source tree — copying `workspace/` into itself made robocopy recurse forever.
  Snapshots belong in the git-ignored `Backup/` folder, not under `workspace/`.
- Added `scripts/backup_opencode.ps1`: dated, hash-verified snapshots of the
  git-ignored `workspace/` instance data plus a curated copy of
  `~/.config/opencode` (junctions and stale/vendored files excluded and listed
  in `manifest.json`). Optional session-DB copy is marked unverified when
  OpenCode still holds the file. Dry-run and three live smoke tests passed.
- Added a git-ignored `.venv/` with `jsonschema` + pure-Python `ruamel.yaml`
  (Python 3.15 has no PyYAML wheel); both validators fall back to ruamel. Draft
  config, example config and the compatibility smoke test all validate clean.

## v0.8.3 — 2026-11-20

- Redesigned the personal `sap-mcp-upgrade` skill for **standalone, OpenCode-only
  MCP scope**. It scans only `mcp` entries in `opencode.json` and their backing
  packages — no VS Code/Copilot/Claude skills, no agents, no unrelated npm/uv
  tools, no skill-install suggestions. Manual-only trigger, built-in MCP registry
  with probe/changelog URLs, mandatory pre-update report, then a **radio
  mode question** (`Upgrade all (Recommended)` / `Upgrade selected` / `Cancel`);
  checkbox selection appears only when the user picks `Upgrade selected`, at
  upgrade-unit level (not per MCP entry), with ambiguous/unsafe rows disabled.
  Added an **auto-computed safety rank** (blast radius / config change /
  rollback / confidence) and an explicit question budget: 1 question for
  `Upgrade all`, 2 only for `Upgrade selected`, zero for safety ranking.
  Severity tiers (`security`/`breaking` never batched), a machine-local
  pending-restart state that blocks new upgrades, one daemon restart, one
  verification, and a terminal "no further upgrades pending". Live and repo
  copies match.

## v0.8.2 — 2026-11-20

- Relabeled from v0.9.0 before publication was kept; the v0.9.0 tag and Release
  were deleted and recreated at the same commit content. The changes below are
  treated as a patch-level clarification of the co-edit contract, not a minor
  feature release.

- Phase 1 of the local-index study: added an object-family capability matrix in
  `docs/coedit-capabilities.md` from read-only DS4/100 probes across the
  supplied TADIR type list. Editable text-source + hash is limited to PROG, INCL,
  CLAS, INTF, FUNC, DDLS, DCLS, BDEF, SRVD, DDLX (STOB read through DDLS);
  SRVD rejects comments, SRVB/FUGR/TRAN and DDIC metadata have no editable
  source. TADIR SQL stays unavailable because `SAP_ALLOW_FREE_SQL` is false.
- Co-edit contract now requires an **approval card + one question** before the
  first edit (no "type อนุมัติ" gate), and **mass activation per activation unit**
  via `activate_multiple` — includes before the main program, RAP bottom-up by
  layer, partial failure stops remaining units, no activation loop. Added the
  same `Activate / Units` fields to `templates/plan.md`.
- Added `docs/coedit-index.md`: a proposal for a **local object index**
  (nodes + tool-confirmed edges, hash_engine, provenance, invalidation),
  explicitly not a Knowledge Graph and never a write authority. Evidence: static
  analysis of a 445-file RAP export supplied locally as a sample (DS4/100 has no
  object of comparable complexity), plus a read-only DS4/100 probe on a CDS pair
  that does exist there — `impact` on the consumption view returns the DCL while
  `impact` on the interface view does not. Added an optional **disabled comment
  block** write mode to the same doc: syntax by object family (SAP Help CDS/BDL
  rules), dividers, placement when comments already exist, and the anchor/marker
  traps. Read-only syntax probes on DS4/100 then confirmed `*` blocks on PROG/
  CLAS/FUNC and `//` blocks on DDLS/DDLX/STOB/DCLS/BDEF are clean, but **SRVD
  rejects comments** ("Comments are not supported and will be deleted on save") — SRVD is excluded
  from comment-block mode and its proposal stays in the local manifest. Not the
  default; activation stays locked to DEFER for that mode. Gap register and
  catalog point at the proposal; no component implemented.
- Refreshed the registry baseline after the temporary `sap-gui` session, daemon
  restart and the new `opencode_console` namespace changed the live tool catalog:
  381 tools / 11 namespaces, 0 issues. Updated README counts and prompt cost
  (77.9k chars). The 7 warnings (catalogs over budget) remain human decisions.

## v0.8.1 — 2026-11-19

- Sandbox-tested the co-edit safety path on DS4/100 with a local test object:
  `object_state.sha256` detected an external edit activated after the baseline,
  a stale-hash edit was rejected with `SOURCE_DRIFT` and no overwrite, and
  `coedit_baseline.py` restored the pre-image as a forward write under CAS.
  Recorded in `docs/coedit-capabilities.md` and `docs/coedit-gap-register.md`.
  Limits: the object was local (`$TMP`), so TR membership was not tested; the
  three-way conflict branch and the 120 s cache window were not demonstrated.
  Sandbox residue (`ZCOEDIT_SANDBOX`, empty TR `DS4K904994`) was deleted through
  temporary `sap-gui` and verified gone; the SE10 find → F2 → delete path is
  recorded in `docs/coedit-capabilities.md`.
- Closed the remaining sandbox gaps on a second object inside a real open TR
  (`ZCOEDIT_SANDBOX2` in `DS4K904996`): detection worked with the TR feed live
  and no new revision; three-way merge preserved an unrelated intervening edit,
  while an overlapping hunk stopped with `UNDO_CONFLICT` and no write. The 120 s
  cache window was **not** reproduced with the mounted read tools and is
  recorded as unproven. Cleanup was blocked by GUI Scripting being disabled;
  the user deleted both artifacts manually and read-only checks confirm they are
  gone (400/404). The `sap-gui` policy file now allows `SE38`.

## v0.8.0 — 2026-11-19

- Program `CHANGELOG.md` now keeps **every** deploy row for the life of the
  program and carries a `TR` column, replacing the old "collapse to one line at
  release" rule. SAP version management still owns exact code diffs; the local
  table is the index that answers what changed and which TR carried it, including
  re-binding to a new TR after a release. Updated `templates/CHANGELOG.md`,
  `AGENTS.md`, `docs/design.md`, README and the `closeout.py` table hint. Existing
  program changelogs were not rewritten.
- Added `templates/RAP_INDEX.md`: a thin RAP read map organised by dependency
  chain, artifact layer and runtime phase, with a procedure for locating edits
  made in SAP outside the agent (TR scan → diff → impact) instead of re-reading a
  20–120 object stack. Template only — no existing program was changed and
  `specs_sync.py` does not mirror this file yet.
- Added `docs/catalog.md` §"Co-edit contract": `kind`/`complexity` paths,
  sync-on-touch, a per-batch activation gate with a structured handshake, and an
  explicit statement that an unreported open-TR edit is undetectable and must not
  be chased as a bug. `CHANGELOG.md` regained its `Scope` column (`CL:`/`RAP:`);
  `spec.md` gained the `last_tr_check` / `last_tr_seen` anchor; `program-register`
  records kind/object count/complexity; AGENTS and `design.md` point at the
  contract. TR stamps stay — no detector was removed.
- Patched the co-edit contract with five ideas merged from a review of another
  session's proposal, kept only where the mounted tools support them: event vs
  state facts with `source`/`by`/`verified_at` and a TTL, read/write/data cones,
  a `get_source(include_hash=true)` → lock → `edit_source(expected_source_hash)`
  → unlock write protocol, recognition-based handoff, and 409/423/404 routing.
  Deliberately left out: ETag conditional GET and `GetObjectDraft` (no mounted
  tool) and the cross-harness write ledger; per-write `.baseline` was added later
  in this release.
- Started Tier 0–2 of the co-edit gap plan from nine reviewed idea documents.
  Added `docs/coedit-capabilities.md` (per-harness tool facts) and
  `docs/coedit-gap-register.md` (accepted/deferred/rejected with reasons), plus
  `templates/coedit-state.json` for per-object hashes. The contract now separates
  Hint/Evidence/Guard, adds `object_state.sha256` as an observation beacon,
  engine-scoped hashes, a post-confirm commit window, post-write read-back,
  `verification_basis`/`confidence`, error routes 412/403/timeout, and a recheck
  circuit breaker. Verified in this harness that ai-dev does expose
  `expected_source_hash` (an earlier VS Code claim was based on scanning only
  `.js`) and that ARC-1 `object_state` returns sha256 — so the "unreported open-TR
  edit is always invisible" limit is narrowed to the no-baseline case. The
  read-only probe on DS4/100 then confirmed `object_state.sha256` stability and
  that ai-dev and ARC-1 produce different hashes for the same 10,538-byte source —
  so engine-scoped hashing is now evidence, not a precaution. Detection of a real
  external edit is still untested (no sandbox write).
- Finished Tier 3–5. Added `scripts/coedit_baseline.py` — a git-ignored,
  content-addressed pre-image store with `save` / `attach` / `get` / `list`, hash
  verification before storing and one entry per intent — and documented in
  `scripts/README.md` + `.gitignore`. Undo is now a write-forward under CAS with
  three-way reconcile, never a blind restore. `templates/RAP_INDEX.md` gained
  sentinels and a dirty frontier; `impact` alone is marked partial and must be
  combined with `deps`/`usages`. The contract gained safe-point human preemption
  and an evidence-card handoff, with attribution and authorization as separate
  questions. Tier 0–2 gap statuses were updated and the plan file recorded in
  `docs/plan-coedit-tier3-5-v080.md`.

## v0.7.9 — 2026-11-18

- A large customer FS now gets a thin read map: `templates/spec-index.md` seeds
  `spec/FS_INDEX.md` (topic → line ranges, ≤10-line summary, cover pages skipped).
  The fingerprint lives once in `spec.md` front matter (`fs_lines` / `fs_bytes`);
  `closeout.py` warns when it changes, because a new FS revision invalidates every
  line range in the map. Tested with a temporary fixture: mismatch warns, match stays
  silent.
- `templates/AGENTS.md` program block now carries the rollback rule SAP cannot cover:
  released TR → version management; open TR → copy the **active** source to
  `.baseline/<OBJ>_<TR>.abap` before first activation, delete at release. The why
  stays in `DECISIONS.md`, so `CHANGELOG.md` keeps its slim four columns.
- `specs_sync.py` refuses to mirror a file carrying a credential-shaped assignment
  or token and reports it as drift instead of silently copying it (7 regex cases
  tested). It also mirrors `spec/FS_INDEX.md` when present (the FS itself is still
  never mirrored).
- fr0ster `v24.0.0` (`8a9ed53`) recorded in `docs/fr0ster-v24-assessment.md`: tool
  counts re-derived from the generated docs, start-time restrictions, opt-in data
  tools, and the local tool-overlap analysis. The capability matrix and the parked
  plan point at it. Nothing installed.
- `opencode.json` now states `SAP_ALLOW_DATA_PREVIEW=false` and
  `SAP_ALLOW_FREE_SQL=false` explicitly for all five SAP MCP entries. ARC-1 already
  defaulted to false; the ai-dev engine does not read these variables, so its data
  tools stay mounted — the document records the gap and the un-applied option.
- New personal skill `sap-data-verify`: read-only, Clean-Core-first data verification
  through ARC-1; probes both gates and stops to ask before opening them. Source in
  `config/opencode-skills/`, installed to global skills, listed in `PERSONAL_SKILLS`,
  registry refreshed. Appendix L maps the local `arc1-*` namespaces. A same-named
  Copilot skill already existed and was not touched.
- New personal skills `sap-project-unregister` and `sap-program-unregister`, plus a
  shared §"Unregistration contract" in `docs/catalog.md`. Every invocation asks Q1
  (local `_archive` or hard delete) then Q2 (final confirm, default cancel); no
  inherited approval, no cascade, no SAP/TR/credential changes, no GitHub archive,
  and `_archive` is never pushed to git. Installed globally and added to
  `PERSONAL_SKILLS`.

## v0.7.8 — 2026-11-18

- The committed registry baseline was refreshed to the current machine snapshot.
  No toolkit asset was added or removed.

## v0.7.7 — 2026-11-18

**Enabling a profile and reading SAP docs are both written down now.**

- `sap-project-register` now explains how to actually enable a profile later: edit
  `opencode.json` to `enabled:true`, store the secret, restart the daemon. The
  OpenCode UI toggle changes only the running daemon's state — it is not written
  back to the file — so enabling by toggle alone is lost on restart.
- `sap-docs` (`mcp-sap-docs`) is now enabled and documented as the preferred source
  for SAP documentation, released APIs and clean-core levels: `tool-map.md` routing
  plus a working-method knowledge entry. Verified live with
  `sap_get_object_details(CLAS, CL_ABAP_REGEX)` → level A. The registry baseline and
  README numbers were refreshed to the 2026-11-18 snapshot (18 servers, 205 tools).

## v0.7.6 — 2026-11-17

**A no-write re-test caught a scaffold gap; registration now asks for it.**

- `sap-program-register` handles an older project scaffold whose `project.yaml` has
  no `allowed_packages`: it asks the user once, uses the answer for this program
  only, and records the source in DECISIONS — it never edits the project manifest.
  Found in a no-write re-test of the registration dialogue.

## v0.7.5 — 2026-11-17

**Registration reads before it asks; the engine baseline is current again.**

- `sap-program-register` now does a read-only object lookup before collecting
  package and TR: `SAPSearch(tadir_lookup)` for existence/package and
  `SAPTransport` for the TR. Found objects reuse those values; a failed or
  inconclusive lookup asks the user instead of guessing. No SAP writes.
- Knowledge domains are now chosen from three bundles (recommended / +sap-data /
  choose myself), with the recommendation prefilled from the stated purpose,
  replacing the five-item multi-select.
- The committed registry baseline was refreshed after the SUS engine registration:
  the disabled `ai-dev-sus-100` / `arc1-sus-100` namespaces are recorded the same
  way as the existing ds4/gsd engines — no profile name, path or credential. The
  parked waiting-list item is closed.

## v0.7.4 — 2026-11-17

- Split `sap-project-register` into two skills with one shared contract in
  `docs/catalog.md`: `sap-project-register` owns the project folder, manifests,
  portfolio `INDEX.md` and optional disabled MCP profile;
  `sap-program-register` owns the program folder, spec, changelog and memory card.
  Both ask for every unknown at invocation; neither deploys or connects to SAP.
- Register skills now follow a shared "Question mode": one question at a time via
  the `question` tool, known values reused instead of re-asked, each answer
  validated before the next, batch only on request. Based on a live test where the
  AI posted a 12-field form and re-asked the client and user it already knew.
- `sap-program-register` scaffold now satisfies the checks it runs: it writes the
  program's own INDEX row and project README entry, marks no-FS REQ rows `none`,
  uses `spec_version: 0.1` for a draft, pins the FS version to the file-name token,
  and names the memory card so closeout can resolve the spec path.
- Transport is now program-level and optional. Project registration no longer asks
  for a TR: it writes `allowed_packages` and `transport: none` to `project.yaml`.
  Program registration skips the TR question when `allowed_packages` is `$TMP` only;
  otherwise it offers "TR / not yet / $TMP" and never invents a number.
- Owner is no longer a registration input: removed from both skills, the project
  manifest, and the `spec.md` front-matter template.

## v0.7.3 — 2026-11-17

**Clean-up after v0.7.2: an MCP upgrade skill, a repository catalog, and a parked pin plan.**

- `sap-support-case` parked from the live skills folder; the baseline was refreshed.
  The skill catalog is back inside its 20k budget (19.4k across 31 OpenCode skills).
- New personal skill `sap-mcp-upgrade` — probe upstream, bump one version token after
  approval, verify the live process and package metadata, then restore `enabled:false`.
- `docs/catalog.md` maps every top-level folder by owner and committed/generated state.
  `registries/README.md` separates the committed baseline from git-ignored live
  snapshots. No file moved, so no consumer changed.
- `docs/plan-mcp-pins.md` parks the plan for one manifest plus a check/write script
  for MCP versions. Not approved to execute; reference only.
- Deferred folder moves (plans into `docs/plans/`, registries into `baseline/` +
  `live/`) are recorded in `docs/catalog.md` with their cost. Not done — paths stay
  stable. `config`, `scripts`, `templates`, `plugins`, `workspace` untouched.
- `sap-gui` is pinned to `0.6.1` and back to `enabled:false` after verification.
  Measured numbers in `README.md` updated to the 2026-11-17 snapshot: 115 skills,
  270 tools, 58.3k chars per session.
- New personal skill `sap-project-register` — scaffolds a project/program from the
  adopted design (folders, manifests, spec, memory card, INDEX, optional MCP profile),
  asks for every unknown, and never deploys or connects to SAP.

## v0.7.2 — 2026-11-17

**Several SAP engines can run at once — now with the rules written down.**

- `scripts/tools_now.py` reads the launcher command from the OpenCode MCP config, joins
  it to the SAP profile, and prints the armed posture per server (`writes`,
  `transport`, `data`, `sql`, `git`, package ceiling). A live tool list no longer has to
  be mistaken for permission. `--check` fails when two write-armed servers share one
  system/client; a server the script cannot read is reported as `POST unknown` instead
  of being assumed read-only.
- `sap-mcp.ps1` gains `-AllowTransportWrites`, `-AllowDataPreview`, `-AllowFreeSql`,
  `-AllowGitWrites` and `-AllowedTransports`. All default to off; transport and Git
  writes are refused without `-AllowWrites`, and transport writes without a whitelist
  warn that release has no package check.
- `docs/mcp-orchestration.md` — what actually happens when two servers run together
  (ETag revalidation makes cross-engine reads trustworthy; the ADT lock serialises
  concurrent writes; sequential read-modify-write silently loses an update), the
  ai-dev/arc-1 coverage split, the three enforcement layers, and the posture table.
- The workspace rule changes from "one writer per task" to **"one object, one writer,
  one session"** — the old wording was too strict about idle servers and too vague
  about the failure it was preventing.
- Example profile names in `config/opencode-sap/` are now placeholders
  (`example-100`), so a local profile name cannot leak into a push.
- New personal skill `sap-auditor` — one pass in three blocks: **audit** (every claim
  against tier 1-2 evidence, `path:line`, ✅/⚠️/❌/🕰/❓), **mentor** (numbered fixes,
  each with a why), **commentator** (≤3 `trigger → consequence → guard` risks), plus a
  coverage line that names what was *not* read. It delegates lint and transport gates to
  the existing skills instead of re-implementing them; `registry_check.py` lists the
  name in `PERSONAL_SKILLS` so the scanner does not file it under vendor.
- `install.ps1` copies `config\opencode-skills\` into `~\.config\opencode\skills` when a
  name is not there yet, so a reinstall restores the personal skills instead of losing
  them. The `sap-auditor` skill is the first one that ships.
- `closeout.py` reports a shipped file that names this machine's paths as an issue. The
  repository is also the installer for the next machine, so a frozen `C:\...` is a
  defect, not a detail; shipped files use repo-relative paths or `~`.
- Knowledge stays one flat tree, filed by competence. `memory/knowledge/README.md` now
  carries the routing table (project decision → `spec.md` / `reports/DECISIONS.md`,
  universal rule → the domain file, procedure → a skill, one-off → drop). Only the
  `domains:` line is checked — an unknown name on a card is an issue, because the digest
  would otherwise load every file. A `Z…` keyword warning for misfiled rules was tried
  and removed: it missed project fields like `MENGE_PD`, and a partial check reads as
  coverage. Two entries were rewritten to keep their project detail in `Evidence`.
- Conventions now have an explicit home. `Projects\<PROJECT>\AGENTS.md` §Conventions
  holds what every program in one project follows (naming prefixes, object types,
  transport and client rules); the knowledge entry for DDIC naming became "read the
  project's convention, or ask", and the concrete `ZD_`/`ZE_` rule moved into the LUF
  project file. The four homes and their precedence are in `docs/memory-model.md`.
- The fr0ster column of `docs/mcp-capability-matrix.md` was re-derived from that
  repository's generated tool docs at `b29d6ff` (still `main` on 2026-11-17), and four
  figures were wrong: the tool count is **292 total / 188 high-level / 74 read-only**
  (not "41 compact" — the compact binary is a separate shape, 28 tools or 17 read-only),
  MSAG is **C R U D** rather than "C R", **DCL has no tool**, and there is no lint or
  format tool — syntax check only, as `Check<Type>`. The README bullet
  `GetView`/`CreateView`/`UpdateView` is still stale at `README.md:273`.
- fr0ster is **absent by design, not disabled**: there is no entry for it in
  `opencode.json`, so it cannot connect and costs nothing. Both docs now say that and
  state the credential path from its own guide (env vars, no keychain route) rather
  than from a guess.
- `docs/mcp-orchestration.md` marks the permission layer as **documented, not
  configured** — `opencode.json` carries no `agents` and no `permission` block, so no
  agent is pinned to an engine today. The matrix also states the rule actually in
  force ("one object, one writer, one session") instead of the older "one writer per
  task".
- The vendor's arc-1 guide (v1.7.0) is **older than the clone the toolkit verifies
  against** (1.10.1 at `755a265`): its object-type list omits DOMA/DTEL/TTYP, which the
  source carries (`src/handlers/object-types.ts:135-143`). The source wins, and the
  toolkit cites the source.
- New personal skill `sap-mcp-upgrade` — probe upstream, bump one version token
  after approval, verify the live process and package metadata, then restore
  `enabled:false`. `install.ps1` copies it; `PERSONAL_SKILLS` marks it editable.
- `docs/catalog.md` maps every top-level folder by owner and committed/generated
  state. `registries/README.md` now splits committed baseline from git-ignored
  live snapshots — no files moved, so no consumer broke.

## v0.7.1 — 2026-11-15

**A fresh install starts clean.**

- `templates/instance` now seeds every file `memory_check.py` requires —
  `user-profile`, `corrections`, `tool-map`, `expertise`, `skill-candidates`,
  `agent-registry` — plus one knowledge domain (`working-method`). A new instance
  reports 0 issues instead of 7.
- A missing `registries/tools-snapshot.json` is a warning ("restart OpenCode so the
  plugin captures the catalog"), not an issue: on a fresh install the file cannot
  exist yet.
- Found by installing v0.7.0 from a clean clone into a temporary config directory.

## v0.7.0 — 2026-11-15

**First installable release.** The toolkit and the instance are separate, the
installer is one command, and the SAP credential path is the native Windows dialog.

- `workspace/` is the instance (memory, specs mirror, reports) and is git-ignored;
  `scripts/_paths.py` resolves it, with `ABAP_WORKSPACE`, `ABAP_PROJECTS_ROOT` and
  `ABAP_INDEX` for an install outside the original portfolio.
- `install.ps1` — idempotent, `-DryRun`, `-Seed`, `-SkipAgents`, `-SkipRegistry`,
  `-WithSap`: instance, memory junction, tool-snapshot plugin entry, AGENTS pointer,
  registry baseline. It never touches SAP profiles, credentials or MCP entries, and
  backs up every file it rewrites.
- SAP launcher: password from `SAP_PASSWORD` → Windows Credential Manager →
  the native sign-in dialog (`CredUIPromptForCredentials`), which stores what you
  type so the next start is silent. One mutex stops two directories opening two
  dialogs. The launcher names the password source on stderr every start.
- `mcp.timeout.startup` 180 s, because the dialog needs more than the 30 s default.
- `tool-snapshot` publishes only from the workspace that owns the toolkit, so a
  second OpenCode window no longer overwrites the numbers.
- `registry_check.py` ignores the `mcp.timeout` block when listing servers.
- MIT licence. `SECURITY.md` splits toolkit data from instance data.
- README rewritten as an install-first document.
- Repository renamed `abap-agent-workspace-opencode` → `abap-ai-opencode-toolkit`;
  GitHub redirects the old URL and a one-shot script moved the local folder, the
  junction and every absolute path outside the repository.

Detailed entries below: v0.6.2 → v0.5.20.

## v0.6.2 — 2026-11-15

**Store first, verify after; only a 401 removes the credential.**

- `store-sap-secret.ps1` writes to the keychain and then probes
  `/sap/bc/adt/discovery`. A 401 deletes the credential again; a 400 or a network
  error keeps it and says so, because those are request-shape problems, not a
  rejected password.
- A non-401 failure prints 160 characters of the SAP response body, so the cause is
  visible instead of guessed.
- `-NoVerify` skips the probe entirely.
- Why: a pre-flight 400 blocked a password the user had just typed, and the screen
  could not tell it apart from a wrong password. 401 is the only signal SAP uses for
  "rejected".

## v0.6.1 — 2026-11-15

**The SAP password prompt is the native Windows dialog, and MCP startup waits for it.**

- `sap-cred.ps1` gains `Prompt()` (`CredUIPromptForCredentials`, generic credentials
  + do-not-persist). `sap-mcp.ps1` and `store-sap-secret.ps1` use it instead of
  `Get-Credential`, so the window is the Windows sign-in dialog (`SAP sign-in`), not a
  hand-built form.
- First start of a profile: dialog -> password -> stored in the keychain -> the next
  start is silent. A `Local\sap-mcp-prompt-<profile>` mutex makes two directories share
  one dialog instead of opening two.
- `opencode.json`: `mcp.timeout: { startup: 180000, catalog: 60000 }`. The legacy
  `mcp.<name>` entry shape accepts only an integer `timeout`; an object there makes the
  whole entry disappear — the object belongs at `mcp.timeout`.
- `sap-mcp.ps1 -PromptTest` shows the dialog without connecting and never stores.
- Found on the live machine: `SAP_PASSWORD` is also set as a Windows user environment
  variable, which bypasses the keychain and exposes the password to every process.
  Remove it once the keychain or the dialog is in use.

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
- Removed the orphaned `~/.sap-adt-cli` profile (`dev`, `allow_write: true`)
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
