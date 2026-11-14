---
program: <PROGRAM>
project: <PROJECT>
spec_version: 1.0
status: draft                 # draft | approved | active | superseded
fs_version: <Vx.y>
fs_date: <YYYY-MM-DD>
fs_file: spec/source/<FS_FILE>.md
fs_original_name: "<name as received>"
scope: <the one thing this program is responsible for>
implemented_version: <vN or ->
owner: <name>
updated: <YYYY-MM-DD>
---

# <PROGRAM> - spec (<scope>)

The contract we build and test against.

| File | Answers |
|---|---|
| `spec.md` (this) | **What** must be true, and how we know it is done |
| `AGENTS.md` | **How we work** - constraints, deploy, scope of editable objects |
| `reports/DECISIONS.md` | **Why** a choice was made, with evidence |
| `templates/plan.md` | **In what order**, for a long run |

Rules:
- The FS under `spec/source/` is immutable. A new FS = a new file + a new
  `fs_version`; never edit the old one.
- One requirement per row, testable by a human in a client. If it cannot be
  tested, it is not a requirement - move it to Open questions.
- Reference the FS by line (`L1459`) or section, not by paraphrase alone.
- Change a requirement here **before** changing code.
- Keep this file under ~200 lines. Detail goes to `AGENTS.md` (rules),
  `DECISIONS.md` (why) and the memory card (session state).

## 1. Purpose

<Two or three lines: the business problem, the actor, the trigger.>

| Item | Value |
|---|---|
| Actor | <role, transaction> |
| Trigger | <what starts it> |
| Target | <system, code client, test client, transport> |

## 2. Scope

| In | Out |
|---|---|
| <what this program does> | <explicitly not this program - name the object that owns it> |

## 3. Requirements

Status: `implemented` = built and runtime-verified; `pending-test` = built, runtime
test not recorded; `pending` = not built; `out-of-scope`.

| ID | Requirement (one line, testable) | FS | Status | Since |
|---|---|---|---|---|
| REQ-01 | <what must be true> | L<n> | pending | - |

## 4. Acceptance criteria

Each AC is one run. `Pending` means no evidence yet - never report it as passed.

| ID | Given / When / Then | REQ | Evidence |
|---|---|---|---|
| AC-01 | Given <state>, when <action>, then <observable result> | REQ-01 | Pending |

## 5. Deviations from the FS (approved)

Empty is the normal state. Every row needs a decision reference and an approval date.

| ID | FS says | We do | Why / approval |
|---|---|---|---|
| DEV-01 | <FS text> | <actual behaviour> | D<n>, <date> |

## 6. Open questions (do not guess)

| ID | Question | Impact | State |
|---|---|---|---|
| Q-01 | <question the FS does not answer> | <what it blocks> | open |

## 7. Change log

| Spec | Date | Change |
|---|---|---|
| 1.0 | <YYYY-MM-DD> | First spec from FS <version> |
