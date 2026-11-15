# Knowledge: working method

> One entry per rule; edit in place and raise `Seen`. Keep the mechanism and the
> symptom, not a narrative. Split a domain file when it passes its cap.

## Read the contract before changing code

- **Rule:** read the program `spec.md` (requirements, acceptance criteria, open
  questions) before the first edit. No spec means the first task is a spec.
- **Why:** the requirement is signed off once; guessing it again in code is how a
  correct patch becomes a wrong one.
- **Break it, and:** the change is technically clean and functionally unwanted.
- **Seen:** 1 · **Confidence:** high · **Last confirmed:** (date)
- **Evidence:** (one line: what showed this)

## One row per incident, consolidated at close-out

- **Rule:** capture a correction the moment it happens, then merge it into this
  domain file at close-out and mark the row `drained`.
- **Why:** a session can end mid-task; a log that grows forever is never read.
- **Break it, and:** the same mistake returns next week, or the inbox becomes a diary.
- **Seen:** 1 · **Confidence:** high · **Last confirmed:** (date)
- **Evidence:** (one line)
