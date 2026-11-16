# Plan: evaluate fr0ster as a fourth (or replacement) SAP engine

> Source: `templates/plan.md`. This is a **toolkit-level** plan, not a program plan:
> it lives in `docs/` because no `spec.md` owns it. It is written for later, not
> approved to execute. The one approval so far is "write and keep this plan"
> (user, 2026-11-17). Every step that touches live config or puts a password on
> disk needs a **new** approval at todo 6.
>
> The plan is a hypothesis. When evidence disagrees, revise it — do not push
> through. ≤12 todos; one verifiable unit each.

Goal:      Decide from measured evidence whether `@mcp-abap-adt` should stay absent,
           be added as a task-scoped read-only engine, or be trialled as a full
           replacement for ai-dev + arc-1.
Acceptance: All 5 comparison tasks in `docs/comparison.md` are run on both stacks,
           the before/after context cost is recorded, and one of the three decisions
           is written in the Log with its evidence. That is the stop condition.

## Contract

- FS:          none — no customer functional spec; this research is the scope
- Spec:        none — toolkit-level, not a `Projects/<P>/<PROGRAM>` folder; this plan is the scope
- ADT path:    none for writes. This evaluation is **read-only**. No `SAPWrite`,
               no `write_source`, no activation, no transport mutation.
- Change type: extend (evaluation; no product code changes)
- Production:  not live — no SAP object is created, changed or activated
- Target:      DS4 client 100 may be read. Client 900 untouched. No transport.

## Approved

- Write:      **this file only** (`docs/plan-fr0ster-evaluation.md`)
- Activate:   no
- Transport:  none
- By:         user + 2026-11-17 — approval limited to writing the plan
- Not approved: `opencode.json`, `~/.config/opencode/**`, npm global installs,
  any file containing a SAP password, any change to the running MCP catalog.

## Findings already established (do not re-research)

| Fact | Evidence |
|---|---|
| fr0ster is **not installed** (`npm ls -g` shows only `arc-1@1.10.1`) | local check 2026-11-17 |
| Node 22 or 24 required; this machine is **v26.13.1** → outside supported set | `INSTALLATION.md:94`, `node -v` |
| npm ≥9 required; machine has 11.20.0 ✅ | `INSTALLATION.md:94`, `npm -v` |
| Process env vars alone are **not a destination** — server boots in tool-inspection-only mode | `server.json` env var description, `README.md:358` |
| A chosen `.env` is read **and written back** with a renewed token → secret on disk | `README.md:408` |
| `SAP_SYSTEM_TYPE=onprem` and `SAP_CONNECTION_TYPE=http` are mandatory; no defaults | `server.json`, `README.md:420` |
| TLS needs `NODE_EXTRA_CA_CERTS` pointing at a PEM; DS4 profile has no `tls_ca` | `INSTALLATION.md:84-90`, `profiles.json` |
| OpenCode is **not** in fr0ster's configurator docs → write `opencode.json` by hand | `CLIENT_CONFIGURATION.md` (0 matches for "opencode") |
| `compact-ro` = 17 read-only tools · `core-ro` = 74 · full core = 292 | generated tool docs at `b29d6ff` |
| fr0ster has no `agents/` or `skills/`, no git, no lint, no DCL, no ENQU write, no classic-view tool | repo root + generated tool list |
| Current cost: tools **49,303 chars / 329** (budget 28,000) · skills **20,216 / 31** (budget 20,000) | `registry-report.md`, 2026-11-17 |
| `sapnwrfc.dll` exists in `System32` → RFC/SNC path is available but needs a login product | local check 2026-11-17 |
| Server packages are AGPL-3.0-only; the library is Apache-2.0 | `package.json` of `core-ro`, `compact` |

## Todo

- [ ] 1. Confirm a side-by-side Node 22 or 24 exists (do **not** replace the global Node) — ~20 min — read-only — evidence: exact `node -v` and its install path recorded in Log
- [ ] 2. Install `compact-ro@23.1.0` under that Node, no config change — ~20 min — evidence: `npm ls -g` line + `mcp-abap-adt-compact-ro --version`
- [ ] 3. Decide the credential path and record it here: (a) temporary `.env` with restricted ACL + deletion after use (**needs password-on-disk approval**), (b) DS4 service key + JWT browser login, (c) SNC with Secure Login Client — ~30 min — evidence: one decision row in Log with reason
- [ ] 4. Capture the baseline cost line verbatim into Log — ~5 min — read-only — evidence: `python scripts\registry_check.py --check --brief` output
- [ ] 5. Draft (do **not apply**) the `opencode.json` entry: `mcp-abap-adt-compact-ro --env-path=<path> --system-type=onprem`, `enabled: false` — ~15 min — evidence: snippet here + hash of live `opencode.json` unchanged
- [ ] 6. **GATE — BLOCKED until the user approves** a temporary, disabled-by-default config entry plus the credential choice from todo 3. Record `BLOCKED: <the one question>` in Log and wait. Do not loop this gate.
- [ ] 7. Apply the entry, verify 17 tools mount and `tools_now.py` prints `POST unknown` for the new namespace — ~20 min — evidence: tool catalog count + script output
- [ ] 8. Run the five candidate tasks from `docs/comparison.md` on both stacks; fill a small scorecard (tool calls, evidence, time, actual engine chosen) — ~90 min — evidence: table appended to Log
- [ ] 9. Capture the after-cost and compute the delta from todo 4 — ~10 min — evidence: two lines side by side
- [ ] 10. Write the decision: **drop** (remove entry, refresh baseline), **keep task-scoped read-only**, or **full-core trial** — ~20 min — evidence: decision + which acceptance criterion it met
- [ ] 11. Close-out: drain the open `fr0ster-not-installed` row in `corrections.md`, update `docs/mcp-capability-matrix.md` only if a fact changed, run `python scripts\closeout.py` — ~20 min — evidence: clean close-out output

Status legend: `[ ]` todo · `[x]` done (with evidence) · `[~]` blocked (with the question)

## Decision criteria (set before running, so the result cannot be reinterpreted)

- **Drop** if no comparison task shows a read that ai-dev + arc-1 cannot already do,
  or if the only acceptable credential path puts a password on disk with no
  service key available.
- **Keep as task-scoped read-only** if at least one task needs DOMA/DTEL/TTYP or
  a debugger/batch read that the current two engines cannot deliver — and the
  credential path is approved.
- **Full-core trial** only if ≥4/5 tasks are clearly better **and** an agent/skill
  migration plan exists (24 vendor agents cannot be edited in place) **and** Node
  22/24 is accepted **and** the AGPL server is acceptable. Absence of any one of
  these means no full-core trial.
- Stop immediately if a gate is unanswered, if two consecutive attempts fail, or
  if a step would leave the approved scope.

## Log

> One line per tick: what was verified and the evidence. This survives a reset.

- 2026-11-17 plan written — approval limited to this file; no config, npm or SAP change made
