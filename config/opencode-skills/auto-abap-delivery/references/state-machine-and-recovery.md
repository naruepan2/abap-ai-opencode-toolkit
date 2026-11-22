# State machine and recovery

Top-level: `DRAFT -> AWAITING_APPROVAL -> QUEUED -> STARTING -> RUNNING -> VERIFYING_FINAL -> READY_FOR_UAT`.
Exceptional: `BLOCKED`, `PAUSING -> PAUSED`, `RECOVERING`, `FAILED_SAFE`, `CANCELLED`, `SUPERSEDED`.

RUNNING substates: DISCOVERING, ANALYZING_IMPACT, PLANNING_TEAM, DESIGNING_TESTS, IMPLEMENTING_SLICE, ACTIVATING, TESTING_FOCUSED, REPAIRING, TESTING_REGRESSION, RUNNING_ATC, AUDITING, DOCUMENTING, BUILDING_UAT_PACK, REPOSITORY_RECONCILIATION, BUILDING_POST_RUN_EVIDENCE, REPAIRING_EVIDENCE.

`REPOSITORY_RECONCILIATION`: after an uncertain/failed create or activation, persist intent, read TADIR/source/active-inactive/lock/package, classify `ABSENT`/`PARTIAL`/`GHOST`/`ACTIVE`/`INACTIVE`, then cleanup or Decision Inbox; retry only after reconciliation. `BUILDING_POST_RUN_EVIDENCE` uses a frozen source/object inventory; a failed evidence-consistency gate enters `REPAIRING_EVIDENCE` and never advances to `READY_FOR_UAT`.

Persist transition actor/reason/time, command ID, spec revision, before/after hashes, evidence IDs, and lease fencing token. Accept side effects only with active lease, matching token, correct SID/client, matching hashes, allowed object/action, valid TR/lock, and no blocking decision.

After restart: acquire new fencing token; load append-only logs; rediscover tools/identity; identify in-flight command; reconcile source, active/inactive version, lock, TR and evidence against SAP; classify replay safety; persist recovery report; resume only from a legal state.

Replay: reads/tests without side effects may repeat. Source write requires hash reconciliation. Activation requires active/inactive reconciliation. External sends, postings, commit/mass updates never replay without idempotency proof and are normally outside this skill.

## State-changing call contract
For every create/edit/activate, persist an `action_contract`: `command_id`, `intended_object`, `intended_action`, preconditions (source hash, SID/client, transport/lock), expected postconditions, and `reconciliation_required`. A success message is a claim; read back source, active/inactive state, object inventory and postconditions before accepting it. Per-type postconditions are in [repository-reliability.md](repository-reliability.md).

## Review states
Add `REVIEW_PENDING`, `REVIEWING`, and `RECONFIGURING`. Review approvals are revisioned evidence snapshots and become stale when source, dependency, spec, target, profile, or evidence changes. Recovery must restore open reviews and revalidate their snapshot before applying an answer.
