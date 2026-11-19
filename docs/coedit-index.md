# Local object index — proposal

Status: **IDEA / optional / read-only navigation aid. Not implemented.**
This is not a Knowledge Graph. The term *knowledge graph* is reserved for a later
layer that adds business capability, semantic meaning and human-curated features
(for example `Approval Status → Workflow → Escalation`). No evidence here
justifies that layer yet.

The index has one job: answer **"which object or sentinel do I query next?"** so a
300–450-object RAP package is not walked from source every session. It helps
navigation. It never authorises a write — `expected_source_hash`, the commit
window and the activation gate in `docs/catalog.md` remain the only safety path.

## Evidence collected 2026-11-19

A real 445-file RAP export was supplied locally as a **sample for this review**,
because DS4/100 has no object of comparable complexity. The sample is not in
git and no machine-specific path is recorded here; object names are withheld.
It was used only as source text and as a benchmark gold set — DS4/100 does not
contain these objects, so nothing about the sample was treated as live tool
evidence.

- 106 DDLS, 7 DCLS, 2 BDEF, 1 SRVD, 7 CLAS, plus a UI5 app.
- **42 of 106 DDLS** end in `_0` / `_1`; filenames alone cannot tell which object
  is the active one or which one supersedes which.
- 94 `select from` references across DDLS → 56 distinct targets.
- One root view only; the chain runs
  `root TP → interface view → _1 successor → _0 predecessor`. The
  "successor of" fact lives in a source comment, not in DDIC dependencies.
- Four DCLs guard that one chain; one inherits conditions from the `_0` object.
- The service definition exposes five entities; its leading entity is not the
  root view. The UI5 app binds to the OData service and contains a custom action
  that reaches a BDEF static action, an abstract parameter BDEF, a result DDLS
  and table-function classes — a chain across six object types.

Read-only live probe on **DS4/100 using a CDS pair that does exist there**
(names withheld from this shipped file). This verifies the *per-layer impact
principle* only; it is not a probe of the sample export:

| Query | Result |
|---|---|
| `SAPContext(impact)` on the **interface** view | 2 projection views, **0 access controls** |
| `SAPContext(impact)` on the **consumption** view | 1 projection view, **1 access control** (the DCL) |

So one impact query on the root/interface does not reveal the DCL; the
consumption-layer query does. This confirms the per-node/per-layer rule in
`templates/RAP_INDEX.md` and the claim received from another review, but with
our own evidence. The SRVD exposure claim came from the static export; it has
**not** been verified by a live probe on a stack that has a service binding.

Earlier sandbox probes also showed that ai-dev `sourceHash` and ARC-1
`object_state.sha256` differ for the same source bytes — so a node must record
its `hash_engine`.

## Node record

One node per **object + locator actually observed**, not one per package object.

```yaml
node:
  key: <system>|<client>|<type>|<name>|<locator>   # locator in the key: CLAS has includes/methods
  role: <root_view | interface_view | projection | behavior | exposure | access | draft | table_function>
  locator: <main | definitions | implementations | method:...>
  hash_engine: <arc1.object_state | arc1.editable | ai-dev.get_source>
  observed_hash: <digest>
  observed_at: <ISO-8601>
  source: <tool + version that produced it>
  status: <FRESH | STALE | DIRTY | PARTIAL | UNKNOWN>
```

`STALE` = TTL passed or upstream changed · `DIRTY` = a signal was seen ·
`PARTIAL` = tool coverage incomplete · `UNKNOWN` = no evidence. These may rank
candidates but may never authorise a write.

## Edge record

One hop, one claim, one piece of evidence.

```yaml
edge:
  from: <node key>
  relation: <selects | exposes | guarded_by | implements | calls_table_function | action_uses | consumed_by_app | succeeds>
  to: <node key>
  assertion: EXTRACTED        # INFERRED only after a separate human decision
  source: <SAPContext(impact) | SAPContext(deps) | source_parse | service_definition_read | manifest_read>
  evidence_hash: <hash of the source used to extract this edge>
  observed_at: <ISO-8601>
  valid_from: <ISO-8601>
  invalidated_at: <ISO-8601 or null>
  system_client_release: <scope; never merge DEV/QAS/PRD or clients>
  confidence: high            # tool-confirmed only; never auto-promote inferred
```

`succeeds` usually comes from a change comment. Store it as `HUMAN_CONFIRMED` or
`INPUT`, never as `EXTRACTED`, until a tool can confirm it.

## Edge types seen in the evidence

| Relation | Source | Example from the export |
|---|---|---|
| `selects` | source parse / `deps` | DDLS → DDLS, including the `_1 → _0` chain |
| `guarded_by` | DCL source or `impact` on consumption view | entity → DCL |
| `exposes` | service definition source | SRVD → five entities |
| `implements` | BDEF declaration | BDEF → behavior pool class |
| `action_uses` | BDEF source | static action → parameter/result DDLS |
| `calls_table_function` | DDLS source | DDLS → CLAS static method |
| `consumed_by_app` | UI5 manifest | OData service → UI5 app |
| `succeeds` | change comment (human-confirmed) | `_1` replaces `_0` |

## Optional write mode: disabled comment blocks

**Not the default.** Direct write (`APPLY_SOURCE_CHANGES`) stays the default path
under CAS. This mode (`INSERT_DISABLED_BLOCKS`) is an optional axis in the
approval card; choosing it locks activation to `DEFER`. It is still a **write**
and must obey fresh-read + CAS like any other.

Comment syntax evidence (checked 2026-11-20):

| Object family | Comment | Evidence |
|---|---|---|
| PROG / CLAS / FUNC | `*` in column 1 | ABAP convention |
| DDLS / SRVD | `//` to end of line; `/* ... */` allowed in CDS DDL | SAP Help `ABENCDS_GENERAL_SYNTAX_RULES`; DS4/100 `SAPRead(grep="//")` on a DDLS returned 13 hits |
| BDEF | `//` to end of line | SAP Help `ABENBDL_GENERAL_SYNTAX_RULES`; **no `/* ... */` documented** — do not use it |

### Block format

ABAP (`*` column 1), dividers top and bottom at the same length:

```abap
**********************************************************************
* COEDIT <intent> OP1/4 REPLACE_UNIT — unit: read_status — why: return reviewed V2
* BEFORE:1a2b3c… arc-1.editable — DISABLED — apply then delete this block
* OLD: METHOD read_status. result = 'V1'. ENDMETHOD.
* NEW: METHOD read_status. result = 'V2'. ENDMETHOD.
**********************************************************************
  METHOD read_status. result = 'V1'. ENDMETHOD.   "<<-- original untouched
```

DDLS / SRVD / BDEF (`//` on every line, including the divider):

```abap
//////////////////////////////////////////////////////////////////////////////////////////////////
// COEDIT <intent> OP1/4 REPLACE_UNIT — unit: ZI_X — why: use successor field
// BEFORE:1a2b3c… arc-1.editable — DISABLED — apply then delete
// OLD: LessThan1Year
// NEW: LessThan1Year_2 as LessThan1Year
//////////////////////////////////////////////////////////////////////////////////////////////////
  LessThan1Year   "<<-- original untouched
```

`OP1/4` = ordinal + total, so multi-op order is unambiguous. `BEFORE` is the
short fresh hash plus its engine; a changed hash voids the approval. The OLD/NEW
lines are human-readable summaries, not machine anchors.

### Placement

| Object | Inline block | Index block |
|---|---|---|
| PROG | before the affected statement in main source | head of program |
| CLAS | `implementations` before `METHOD`; `definitions` before declaration; `testclasses` before test method | head of the include holding most ops; one index per include if ops span includes |
| FUNC / FUGR | inside the FM include, before the statement | head of FM include (or top include for several FMs) |
| DDLS | before the field / association / statement | head of DDL source, **after** existing header comments, before the first `@` annotation |
| SRVD | before the `expose ...;` line | head of service definition |
| BDEF | before the behavior statement / action | head of BDEF, after existing header comments |

If a comment group already sits directly above the target, insert our block
**above the whole group** — that comment belongs to the target and must stay
adjacent to it. A trailing comment on the source line is untouched.

### Traps — all of these mean STOP + ask

1. **Anchor duplication:** the `OLD:` line repeats the anchor text, so a naive
   occurrence count finds 2. Count anchors only in **non-comment source**, never
   inside a COEDIT block. An anchor found only in comments → STOP.
2. **OLD/NEW are summaries:** for `REPLACE_UNIT` the real anchor is `anchor_text`
   + `unit`, not the one-line OLD text.
3. **Existing marker:** same `intent_id` → never stack. A different intent's
   block already present → also STOP and ask before adding another.
4. **Target is a comment:** never "fix" a comment into source. STOP.
5. Index block and inline block disagree → STOP; no auto-reconcile.

Commented code is never compiled — never claim syntax or ATC passed for it.

## Rules

1. Store only tool-confirmed or deterministic-source edges. A huge `deps` dump
   is not an index; summarising it would recreate the cost the index avoids.
2. Query `impact` **per sentinel**, not once for the whole package.
3. Read the service definition source for `exposes` edges; `impact` may return
   no service binding.
4. Every hash carries `hash_engine` and `locator`. Never compare across engines.
5. A cached hash is navigation evidence only. The commit window still re-reads
   the write-set; the index never bypasses CAS or user approval.
6. Re-index only the changed node and its immediate neighbours. No full rebuild,
   no background crawler, no server, no vector store.
7. Local and rebuildable. JSONL is enough for a pilot; SQLite only if multi-hop
   queries are measurably slow. Keep instance data in the gitignored local area;
   ship the schema/template only, never object names, hashes or customer data.
8. One home per fact: for a pilot, extend `spec/coedit-state.json` with an
   `edges` array rather than creating a second node store. Split to
   `spec/coedit-index.jsonl` only if edge volume demands it, and keep one logical
   index.

## Query protocol

`seed (object name / intent) → 1-hop neighbourhood → rank verified edges →
targeted SAP read → unchanged commit guard`. Never traverse without a hop cap,
and never let index output stand in for a fresh source read before a write.

## Exit criteria before this is more than an idea

Use the 445-file export as a local gold set (do not commit it). Benchmark 20–30
real questions: find the action, find the DCL, find the successor, find the
service exposure, trace the UI action. Compare source-first traversal with
index-assisted navigation.

- median source tokens reduced (proposed gate: ≥40%)
- no new impact misses; edge recall on a small verified gold set
- stale index causing an unsafe write: **0**
- graph/business/semantic layers stay out until these gates pass

Until then the index stays optional and read-only.
