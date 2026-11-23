# Plan: <task>

> Copy this file to the program folder as `plan-<task>.md` and get it approved once.
> After that it is the **checkpoint**, not a contract: tick todos with evidence and
> revise it when reality disagrees.
>
> Four rules:
> 1. One todo = one verifiable unit (~15–45 min, at most one artifact). "Read the FS"
>    is not a todo; "confirm all 12 FS rules map to a method" is.
> 2. Approve the plan once. Only leaving the approved scope needs another approval.
> 3. The plan is a hypothesis. When a todo proves it wrong, revise — do not push
>    through.
> 4. ≤12 todos. More means it is not decomposed yet: split into phases, one plan each.

Goal:        <the single measurable outcome>
Acceptance:  <what is tested, and when it counts as done>   ← = stop condition

Contract:
- FS:          <path / "none — proposed <date>">
- Spec:        <program folder>/spec.md — REQ ids in scope: <REQ-01, REQ-02>
- ADT path:    <ai-dev | arc1> — writer: <ns>, verify: <ns>, analyse: <ns>
- Change type: <bugfix | extend | change request>
- Production:  <not live | live (dev in sync?) | unknown>
- Target:      <system, client, transport>
- Preconditions: <read-only assertions checked before any write; halt with no partial write if unmet>
- Reversibility: <reversible | one-way> — one-way adds a decision gate before its dependent step
- First slice:  <thinnest end-to-end path touching every layer this change modifies>

Approved:
- Write:      <objects that may change — type/name/locator/layer/hash engine/CAS>
- Activate:   <yes | no> — `activate_multiple` per activation unit, never one blind batch
- Units:      <U1 <layer>: objects ...; U2 <layer>: objects ...> — bottom-up order
- Transport:  <TR or none>
- By:         <user + date>

## Todo

- [ ] 1. <verifiable unit> — ~30 min — owner: lead
- [ ] 2. <verifiable unit> — read-only → child (`explore`) — evidence: <what to return>
- [ ] 3. <verifiable unit> — owner: child (`abap-developer`) — brief: contract + scope above

Status legend: `[ ]` todo · `[x]` done (with evidence) · `[~]` blocked (with the question)

## Log

> One line per tick: what was verified, and the evidence. This is what survives a
> context reset.

- <date> 1. <what> — evidence: <file / table read / test output>
- <date> 2. BLOCKED: <the one question a human must answer>
