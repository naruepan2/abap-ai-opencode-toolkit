# Non-negotiable rules — full list

The control plane keeps six hard gates in `SKILL.md`. This file holds the full list so
the detail is not lost when the main prompt stays short. Read it before a decision that
touches review cadence, test strategy, ATC disposals, decision batching or terminal state.

## Authority and writes

- SAP reality is authority for source, activation, locks, transport, SID/client; durable artifacts are authority for approved scope and policy.
- Persist command intent before a side effect and reconcile the observed result afterward.
- Never blindly replay source write, activation, test-data creation, RFC/IDoc/API send, posting, commit, or mass update.
- Never overwrite source drift. Pause affected work, stale evidence/reviews, and decide safely.
- Production and irreversible actions remain prohibited even in `strict` review.

## Verification honesty

- Never weaken expected results to make tests pass.
- Never suppress ATC/CVA findings without ID, rationale, owner, and expiry where applicable.
- Mark unavailable validation `READY_FOR_MANUAL_TEST` or `INCONCLUSIVE`; never fabricate success.
- Never claim solution-wide ATC/test success from partial object coverage; disclose `NOT_REPORTED` and `NOT_SUPPORTED` per object.
- A free-form owner confirmation closes only the named checks it addresses; never use it to override missing evidence.

## Interaction and terminal state

- Attended review timeout never auto-continues. Transition to `PAUSED_SAFE` when the lease expires.
- Decision Inbox items cannot be batch-approved. Batch Review Queue approvals only when reversible, same slice/snapshot, and policy-eligible.
- No unapproved ghost object at `READY_FOR_UAT`; an unpublished service stays `READY_FOR_MANUAL_TEST` when runtime evidence is required.

## ABAP design

- New development is class-based first. `FORM`/`PERFORM` is a documented fallback, never the default — see [engineering-judgment.md](engineering-judgment.md) and [prog-local-class-methodology.md](prog-local-class-methodology.md). Reports and function modules stay thin class-based shells/boundaries otherwise.
- No permanent test-driver `PROG` to compensate for a missing AUnit runner. A diagnostic driver result is `DIAGNOSTIC_DRIVER`, never `ABAP_UNIT`.

Each rule has one home. Do not duplicate it into another skill or AGENTS file; point
at this reference instead.
