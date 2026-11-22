---
name: senior-abap-development
description: Plan and develop SAP ABAP programs from requirements through verification, for classic ABAP and modern ABAP Cloud, Clean Core and RAP. Use for new or changed reports, SALV/ALV, classes, function modules, enhancements, CDS and RAP objects, or when choosing between classic and modern designs. For a multi-slice delivery run with durable state and UAT handoff use auto-abap-delivery instead.
---
# Senior ABAP Development

A practical development workflow for one object or one bounded change. Select the
simplest model that fits the requirement and the target system; modernization is
neither a reason to reject a valid classic solution nor a licence for legacy patterns
in new code.

## 1. Establish the request and the target

Identify new program, change to an existing object, explanation/review, or runtime
issue. For development establish expected behavior, inputs, outputs, authorization,
error handling, data volume, execution context (dialog/background/API), and acceptance
checks. Ask only for requirements that change the design; separate user requirements
from assumptions and unresolved decisions.

For any SAP-connected operation, including reads, use the exact system and client the
user explicitly confirmed in this session. Reuse that confirmation for later work on
the same target; ask again only when it is missing, ambiguous, or changes. Workspace
roots, editor state, previous sessions, defaults, connection lists, and tool output do
not confirm a target. Offline review of supplied source needs no target.

Before create/edit/delete/activate or a live-data change, present one Pre-Flight:
confirmed system/client, operation, exact object scope, package/transport,
dependencies, validation plan, and risks. Wait for explicit approval; approval covers
only that scope. Reconfirm if any of those fields changes.

## 2. Inspect before designing

For existing code read the target, its callers and dependencies first. Verify object
names, signatures, data elements, DDIC fields, released-API state and release
availability against the connected system, not memory. Prefer reuse of a suitable
standard or custom capability or supported extension point when evidence shows it
fits. Keep SAP standard source unmodified.

Determine the actual release and effective ABAP language version before selecting
syntax or APIs. In multi-root or ADT virtual workspaces use SAP-aware tools for live
objects; do not treat virtual object paths as local files.

## 3. Choose the right ABAP model

- **Classic report** — requested SE38/SA38 reports, batch tasks, operational lists, classic systems/packages. Selection screen, ABAP SQL, presentation suited to the need.
- **SALV** — prefer `CL_SALV_TABLE` for read-only tabular display when its functions suffice. **ALV Grid** only when editing/interaction justifies it; verify release support and keep data selection/processing separate from presentation.
- **Classes and function modules** — classes own cohesive OO logic and testable services. Use or create FMs for existing integration contracts, RFC/update-task behavior, function groups, or a stated user need; verify signature and processing type.
- **Enhancements** — prefer released BAdIs, enhancement spots, explicit extension points. Implicit enhancements only when no supported point exists, with the exact location, upgrade risk and ownership verified.
- **Clean Core / ABAP Cloud** — use released APIs and the supported extension model. Check language version, API state and ATC evidence. State explicitly when a classic requirement conflicts with cloud restrictions.
- **CDS and RAP** — for transactional business objects and service-backed applications when they fit the requirement and release. Design persistence, CDS model, behavior, authorization, service exposure and tests as one stack. Do not introduce RAP merely to modernize a standalone report.

Class-based methods are the first choice for new logic. `FORM`/`PERFORM` is a
documented fallback, not a default: use it when maintaining existing procedural code,
when the target convention or a framework requires a subroutine-style routine, when
the live toolchain cannot create a class-based include, or when a proven
compatibility/performance constraint leaves no equivalent. Record the reason with the
object. Do not launch an unrelated refactor.

Clean Core Level is the **lowest level used inside the extension** (A released/stable,
B wrapper/adapter, C internal/unreleased, D modification or `noAPI` debt). Level D
must be remediated or escalated immediately; a mixed usage is never simply "clean".

For concrete released replacements (`CL_ABAP_AUTHORIZATION`, `cl_abap_context_info`,
`cl_system_uuid`, `cl_numberrange_runtime`, `I_*` CDS views, and classic statement
alternatives), read [references/released-alternatives.md](references/released-alternatives.md).

### CDS and RAP design checkpoints
Read [references/cds-rap-design-checkpoints.md](references/cds-rap-design-checkpoints.md)
after the model is chosen, not as a survey of options.

### Requirement checks by program type
Read [references/requirement-checks-by-program-type.md](references/requirement-checks-by-program-type.md)
when writing the plan or Pre-Flight scope.

Explain material trade-offs briefly. Ask for confirmation only for an unresolved
decision that changes scope, behavior, or deployment model.

## 4. Design and implement incrementally

Define object responsibilities, data flow, error behavior, authorization checks,
transaction boundaries and test strategy before writing code. Keep the change narrow
and compatible unless refactoring is explicitly in scope. Verify every referenced
object, field, API and signature before use. For existing objects treat observed
behavior, callers and public contracts as the regression baseline; prefer method-level
edits over replacing a whole object; inspect the diff and preserve unrelated edits.

For a material behavior change identify the highest useful test seam before coding and
say what it catches and misses. Prefer a focused failing regression test before the fix
when the environment supports it; work one behavior slice at a time. If the tooling
cannot provide a meaningful red test, use the strongest available syntax, unit,
integration or controlled manual check and disclose the gap. Tests verify observable
behavior, not private implementation details.

When ABAP Unit is selected use `ltc_`/`ltd_` prefixes, `RISK LEVEL` and
`DURATION SHORT/MEDIUM/LONG`, `FOR TESTING ... RAISING cx_static_check`; create the
environment in `class_setup`, clear doubles in `setup`, destroy in `class_teardown`.
Prefer constructor injection; `TEST-SEAM` is a legacy bridge. Unit tests remain
optional and value-based.

Load only the guidance the task needs (availability varies by host; disclose gaps):
`sap-abap` (language/SQL/OO/EML/DDIC/ABAP Unit), `sap-abap-cds`, `sap-clean-core-atc`,
`generate-rap-service` or `generate-rap-service-researched`, `generate-rap-logic`,
`generate-abap-unit-test`, `sap-se38-report-tester`, `sap-abap-reverse-engineering`,
`explain-abap-code`, `ponytail` and `ponytail-review`. For performance, verify the
target database first, then use `debug-slow-sql`. For a multi-slice run hand off to
`auto-abap-delivery`.

## 5. Validate the result

For local source use an available linter. Look for a project-local `node_modules/.bin/abaplint`
first, then an existing command; if absent, ask before installing. Prefer a local dev
dependency, never download silently, and do not alter `abaplint.json` without approval.
Preserve the configured syntax version and rule IDs.

For live objects read back the saved source/state, run syntax checks, then activate in
dependency order only after approval. Run ABAP Unit or the requested report/UI/integration
test when available; run ATC when relevant. Activation is not proof of behavioral
correctness. Record unavailable or unrun checks as `UNVERIFIED`, not passes. On failure
capture the exact diagnostic, inspect object state before retrying, and never replay a
write blindly.

Severity of findings follows impact: **Critical** = incorrect results, data loss,
security or production failure; **Major** = confirmed defect or substantial
performance/reliability risk; **Minor** = localized style. A preference such as method
length, naming or string-literal style is not Critical. Keep the linter's own rule ID
and severity separate from this manual severity.

## 6. Report

Summarize the chosen design and why it fits the classic/modern model. For live changes
identify system/client, changed objects, active/inactive state, package/transport,
validation performed, results, and remaining risks. Separate observed system evidence
from assumptions, and never claim an unrun check or unverified behavior as successful.
