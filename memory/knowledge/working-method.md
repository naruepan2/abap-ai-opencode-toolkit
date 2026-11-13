# Knowledge: working method

> Rules about how to do the work, independent of SAP. One entry per rule; edit in
> place and raise `Seen` — never add a second entry for the same rule.
> Schema and the consolidation gate: `docs/memory-model.md`.

## Read the live source before patching

- **Rule:** re-read the deployed source (`ADT get_source`) before every patch; the
  local copy or a memory of it is a hypothesis.
- **Why:** the local file and the live object drift silently.
- **Break it, and:** the patch applies to code that is not there — the diff is
  rejected, or worse, an older version is re-deployed.
- **Seen:** 2 · **Confidence:** high · **Last confirmed:** 2026-11-13
- **Evidence:** ZDEMO01 v5 vs live diff (`kosta` found in the live object only)

## Verify before claiming absence

- **Rule:** never conclude "it does not exist" from a filter popup, an empty ALV, or
  a failed search. Confirm in the table, over HTTP, or with a second tool.
- **Why:** an empty result proves the *filter* missed, not that the object is absent.
- **Break it, and:** you report a missing object that exists — and the user rebuilds
  something that was already there.
- **Seen:** 2 · **Confidence:** high · **Last confirmed:** 2026-11-13
- **Evidence:** `HCLINTERFACE` node existed while the SICF filter returned "no data"

## Find every cause, not the first one

- **Rule:** when a symptom has one obvious cause, still check the next layer
  (input data, preload key, API return) before declaring the fix.
- **Why:** two independent faults produce one symptom; fixing one leaves the bug.
- **Break it, and:** the fix "works" in one case and the same ticket comes back.
- **Seen:** 1 · **Confidence:** medium · **Last confirmed:** 2026-11-13
- **Evidence:** ZDEMO01 — preload key mismatch *and* a missing BAPI main-item row

## Establish the change contract before touching code

- **Rule:** before creating or editing a program, get four answers from the user:
  **FS** (does one exist, where?), **change type** (bug fix / feature extension /
  change request), **live on production** (yes/no, and is the dev object in sync),
  and **target** (system, client, transport). Record them in the project card.
- **Why:** each answer implies a different correct shape — minimal patch, designed
  delta, or impact analysis. Without them you cannot tell which one you are doing,
  and a "small improvement" becomes an unrequested refactor.
- **Break it, and:** you patch a symptom the FS never described, or edit a dev object
  that has already diverged from the production version — and the transport ships a
  change nobody asked for.
- **No FS is a finding, not a licence to invent one:** say so, and propose a one-page
  FS (goal, inputs/outputs, business rules, edge cases) for approval before coding.
- **Seen:** 1 · **Confidence:** high · **Last confirmed:** 2026-11-14
- **Evidence:** user instruction 2026-11-14; `docs/memory-model.md` §task kickoff

## Diagnose from the symptom, not from memory

- **Rule:** when a failure looks familiar, search `memory/knowledge/` for the symptom
  (`Break it, and` lines) before forming a hypothesis, then verify in the data.
- **Why:** recognising the symptom is what an expert actually does; the rule is
  useless if it is never retrieved at the moment of failure.
- **Break it, and:** you re-derive the cause from scratch, or confidently apply the
  wrong familiar rule to a different fault.
- **Seen:** 1 · **Confidence:** medium · **Last confirmed:** 2026-11-14
- **Evidence:** probe 8 in `memory/expertise.md`

## A rule that repeats belongs in a check, not in prose

- **Rule:** the second time a rule is violated, move it out of prose into
  `AGENTS.md`, a skill, or a script check — prose is not enforced.
- **Why:** what is written but not checked is forgotten under work pressure.
- **Break it, and:** the same correction is re-learned a third time.
- **Seen:** 2 · **Confidence:** high · **Last confirmed:** 2026-11-14
- **Evidence:** `memory_check.py` row budget and status schema replaced prose rules
