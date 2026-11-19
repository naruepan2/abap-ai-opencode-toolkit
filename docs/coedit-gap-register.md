# Co-edit gap register — decision record

Nine idea documents were reviewed on 2026-11-19: the original co-edit brief, the ChatGPT sol5.6
analyses (`human-ai-coedit-analysis-ideas*.md`, `human-ai-coedit-q1-q15-systematic-ideas.md`,
`human-ai-coedit-lean-evidence-protocol-v2.md`) and the VS Code side
(`human-ai-coedit-object-evidence-brief.md`, `human-ai-coedit-q1-q10-analysis-idea-review.md`,
`test1.md`). All are **INPUT** — no statement from them is evidence by itself.

This file records what we decided about those ideas. The **rules** live in
`docs/catalog.md` §"Co-edit contract" and the **tool facts** in
`docs/coedit-capabilities.md`. Do not duplicate either here.

Status: `accepted` | `modified` | `deferred` | `rejected`.

| # | Gap / idea | Status | Why |
|---|---|---|---|
| G1 | human draft pending, not activated | accepted | `INACTIVE_OBJECTS` + `object_state.hasInactiveDivergence` are mounted |
| G2 | human edited + activated after we observed | accepted; two sandbox tests 2026-11-19 | detected on a local `$TMP` object and again on `ZCOEDIT_SANDBOX2` inside open TR `DS4K904996` (status `D`, 1 object, no new revision) |
| G3 | human edited + activated before we ever observed | rejected as fixable | no baseline exists → information limit, record and stop chasing detectors |
| G4 | edit lands between our read and write | accepted; sandbox tested 2026-11-19 | stale-hash edit returned `SOURCE_DRIFT`; source unchanged |
| G5 | read right after activation sees stale source | accepted | `force_refresh` / different engine / post-write read-back |
| G6 | timeout after write, outcome unknown | accepted | read-after-timeout, zero replay until outcome known |
| G7 | same SAP user from two harnesses | accepted, local only | `by` + `harness` + `intent_id` from explicit human choice; never infer |
| G8 | RAP 120+ objects read repeatedly | accepted | `RAP_INDEX.md` sentinels + dirty frontier + `deps`/`usages`; still benchmark before a graph |
| G9 | undo restores over an intervening edit | accepted; sandbox tested 2026-11-19 | clean undo restored A; three-way non-overlap merged A's L2 with C's L3 under CAS; overlapping hunk produced `UNDO_CONFLICT` and no write |
| G10 | verification loop / duplicate reads | accepted | read-once evidence + invalidation + budget + circuit breaker |
| G11 | simultaneous writers in two harnesses | deferred | CAS already prevents lost update; ledger/broker is UX only until there is collision evidence |
| G12 | ETag / 304 as a guard | rejected | no mounted tool exposes it; do not invent a rule |

Other decisions:

- Full Knowledge Graph, graph server, vector store, background crawler: **deferred** —
  the lean document itself admits added overhead; prompt cost is already over budget.
- Custom SAP Z-table / central coordination service / new `RepositoryObjectHead` tool:
  **deferred** — needs governance and approval before any new tool or object.
- `expected_source_hash` mandatory in code: **rejected as a code change** — the
  schema marks it optional; we enforce it in the working method and write guard.
- AI-inferred actor / TR / business capability: **rejected** — explicit human choice only.
- Session scope, change unit + physical write-set + observation strategy:
  **accepted as vocabulary** — no separate file format; `spec/coedit-state.json`
  holds observations, `CHANGELOG.md` holds intent/history.

Review gate: any idea promoted from `deferred` needs a read-only probe, a
negative test, and an explicit approval recorded here with date and evidence.
