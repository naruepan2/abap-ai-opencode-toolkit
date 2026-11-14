---
program: HCL_INTERFACE_QA32
project: DEMO
spec_version: 0.1
status: draft
fs_version: none
fs_date: "-"
fs_file: none
fs_original_name: "none - the scope is not confirmed yet"
scope: HCL interface scoped to QA32 - SICF node and handler, contract unknown
implemented_version: "-"
owner: Pongg
updated: 2026-11-14
---

# HCL_INTERFACE_QA32 - spec (draft)

There is **no FS** for this work yet. Everything below is what has been verified in
DS4 client 100, not an agreed requirement. Do not implement beyond it; the open
questions are the scope.

## 1. Purpose

HCL calls SAP; the endpoint under discussion is a SICF REST node. The interface name
"QA32" is not yet defined (transaction, client or interface).

| Item | Value |
|---|---|
| Actor | HCL (external system) |
| Trigger | HTTP call under `/sap/bc/rest/` |
| Target | DS4, client 100 (ADT), test client 900 (GUI), package `Z001` |

## 2. Scope

| In | Out |
|---|---|
| Node `/default_host/sap/bc/rest/HCLInterface` and its handler | Any other REST sibling (`4-WAYS`, `ASRS`, `SALESFORCE`, ...) |
| Verifying the node over HTTP and via `ICFSERVICE`/`ICFHANDLER`/`ICFSERVLOC`/`TADIR` | A payload contract or mapping - not specified yet |

## 3. Requirements

Status: `implemented` = built and verified; `pending-test` = built, test not recorded;
`pending` = not built; `out-of-scope`.

| ID | Requirement (one line, testable) | FS | Status | Since |
|---|---|---|---|---|
| REQ-01 | The node `/default_host/sap/bc/rest/HCLInterface` exists and is active, and an unauthenticated `GET` returns 401/403 (not 404) | none | implemented | 2026-11-13 |
| REQ-02 | The node has a handler on its Handler List (`ZCACL_REST_HTTP_HANDLER_HCL`, order 01, type A) and both objects are transportable in package `Z001` | none | implemented | 2026-11-13 |
| REQ-03 | The interface answers HCL with the response HCL expects, under the agreed authentication model | none | pending | - |
| REQ-04 | The node and class belong to the intended transport request, and the node is not exposed to upgrade overwrite | none | pending | - |

## 4. Acceptance criteria

| ID | Given / When / Then | REQ | Evidence |
|---|---|---|---|
| AC-01 | Given the node is active, when `GET /sap/bc/rest/HCLInterface` runs, then it returns 401, a bogus path returns 404, and `/sap/public/ping` returns 200 | REQ-01 | client 100, 2026-11-13 |
| AC-02 | Given the node exists, when `ICFSERVICE`, `ICFHANDLER`, `ICFSERVLOC` and `TADIR` are read, then the node is active with handler `ZCACL_REST_HTTP_HANDLER_HCL` in `Z001` | REQ-02 | client 100, 2026-11-13 |
| AC-03 | Given an agreed logon model, when HCL calls the node, then it receives the expected response instead of 401 | REQ-03 | Pending |
| AC-04 | Given the transport is confirmed, when the request is released, then the node and class are in the intended request | REQ-04 | Pending |

## 5. Deviations from the FS (approved)

None - there is no FS yet.

## 6. Open questions (do not guess)

| ID | Question | Impact | State |
|---|---|---|---|
| Q-01 | What exactly is "QA32" - a transaction, a client, or an interface name? | The whole design | open |
| Q-02 | Must HCL call without a logon (anonymous / ICF user), or with one? | The 401 is the current blocker | open |
| Q-03 | Is a dedicated handler class expected, or is the copied `ZCACL_*` prefix acceptable? | Naming and ownership | open |
| Q-04 | Is a node directly under `/sap` acceptable, or is an external alias required? | Upgrade safety | open |
| Q-05 | What does HCL send and expect back (method, payload, response)? | Cannot write REQ-03 without it | open |

## 7. Change log

| Spec | Date | Change |
|---|---|---|
| 0.1 | 2026-11-14 | Draft from verified facts in `README.md`; no FS exists |
