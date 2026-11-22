# Methodology resolution

Resolve the delivery profile before object design. Unknown is not allowed; if a field
below cannot be established from live evidence, stop and ask.

## Profiles

- **A — Classic Standard ABAP**: standard ABAP package; class-first classic objects; disclose Clean Core debt.
- **B — Cloud-ready Classic**: standard ABAP package, but prefer released APIs and migration seams.
- **C — RAP / ABAP Cloud**: ABAP for Cloud Development; released C1 or verified same-component dependencies.
- **D — Classic Bridge**: approved wrapper boundary only when a required released successor does not exist.

## Pre-write gate

Require product/edition, release, package, software component, effective language
version, permitted object types, dependency classification, Clean Core verdict,
Object Responsibility Plan, activation order, and verification plan.

- C2 remote availability is not automatically a system-internal ABAP API.
- A `Z*` name is not evidence of release state.
- Changing package or language version, or creating a bridge, needs an owner decision.
- Profile C requires `abap_for_cloud_development` — never infer it from a project name.

## Standard-first discovery (ordered)

1. Find the SAP standard application or built-in capability on the **target** system.
2. Verify release state and visibility there — public-cloud material is only a lead.
3. Approve the dependency, then decide reuse, adapter, reference-only, wrap, reject, or build new.

External repositories default to reference-only. Installation needs a separate
governance decision covering licence, security, compatibility, namespace, Clean Core,
object inventory, operational owner, and removal/upgrade.

## Fail conditions

No create while dependencies are unclassified, release state is assumed, or the
language version/package is unresolved. Record the selected profile and its evidence
in the run contract before the first write.
