# Knowledge base

One file per **domain of competence**, one entry per **rule**. This is the durable
memory: `corrections.md` is only a buffer that drains into here.

The model and the reason for it: `docs/memory-model.md`.

## Domains

| File | Domain | Cap |
|---|---|---|
| `working-method.md` | how to do the work, tool-independent | 12 |
| `tooling.md` | which tool owns which job, tool-layer behaviour | 12 |
| `sap-gui.md` | driving the SAP GUI | 12 |
| `sap-abap.md` | ABAP and API contracts | 12 |
| `sap-data.md` | which table is the truth, what a quantity means | 12 |

A project card declares the domains it touches:

```yaml
domains: [sap-abap, sap-data]
```

so a task session loads only those files. Add a domain file only when a rule has no
home; do not create one per project.

A card with **no** `domains:` line — or one that names a file that does not exist —
makes the digest load every domain file. `memory_check.py` treats an unknown domain as
an issue for that reason: the scope has to be a name that resolves, not a good intention.

## What belongs here, and what belongs to a project

Knowledge is filed by **where the rule is used**, not by where it was learned. A project
name in `Evidence` is normal; a project name in the `Rule` means the entry is misfiled.

| The fact is… | It goes to | Test |
|---|---|---|
| a decision, exception, object name, field, or naming choice of one program | that program's `spec.md` (DEV/Q) or `reports/DECISIONS.md` | would another project be wrong to copy it? |
| true wherever the table or tool exists | `knowledge/<domain>.md` | can you state it without naming a custom object? |
| a repeatable procedure | a skill, with one line left here | does it need steps rather than a rule? |
| one incident, no generalisation | nowhere — drop it at close-out | what would the next agent do differently? |

No check catches a misfiled `Rule`. A keyword test only sees names that start with `Z`,
and a project field such as `MENGE_PD` passes it — so the review at close-out is the
gate. The test is the last column above: would another project be wrong to copy it?

## Entry template

```markdown
## <the rule, in one line, imperative>

- **Rule:** what to do, concrete and checkable
- **Why:** the mechanism that makes it true
- **Break it, and:** the symptom the next agent will see
- **Seen:** <n> · **Confidence:** low|medium|high · **Last confirmed:** YYYY-MM-DD
- **Evidence:** file, table, tool output, or project card section
```

`Evidence` may name a project, a program, or a custom object; the `Rule` may not.

## How an entry changes

| Situation | Action |
|---|---|
| The rule exists | edit that entry, `Seen +1`, raise confidence if it was verified again |
| The rule is new but general | add an entry, if the domain is under its cap |
| The rule is a one-off incident | do not add it — drop it at close-out |
| The rule is a multi-step procedure | promote to a skill, leave a one-line entry |
| A script can catch it | promote to a check, leave a one-line entry |

Never add a second entry for a rule that is already here. If two entries turn out to
be one rule, merge them: keep the wider `Rule`, the sharper `Break it, and`, and the
higher `Seen`.

## At the cap

The domain is full. Merge the entry with the lowest `Seen`, then the lowest
confidence, into a neighbour that covers it; if it covers nothing else, move it to
`memory/_archive/knowledge/` (git keeps it). A domain at its cap is a signal to
sharpen, not to grow.

## Confidence

| Level | Means |
|---|---|
| `low` | seen once, not verified — a hypothesis with a story |
| `medium` | seen once and verified in a table, test, or runtime result |
| `high` | seen more than once, or it cost a real failure |

`Seen` counts **confirmations**, not mentions: two rows about the same incident are
one confirmation.
