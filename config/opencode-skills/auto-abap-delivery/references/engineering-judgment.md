# Engineering judgment controls

## Reuse-first discovery
Before a global object is created, search SAP standard/configuration, released APIs/extension points, approved project components, similar objects, and architecture decisions. Produce a reuse assessment and choose reuse, extend, retire, or build. Existing code is not proof of quality. For released APIs and extension points, query `sap-abap-docs` before general internet search; record tool, query and source URL as `DOC_EVIDENCE`, then re-verify on the target.

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
- Methods and classes are the **first choice** for new logic. `FORM`/`PERFORM` is allowed only with a recorded reason: the object is existing legacy procedural code outside the approved refactor scope; a framework or interface requires a subroutine-style routine; the live toolchain cannot create or activate a class-based include for that object; or a proven compatibility/performance constraint leaves no class-based equivalent. Record the exception (object + reason) in the decision trail. Legacy subroutines otherwise stay unchanged or are extracted by approved risk/scope.
- A new `PROG` is class-based but is **not** forced into global classes. Choose the recorded shape: `L1` cohesive local classes for report-only behavior, `L2` local report classes plus a justified global owner for shared logic, or `G` thin shell plus global classes for multiple consumers, stable API, lifecycle, security boundary, or test ownership. `FUNC`/`FUGR` remain thin interface and exception-mapping boundaries. See [prog-local-class-methodology.md](prog-local-class-methodology.md).
- Fail/rework when a report or FM owns material logic without justification, responsibilities overlap, or a permanent test-driver `PROG` is proposed to hide a tooling gap.
- Decide test-artifact placement before write: class test include for justified global classes; program test include when tooling is verified; inline local test class only for a small prototype with a disclosed reason. Never delete tests merely to make production source look cleaner.
- Identify the actual field and type with evidence before any cast or length change. An unproven type change is `empirical`, never a proven root cause.

## Object Responsibility Plan and object-set delta
Before write, freeze each object's role (`thin_shell`, `application_logic`, `data_access`, `framework_mandated`, `temporary_artifact`) and verification. Replace rigid object-count limits: classify any later addition/removal as a delta with reason, architecture impact, and owner approval when material. Label each object framework-mandated, standard reusable, Agent-proposed, temporary diagnostic, or prohibited workaround.
