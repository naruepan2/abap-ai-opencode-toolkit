---
name: auto-abap-delivery
description: explicit opt-in orchestration for bounded sap abap delivery from intake and approved specification through implementation, self-testing, atc, recovery, trust-calibrated attended or unattended interaction, evidence, and uat handoff. use only when the user explicitly invokes auto-abap-delivery, asks to start/resume an autonomous abap run, or supplies an existing run id. do not trigger for ordinary abap questions, code examples, reviews, explanations, or troubleshooting unless the user explicitly activates this mode.
---
# Auto ABAP Delivery

Operate as the control plane for a bounded SAP ABAP delivery run. Treat the user as Project Owner. Stop at `READY_FOR_UAT`; never infer approval for transport release/import, production write, productive job scheduling, mass correction, authorization change, or real external side effects.

A **run** is one approved delivery scope with its own `run_id`, ledger and evidence package,
created by `scripts/init_run.py` — not a session, a program or a single object change. One
session may hold several runs; one run may span several slices and objects inside the same
approved scope.

## Invocation and interaction defaults

Proceed only after explicit invocation, for example `/auto-abap-delivery start`, `start-unattended`, `start-attended --level guided`, or `resume RUN-...`.

After Spec, plan, and Autonomy Envelope approval, resolve interaction policy using [interaction-control.md](references/interaction-control.md):

- Initial default for unqualified scope: `execution_mode: attended`, `review_level: standard`.
- Qualified scope may default to `unattended`; critical scope requires at least `controlled`.
- Attended levels: `standard`, `guided`, `controlled`, `strict`, or `custom`.
- Unattended is preselected only for qualified scope. Unqualified scope preselects Attended Standard. SAP write requires explicit `APPROVE AND START`; a pre-approval recorded in a project or program `AGENTS.md` counts for the exact scope it states, so do not re-ask. Reconfirm if target, objects, package/transport, or operation changes.
- Use one delivery engine for both modes. Do not create a separate attended workflow.
- Keep Review Queue separate from Decision Inbox.

## Workflow

1. **Discover safely**: inspect the live MCP/tool surface and SAP target read-only. Never trust a remembered tool list. Load [capability-and-intake.md](references/capability-and-intake.md).
2. **Draft the assignment**: gather outcome, landscape, object/package/TR, scope, acceptance criteria, test permissions, and production boundary. Ask only what tools and SAP metadata cannot establish.
3. **Resolve architecture and guardrails**: determine ECC, S/4HANA, ABAP Cloud, Clean Core, released API, authorization, client, LUW, lock, performance, transport, and observability controls. Load [sap-guardrails.md](references/sap-guardrails.md).
4. **Resolve methodology**: select profile A Classic, B Cloud-ready Classic, C RAP/ABAP Cloud, or D approved Classic Bridge before any object design. Classify dependencies on the target system; unknown blocks write. Load [methodology-resolution.md](references/methodology-resolution.md).
5. **Assess trust and qualification**: load [trust-and-qualification.md](references/trust-and-qualification.md), classify unqualified/qualified/critical scope, and resolve the effective mode.
6. **Seek approval**: freeze Spec, implementation plan, test plan, execution contract, autonomy envelope, resolved interaction policy and `write mode` (`direct` | `comment-proposal`). Do not write SAP source before approval.
7. **Initialize the run**: execute `scripts/init_run.py` with approved identifiers and interaction fields; validate with `scripts/validate_run.py`.
8. **Plan the team and objects**: choose one-agent role passes, three roles, or five-to-seven specialist roles based on risk. Enforce one writer per production object. Freeze the Object Responsibility Plan; any later object-set change is an approval-required delta. For a new `PROG`, record the local/global class decision (`L1`/`L2`/`G`) from [prog-local-class-methodology.md](references/prog-local-class-methodology.md). Load [team-and-testing.md](references/team-and-testing.md).
9. **Apply engineering judgment**: before create/complete decisions, load [engineering-judgment.md](references/engineering-judgment.md) and require reuse, simplicity, test-adequacy, consumer-impact, project-memory, and reviewer-competency controls as applicable. Choose class-based logic first; use `FORM`/`PERFORM` only for a recorded exception; decide test-artifact placement before write.
10. **Execute by slice**: fresh-read, check preconditions, implement the minimum change inside an action contract, syntax-check, activate, read back source and object state, focused-test, repair from evidence, regress, ATC/CVA/readiness-check, audit, and checkpoint. Per-type postconditions are in [repository-reliability.md](references/repository-reliability.md).
11. **Apply interaction policy**:
    - unattended: continue silently within approved boundaries;
    - attended: create revisioned Review Queue items at configured checkpoints and enter `REVIEW_PENDING`;
    - never represent scheduled review as a technical blocker.
12. **Handle owner input**: validate Review Queue approval against source/spec/evidence snapshot; create Decision Inbox items only for human authority or judgment. Load [decision-inbox.md](references/decision-inbox.md).
13. **Switch modes safely**: apply a mode/level change only at a reconciled safe checkpoint through `RECONFIGURING`. Never stop midway through write or activation.
14. **Recover**: after restart or uncertain tool result, acquire a new fencing token, reconcile against SAP, invalidate stale evidence/reviews, and resume only from a legal state. After a failed/uncertain create or activation, classify TADIR/active state as `ABSENT`/`PARTIAL`/`GHOST`/`ACTIVE`/`INACTIVE` before any retry. Load [state-machine-and-recovery.md](references/state-machine-and-recovery.md).
15. **Complete**: require fresh source-linked evidence, no outstanding `REWORK` or required review, guardrail report, UAT mapping, and unreleased transport. Emit post-run evidence with a per-object verification matrix, scoped owner confirmation, disclosed local-package lifecycle, and learning candidates for human review. Build handoff using [evidence-and-uat.md](references/evidence-and-uat.md) and [accountability.md](references/accountability.md).

## Read and plan discipline

Load only the reference needed for the current step — do not preload all references.
Before execution, a plan must state read-only preconditions, the thinnest end-to-end
slice that touches every layer changed, and a BLOCKER-quality review of its dimensions.
Bounded revision is allowed; unresolved blockers go to the owner, never to auto-approval.
A `one-way` change inserts a decision gate before its dependent step.

## Fast path for small changes

A one-to-three-step local change with no new SAP object, no multi-slice plan and no need
for durable run state does not need a full run. Route it to `senior-abap-development`
(or the default coding agent for toolkit/non-SAP work) instead of initializing a run.
Keep the core gates: confirmed target, fresh read, a recorded reason if `FORM`/`PERFORM`
is used, read-back after write, and no transport release or production action. The fast
path skips the run ledger and evidence package **only** — the change contract (intent,
target, approval) still applies. An SAP object change also needs the program `spec.md`;
a toolkit or local-file change does not.

## Hard gates

1. **SAP reality wins.** Re-read source/hash/lock/TR before a write; read back after. Never overwrite drift or replay an uncertain side effect.
2. **No irreversible authority.** No transport release/import, production write, mass change, or real external effect — even in `strict` review.
3. **No fabricated success.** Unavailable validation is `READY_FOR_MANUAL_TEST`/`INCONCLUSIVE`, never PASS. No solution-wide claim from partial coverage; owner confirmation closes only named checks.
4. **Clean terminal state.** No unapproved ghost object at `READY_FOR_UAT`; unpublished service stays `READY_FOR_MANUAL_TEST` when runtime evidence is required.
5. **Human gates stay human.** Decision Inbox items are never batch-approved; an attended review timeout never auto-continues.
6. **Class-based first.** `FORM`/`PERFORM` only as a recorded fallback; no permanent test-driver `PROG`; unit tests value-based.

The full rule list with rationale lives in [non-negotiable-rules.md](references/non-negotiable-rules.md).
Read it before touching review cadence, test strategy, ATC disposals, decision batching or terminal state.

## Legal final states

Use only `READY_FOR_UAT`, `READY_FOR_MANUAL_TEST`, `BLOCKED_OWNER_DECISION`, `BLOCKED_TOOLING`, `PAUSED_SAFE`, `FAILED_SAFE`, or `CANCELLED`. Do not use `DONE` before UAT and a separate production workflow.

## Mandatory completion gates

Require reuse assessment for new global objects, simplicity verdict, independent test-adequacy audit, consumer-impact report when applicable, reviewed project-engineering-profile revision, qualified reviewer routing, accountability matrix, and updated autonomy qualification record.
