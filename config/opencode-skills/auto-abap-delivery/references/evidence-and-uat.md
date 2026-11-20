# Evidence and UAT handoff

Evidence fields: ID, task/run, target SID/client, spec revision/hash, autonomy-envelope hash, object, source/dependency hashes, check, raw result location, captured time, limitations, freshness.

Invalidate evidence when source, dependency, spec, target, relevant configuration, or reconciled command boundary changes.

Before `READY_FOR_UAT`: all required slices complete; every acceptance criterion maps to fresh automated evidence or explicit manual UAT; no `REWORK`; syntax/activation, focused/regression tests, required ATC/CVA/readiness and guardrails pass or have approved disposition; temporary artifacts are cleaned/disclosed; transport is unreleased.

UAT pack: executive summary; approved revisions; changed objects; before/after; acceptance traceability; ABAP Unit/ATC/system cross-check/guardrail results; limitations and residual risk; exact UAT client, scenarios, data, steps and expected results; transport status; rollback/disable approach; evidence index; explicit statement that production action was not performed.

## Per-object verification matrix
Never claim solution-wide ATC/test success from partial coverage. For each object record syntax/activation/test/ATC state as `PASS`, `FINDINGS`, `NOT_REPORTED`, `NOT_SUPPORTED`, `NOT_RUN`, or `STALE`, with reason and alternative check. Name every `NOT_REPORTED`/`NOT_SUPPORTED` object in the summary.

## Repository and terminal-state gates
After uncertain create/activation, reconcile TADIR into `ABSENT`/`PARTIAL`/`GHOST`/`ACTIVE`/`INACTIVE`. `READY_FOR_UAT` requires zero unapproved ghost objects, no unexplained partial/inactive objects, and no unresolved `REWORK`. `READY_FOR_MANUAL_TEST` is allowed when an owner cleanup action is recorded and no further autonomous write is safe. A local package with no TR qualifies local development only — never deployment/transport readiness. An active but unpublished service stays `READY_FOR_MANUAL_TEST` when runtime evidence is required.

## Owner confirmation scope
Map a free-form owner statement to the named checks it closes (`confirmed_checks`) and list what it does not confirm (authorization-negative, full data reconciliation, performance, service runtime). Recalculate the terminal state from remaining criteria; general confirmation never overrides missing evidence.

## Post-run evidence and learning candidates
Before completion produce `docs/evidence/<run-id>/RUN_EVIDENCE.md` and `evidence-manifest.yaml` as the minimum package (delivery, verification, spec/decision, agent-performance layers). With no approved Spec, label Observed-Run Evidence and state that full specification conformance cannot be confirmed. Record learning candidates with observation, evidence, proposed destination, confidence, and `pending_human_review`; never auto-promote them into SKILL.md, agent, policy, or project memory.
