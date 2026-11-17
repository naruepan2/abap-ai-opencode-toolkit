# Plan: one manifest for MCP servers and version pins

> Source: `templates/plan.md`. Toolkit-level plan; lives in `docs/` because no
> `spec.md` owns it. Written for later, **not approved to execute**. The only
> approval so far is "write and keep this plan" (user, 2026-11-17).
> Every step that edits `opencode.json`, adds code, or refreshes a registry needs
> a new approval. The plan is a hypothesis; revise it when evidence disagrees.

Goal:      Make adding an MCP server and upgrading its version a manifest edit plus
           one check, not four manual edits and a memory exercise.
Acceptance: A fresh session can run `python scripts\mcp_pins.py --check` and get
           exit 0 when the manifest matches the live config, exit 1 when a pin is
           missing, mismatched, or a server is new. `--probe` reports a newer
           upstream version read-only. `registry_check --brief` prints the pin.
           One documented upgrade procedure works for every server. That is done.

## Contract

- FS:          none — no customer functional spec; this research is the scope
- Spec:        none — toolkit-level, not a program folder; this plan is the scope
- ADT path:    none for writes. No SAP object is created, changed or activated.
- Change type: extend (tooling, not product code)
- Production:  not live — no SAP system is connected by this plan
- Target:      none. `~/.config/opencode/opencode.json` is the live config to read
               and, only after approval, to write.

## Approved

- Write:      **this file only** (`docs/plan-mcp-pins.md`)
- Activate:   no
- Transport:  none
- By:         user + 2026-11-17 — approval limited to writing the plan
- Not approved: `config/mcp-catalog.json`, `scripts/mcp_pins.py`,
  `scripts/registry_check.py`, `docs/mcp-upgrades.md`, `opencode.json`,
  `registries/*.json`, or any npm/uvx install.

## Findings already established (do not re-research)

| Fact | Evidence |
|---|---|
| Live config holds 10 MCP entries, but only `sap-gui` carries a version pin (`==0.6.1`) | `opencode.json` read 2026-11-17; `Select-String '=='` found one line |
| `playwright-mcp`, `open-computer-use` and `windows-mcp.exe` are unpinned | same read: command arrays have no version token |
| `registry_check.scan_mcp()` records `command_kind` and `url_host` only — no version | `scripts/registry_check.py:240-276` |
| Every upgrade currently touches four places: config, daemon restart, registry refresh, memory/tool-map | observed across the 0.6.0 -> 0.6.1 change on 2026-11-17 |
| `sap-gui` 0.6.1 is live and verified three ways | live process command line, `mcp_sap_gui-0.6.1.dist-info`, successful `sap_list_connections` call |
| `sap-gui` is currently `enabled:true` only for this GUI task; steady state is `false` | `tool-map.md` §"SAP on-demand" |
| `closeout.py` rejects shipped files naming this machine | `scripts/closeout.py:246-269`; the manifest must use no drive letters |

## Todo

- [ ] 1. Confirm the manifest field set against all 10 live entries; record which servers are uvx, npx, local exe, or remote — ~20 min — read-only — evidence: one table in Log
- [ ] 2. Write `config/mcp-catalog.json` with `server`, `kind`, `package`, `pin`, `upstream_api`, `steady_enabled`, `optional_namespace`, `expected_tools` — ~30 min — evidence: parses, no `C:`/`D:` paths
- [ ] 3. Add `scripts/mcp_pins.py --check` (stdlib only): compare manifest to live config; exit 1 on missing pin, mismatch, unknown server, or wrong package — ~45 min — evidence: fixture run
- [ ] 4. Add `--probe`: call PyPI/GitHub release API read-only and report a newer version without writing — ~30 min — evidence: reports 0.6.1 as current on 2026-11-17
- [ ] 5. Add `--write`: patch only the `==`/`@version` token, keep a timestamped `.bak`, idempotent; refuse to touch `enabled`, `url`, or profile paths — ~45 min — evidence: temp-copy diff shows one token changed
- [ ] 6. Extend `registry_check.scan_mcp()` with `pin` and `package`; print one pin line in `--brief` — ~30 min — evidence: brief shows `sap-gui 0.6.1`
- [ ] 7. Write `docs/mcp-upgrades.md`: read changelog -> bump manifest -> `--write` -> restart daemon -> read-only tool + dist-info check -> registry refresh -> update memory evidence -> restore `enabled:false` — ~30 min — evidence: doc matches the 0.6.1 run retold step by step
- [ ] 8. Test `--check` with three fixtures: pin mismatch, missing server, new server — ~30 min — evidence: exit 1 with the right reason each time
- [ ] 9. Test `--write` on a **copy** of `opencode.json` in temp, never the live file — ~20 min — evidence: before/after hash of untouched fields
- [ ] 10. Run `registry_check.py --refresh` after the code change and commit the baseline delta — ~15 min — evidence: `changes=0 new=0 missing=0`
- [ ] 11. Close-out: `memory_check --brief`, `closeout.py`, then set `sap-gui` back to `false` and ask the user to restart the daemon — ~20 min — evidence: clean checks + config read-back

Status legend: `[ ]` todo · `[x]` done (with evidence) · `[~]` blocked (with the question)

## Guardrails

- Scripts **report** upgrades; they never auto-install or auto-enable. A vendor
  changelog must be read before a pin moves (Evidence over guesses).
- The manifest is portable: no machine paths, no credentials, no customer IDs.
  Live paths stay in `opencode.json`, which is not committed.
- One owner per artifact: one script writes config, one check reads it, one doc
  owns the procedure. No parallel edits to `opencode.json`.
- A new server enters the manifest with `steady_enabled:false`. The script may
  print a snippet; it must never flip `enabled` on its own.
- Stop if a gate is unanswered, if two consecutive attempts fail, or if a step
  would leave the approved scope.

## Log

> One line per tick: what was verified and the evidence. This survives a reset.

- 2026-11-17 plan written — approval limited to this file; no config, code, registry or SAP change made
