# CDS and RAP design checkpoints

Design detail for step 3 of `SKILL.md`, when the chosen model is a CDS-backed view
or a RAP business object. Read it after the model is chosen, not as a survey of
options.

For CDS-backed designs, decide what the model is for before choosing artifacts:
reusable domain/data model, service-specific projection, or analytical/read-only
consumption. Keep service-specific exposure separate from reusable data modeling
when that separation benefits multiple consumers. Verify CDS entity type and
features against the target release; do not assume current cloud syntax is
available in a classic system. Model associations and compositions from actual
business ownership and data cardinality, and ensure amount/quantity semantics,
authorization behavior, and null/outer-join behavior are intentional.

For RAP business objects, model and verify the full stack: persistence, root and
child entities/relationships, BDEF, behavior implementation where needed,
projection when a service needs a restricted/adapted interface, then service
definition and binding. Prefer managed behavior when the framework can correctly
own persistence and standard operations. Choose unmanaged behavior only when
verified existing processing or persistence requirements justify owning that
implementation; consider managed extensions/additional save before replacing
the managed save path. Make draft, numbering, locking/ETag, authorization, feature
control, validations/determinations, and service protocol explicit design choices
rather than defaults to copy blindly.

Treat the RAP transactional buffer and save sequence as the transaction boundary:
behavior code should follow the RAP BO contract, return appropriate `failed`,
`reported`, and (where applicable) `mapped` responses, and avoid direct database
updates or transaction commits that bypass the BO lifecycle. Verify the exact
contract and phase restrictions for the target release before implementing
unmanaged or save-phase logic.

Before calling a classic API from inside a RAP business object, apply the
admission test: in the ABAP Cloud context a classic API may be used from a RAP
application only when it carries the `transactional-consistent` label in the
Cloudification Repository. An unlabelled classic API can break RAP's
transactional model even when it compiles and its ATC check passes, so a clean
ATC result is not evidence that the call is allowed. Verify the label in the
system rather than assuming it, and when it is missing treat the call as a
design change to be raised with the user, not as a coding detail.

For deeper implementation detail, use `sap-abap-cds` for CDS and DCL, and the
RAP service/logic Skills listed in `SKILL.md`. Authoritative references: [SAP ABAP Data
Models](https://help.sap.com/docs/abap-cloud/abap-data-models/abap-data-models),
[SAP RAP Developer Guide](https://help.sap.com/docs/abap-cloud/abap-rap/abap-restful-application-programming-model),
[RAP Development Constraints](https://help.sap.com/docs/abap-cloud/abap-rap/development-constraints),
and the [ABAP CDS Keyword Documentation](https://help.sap.com/docs/abap-cloud/abap-keyword/abap-core-data-services-abap-cds).
Use [SAP's ABAP Cheat Sheets](https://github.com/SAP-samples/abap-cheat-sheets)
for concise syntax examples only; check language version and release, since
examples are simplified and are not production design templates.
