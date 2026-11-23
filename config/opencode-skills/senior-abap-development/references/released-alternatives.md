# Released alternatives and cloud restrictions

Use this as a lookup, not as an unconditional rewrite rule. Verify the target release,
language version and the actual object's release state before applying any row.

`DOC_EVIDENCE` pre-check: `sap_get_object_details` and `abap_feature_matrix` from
`sap-abap-docs` can confirm released state and release availability before the target check;
they report public-cloud metadata, so never treat that as on-prem evidence.

## Common replacements

| Classic construct |Preferred released alternative | Scope note |
|---|---|---|
| `AUTHORITY-CHECK` | `CL_ABAP_AUTHORIZATION` | ABAP Cloud / cloud development. Classic ABAP keeps `AUTHORITY-CHECK`; never state the cloud rule unqualified. |
| `sy-uname` | `CL_ABAP_CONTEXT_INFO` | Where available in the target release. |
| `GUID_CREATE` | `CL_SYSTEM_UUID` | Released UUID creation. |
| `NUMBER_GET_NEXT` | `CL_NUMBERRANGE_RUNTIME` | Check number-range object support. |
| Direct `SELECT` on an SAP table | released `I_*` CDS view | Verify the view exists and is released on the target system; public-cloud availability is not on-prem evidence. |
| `CALL TRANSACTION` / `SUBMIT` | released API, RAP action or OData service | ABAP Cloud restriction. |
| `WRITE` / classic list output | SALV, RAP UI or released output service | ABAP Cloud restriction. |
| `EXEC SQL` / native SQL | released ABAP SQL / CDS / AMDP with client handling | ABAP Cloud restriction. |

## ABAP Cloud restriction checklist

In ABAP Cloud (not classic ABAP): no direct SAP table access, no classic dynpro or
selection screens, no `CALL TRANSACTION`/`SUBMIT`, no classic `AUTHORITY-CHECK` (use
`CL_ABAP_AUTHORIZATION`), no classic BAdIs or user exits, no `EXEC SQL`, no `INCLUDE`,
no `WRITE`. Use `IF_OO_ADT_CLASSRUN` for console output in development.

For Clean Core, classify by the **lowest level used inside the extension** and never
call a mixed usage clean. Wrap classic APIs deliberately; a `noAPI` object must not be
wrapped. An ATC pass is not evidence that a classic API is admissible inside RAP — the
`transactional-consistent` label in the Cloudification Repository is required there.

Source patterns: `abap-skills-main` released-API and cloud references; verify against
SAP Help and the connected system before relying on them.
