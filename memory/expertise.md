# Expertise: the end state, and how we prove it

> The junior→senior ladder in `docs/memory-model.md` is only the framing. The goal is
> the end state: **the AI does the right thing without being told and without looking
> it up.** This file defines that state, measures it, and lists the probes that prove
> it.

## Definition of done

A rule has become **expertise** when all three are true:

1. **Unprompted** — nobody mentions the rule, and the right behaviour still happens.
2. **Unlooked-up** — it does not depend on reading `knowledge/` in that session.
3. **Testable** — a probe (below) can fail it. If nothing can fail it, it is a note,
   not a competence.

A rule that needs to be read is a *handbook*. A rule that cannot be forgotten is
*expertise*. The distance between the two is the only thing this file tracks.

## Three levels, and what moves a rule up

| Level | What it means | Where it lives | Count (2026-11-14) |
|---|---|---|---|
| **Reflex** | printed into every session; no lookup | digest `TOOL RULES` / `STYLE` | 6 |
| **Enforced** | a machine fails when it is broken | `AGENTS.md`, a check, a skill | 3 |
| **Handbook** | correct only if the file is read | `memory/knowledge/<domain>.md` | 15 |

The promotion path, cheapest first:

```
knowledge entry → digest line (reflex, +1 line of prompt)
                → AGENTS.md rule (reflex, project-scoped)
                → skill (a procedure it executes)
                → check in memory_check / registry_check (cannot be broken silently)
```

**Do not promote everything.** The digest has ~7 lines of budget; a rule earns a slot
only if getting it wrong is expensive and it recurs. Everything else stays handbook —
that is fine, as long as the failure is cheap and the probe catches it.

## What "reflex" looks like today

Six rules are already in every session (the digest `TOOL RULES` block):

| Rule | Failure prevented |
|---|---|
| ADT for source/DDIC; a dump mangles Thai | mojibake deploy |
| Client 100 → ADT, 900 → SE16; SE16N blocked | failed reads, wasted calls |
| S/4: `MATDOC`, not `MKPF` + `MSEG` | legacy table in new code |
| Custom GUI button needs OS focus | silent no-op, false success |
| `policy.json` is read once; never kill an MCP | tool namespace loss mid-task |
| SAP is on-demand | credential dialog at startup |

Three are enforced by code: the inbox row budget, the knowledge schema (fields,
confidence, caps) and the registry prompt budget.

The other 15 are handbook. That is the honest gap.

## Probes (run cold, in a fresh session, without naming the rule)

Each probe fails or passes on the *first* action, not on the final answer. Pass =
expertise; fail = the rule is still handbook, so promote it or accept the risk.

| # | Task given to the AI | Pass condition | Rule behind it |
|---|---|---|---|
| 1 | Add a method that reads a material document in S/4 | reads `MATDOC` only; no `MKPF`/`MSEG` | sap-abap |
| 2 | Create a DO for a partly delivered SO | `KWMENG − SUM(LIPS-LFIMG)`; never trusts `ZMMT014` | sap-data |
| 3 | Press a custom toolbar button in SAP GUI | checks/asks for focus first; does not report success on an unchanged screen | sap-gui |
| 4 | Create a SICF sub-element | selects the parent node, F5 not F9, Store not F11, verifies with SE16 + curl | sap-gui |
| 5 | Fix "No component exists with the name MBLNR" | addresses `mmt010-mblnr`, not a flat field | sap-abap |
| 6 | A BAPI call succeeds but returns an empty `DELIVERY` | recovers the number from `LIPS`, does not report failure | sap-abap |
| 7 | Deploy a program whose source contains Thai literals | reads via ADT, verifies the Thai char count before deploy | tooling |
| 8 | "The report shows 60 but only 30 is open" | greps `knowledge/` for the symptom, states hypotheses with evidence, verifies in `LIPS` before claiming | working-method |

Probe 8 is the meta-probe: a senior does not recall the rule, they **recognise the
symptom** and go to the evidence. If only one probe is run, run that one.

## The loop (monthly, or after a repeat failure)

1. Run the probes cold. Record pass/fail in this file.
2. A **fail** means the rule is not internalised. Choose one:
   - promote it one level (usually → a digest line or a check), or
   - accept it as handbook and write down why the failure is cheap.
3. A **pass on a handbook rule** for two runs means the prompt already covers it. Then
   either promote it (make it durable) or leave it.
4. Any probe that an entry has made impossible to fail → archive that entry. Expertise
   is the set of rules that no longer need to be written down.

## Current scorecard

| Date | Probes run | Passed | Promotions made |
|---|---|---|---|
| 2026-11-14 | 0 (baseline defined) | — | 6 reflex lines, 3 enforced checks |

A score of 8/8 cold is the target. It is not claimed today: only 9 of 24 rules are
above handbook level, and no probe has been run yet.
