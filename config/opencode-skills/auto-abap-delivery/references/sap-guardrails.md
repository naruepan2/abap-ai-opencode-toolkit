# SAP-native guardrails

Resolve rules by ECC, S/4HANA on-prem/private/public, BTP ABAP, Standard ABAP, or ABAP Cloud.

For every slice classify: language/API compatibility; security/input trust; authorization; client isolation; SAP LUW/update consistency; locking/concurrency; database/performance; exception/cleanup; testability/observability; transport/lifecycle; migration/Clean Core; privacy/external effects.

Mandatory controls:
- Prefer standard/configuration and released APIs/extension points. Record release contract, deprecation, successor, and migration debt.
- Reject unallowlisted dynamic SQL/calls/identifiers, direct physical paths, credential logging, and uncontrolled outbound calls.
- Test allowed/denied authorization. Never ignore `AUTHORITY-CHECK` result.
- Treat cross-client access, Native SQL/ADBC/AMDP client handling, schema/index changes, and authorization changes as high risk.
- Reusable classes/BAdIs/FMs must not own `COMMIT WORK` unless their contract explicitly requires it. Respect RAP transactional buffer/save sequence.
- Define enqueue/ETag strategy before read-modify-write. Test foreign lock, stale ETag, and duplicate submission where relevant.
- Avoid SQL in loops, unbounded reads, needless columns, and unsupported performance guesses. Require SAT/ST05/SQL Monitor evidence for triggered high-volume changes.
- Discover organization ATC/CVA/readiness variants live. New priority 1/2 findings fail by default.
- Check TADIR, package, original system, namespace, transport/task, lock, inactive version, and source hash before write.
- Keep transport release/import, production write, mass update/delete, real external effects, and productive job scheduling outside the autonomous envelope.

## Clean Core and RAP guardrails

- A clean ATC result does **not** authorize a classic API call inside a RAP application. Such a call is admissible only when the Cloudification Repository marks the API `transactional-consistent`; verify the label in the system. An unlabelled classic API is a design decision for the owner, not a coding detail.
- Classify an extension by the **lowest Clean Core Level** used within it (this is a Clean Core Level, not the methodology profile): Level A released/stable, B wrapper/adapter, C internal/unreleased, D modification or `noAPI` debt. A Level D finding must be remediated or escalated immediately; never call a mixed usage "clean".
- Wrapping a classic API creates a Level B wrapper; an internal object is Level C; a `noAPI` object is Level D — do not build a wrapper for it. A wrapper can collapse several ATC findings into one exemption. Do not copy non-released data types into the wrapper: expose `TYPES` and provide `SU22` data/variants. Retire the wrapper if SAP releases a successor.
- Exempt only priority 1/2 findings, with ID, rationale, owner and expiry. Never exempt priority 3 classic-API findings. Use an ATC baseline only for legacy code that will not be changed. Prefer wrap → one exemption over many suppressions.
