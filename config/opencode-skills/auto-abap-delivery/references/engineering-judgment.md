# Engineering judgment controls

## Reuse-first discovery
Before a global object is created, search SAP standard/configuration, released APIs/extension points, approved project components, similar objects, and architecture decisions. Produce a reuse assessment and choose reuse, extend, retire, or build. Existing code is not proof of quality.

## Simplicity gate
Justify each new global object/public interface/wrapper/layer. Prefer the smallest maintainable solution. Flag speculative reuse, pass-through wrappers, duplicated patterns, unjustified classes, and excess public surface.

## Test adequacy
Independent auditor challenges scenario coverage, negative/exception/authorization/alternative/boundary/concurrency/regression cases, test-double fidelity, assertion strength, and manual-UAT gaps. Passing tests alone do not pass this gate.

## Consumer impact
For CDS/RAP/OData/RFC/BAPI/IDoc/DDIC/public interfaces/forms/events, enumerate consumers, contract deltas, semantic compatibility, regression tests, versioning and rollout.

## Project engineering memory
Load reviewed style, naming, approved patterns/components, testing, Clean Core, released API and forbidden-pattern files. AI creates lesson candidates only; human review promotes them.

## Reviewer competency
Route checkpoints to qualified roles. Architecture/Clean Core needs senior ABAP or architect; authorization needs Security plus owner; scenarios need functional owner/test engineer; source diff needs ABAP reviewer; contracts need integration owner.

## Class-First Gate (before any new PROG/FUGR/FUNC write)
- New `FORM`/`PERFORM` and external `PERFORM` are prohibited. New business logic lives in methods/classes; legacy subroutines stay unchanged or are extracted only by approved risk/scope.
- A new report is a thin selection/event shell: no material calculations, data aggregation, authorization orchestration, or reusable validation. `FUNC`/`FUGR` are thin interface and exception-mapping boundaries. Global classes own rules, orchestration, and testable data-access seams.
- Fail/rework when a report or FM owns material logic without justification, responsibilities overlap, or a permanent test-driver `PROG` is proposed to hide a tooling gap.
- Decide test-artifact placement before write: class test include for justified global classes; program test include when tooling is verified; inline local test class only for a small prototype with a disclosed reason. Never delete tests merely to make production source look cleaner.

## Object Responsibility Plan and object-set delta
Before write, freeze each object's role (`thin_shell`, `application_logic`, `data_access`, `framework_mandated`, `temporary_artifact`) and verification. Replace rigid object-count limits: classify any later addition/removal as a delta with reason, architecture impact, and owner approval when material. Label each object framework-mandated, standard reusable, Agent-proposed, temporary diagnostic, or prohibited workaround.
