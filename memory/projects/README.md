# Project memory

One file per project. Keep it short and current.

Mirror the SAP project layout:

```
memory/projects/<project>/<program>.md
```

Example: `memory/projects/DEMO/zmme011.md` for
`<portfolio>\SAP Projects\Projects\DEMO\ZDEMO01`.

## Template

```markdown
# <project>

## Resume card
- Status:
- Next step:
- Do not:
- FS:                     # path or "none — proposed <date>"
- Change type:            # bugfix | extend | change request
- Production:             # not live | live (dev in sync?) | unknown
- Target:                 # system, client, transport
- Approved scope:         # what may be written / activated / transported, and by whom
- Stop condition:         # the acceptance test that ends the work
- Plan:                   # plan-<task>.md for a long task, or "none"

## Goal

## Constraints

## Environment

## Business rules

## Code map

## Decisions

## Known unknowns

## Evidence
```

## Rules

- Update the resume card at the end of every session.
- Move durable, cross-project rules to `../knowledge/<domain>.md` (one entry per rule,
  edit in place). Repeated patterns go to `../skill-candidates.md`.
- No credentials, no customer data.
