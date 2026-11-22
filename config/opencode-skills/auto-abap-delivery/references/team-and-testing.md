# Dynamic team and self-testing

## Team selection
- Risk 0-24: one coordinator using separate Developer, Tester, and Reviewer passes.
- Risk 25-54: Delivery Lead/Developer, Test Engineer, Independent Auditor.
- Risk 55-100: add Requirement Analyst, SAP/Clean Core Architect, Integration/Performance specialist, and developers by independent workstream, maximum seven active roles.
- One production object has exactly one writer. Auditor is read-only. Tester cannot weaken expected results.

## Engineering loop
`Understand -> design tests -> characterize/reproduce -> implement minimum change -> syntax/activate -> focused tests -> repair -> regression -> ATC -> audit -> evidence -> checkpoint`.

Generate scenarios from acceptance criteria, invariants, object failure modes, dependencies, historical regression, malformed/boundary inputs. Include relevant empty, duplicate, missing master, invalid status, authorization, lock, partial success, currency/unit, date/time, precision/overflow, retry/idempotency, timeout, volume, commit/rollback, and legacy behavior cases.

Select ABAP OO, SQL, CDS, Function Module, AMDP, or RAP test doubles by dependency and release capability. Use deterministic fixtures; no productive mutation or real outbound call. An activation is not proof of correctness.

Repair at most three times per slice by default. If the same error signature repeats twice without a new hypothesis, stop and escalate.

## Optional, value-based unit tests
Unit tests are not a universal gate. `CLAS` with material logic gets them when value justifies cost (calculation, quantity/date/unit logic, regression-prone fix, boundary-heavy validation, reusable service). `PROG`/`FUNC`/`FUGR` shells do not require them; verify those boundaries with selection validation, foreground/background smoke, controlled execution, output cross-check, and ATC. Never infer "tests impossible" from the object type — check live runner/test-include capability and record `NOT_APPLICABLE` with compensating evidence when omitted.

When ABAP Unit is selected: use `ltc_`/`ltd_` prefixes, `RISK LEVEL` and `DURATION SHORT/MEDIUM/LONG`, and `FOR TESTING ... RAISING cx_static_check`; create the test environment in `class_setup`, clear doubles in `setup`, and destroy it in `class_teardown`. Prefer constructor injection; use `TEST-SEAM` only as a legacy bridge. These mechanics never override the value-based gate.

## Test result taxonomy
Classify every executed check as `ABAP_UNIT`, `SMOKE`, `INTEGRATION`, `SERVICE_RUNTIME`, `STATIC_REVIEW`, `MANUAL_OWNER_CONFIRMED`, or `DIAGNOSTIC_DRIVER`. A temporary diagnostic driver needs owner approval, a local/non-transportable package, cleanup, and must never be reported as ABAP Unit. Completion uses verification sufficiency (class-based design, required per-object checks, selected tests pass, boundary evidence complete, gaps mapped to UAT), not a fixed unit-test count.
