# <PROGRAM> — RAP object index

Read this file, not the whole stack. This is a **thin read map**: which artifact
does what, which layer it sits in, which runtime phase it affects, and which TR
last touched it. It is **not** a log and **not** a copy of SAP source. Place it at
`spec/RAP_INDEX.md` next to `spec.md` and `spec/FS_INDEX.md`.

SAP stays the authority for exact code diffs and released versions. This index is
the local navigation map that lets a person or an agent pick the one artifact a
task needs instead of opening 20–120 objects.

| | |
|---|---|
| stack | <PROGRAM> — <one-line business object> |
| system / client | <SID> / <client> |
| package(s) | <Z...> |
| implementation | managed / unmanaged / managed with unmanaged save |
| draft | yes / no |
| object count | <n> |
| spec | `spec.md` — REQ / AC / Q |
| history | `CHANGELOG.md` — one row per deploy / TR |
| last_tr_check | <YYYY-MM-DD> (date of the last live TR scan) |
| last_tr_seen | <TR1>,<TR2> (TR ids seen at that scan) |

## 1. Chain map — read this first

Write the dependency chain, not a flat list. One line per path, left = upstream,
right = consumer:

```
ZI_<ROOT> → ZI_<COMPOSITE_1> → ZI_<COMPOSITE_2> → ZC_<CONSUMPTION>
ZI_<ROOT> → ZB_<BDEF> → ZCL_<POOL>
ZC_<CONSUMPTION> → ZDLX_<MDE> → ZSRVD_<SRVD> → ZSRVB_<SRVB>
```

Rule: a change to an upstream `ZI_*` can affect everything to its right. Before
changing one, run `SAPContext(action="impact", type="DDLS", name="<object>")`
and follow the returned downstream set. Do not read every object in the chain.

## 2. Artifact table

`Phase` = which stage a change to this artifact affects:
`design` (dependency/contract), `metadata` (`$metadata` / UI),
`interaction` (buffer, determination, validation, action, auth, feature),
`save` (FINALIZE → CHECK_BEFORE_SAVE → ADJUST_NUMBERS → SAVE → COMMIT → CLEANUP),
`draft` (draft persistence / activation).

| Layer | Object | Type | Role / Phase | Upstream → downstream | Last TR | Spec section |
|---|---|---|---|---|---|---|
| persistence | <table> | TABL | active data · save | → ZI_\<ROOT\> | <TR/none/$TMP> | REQ-.. |
| persistence | <draft table> | TABL | draft state · draft | ↔ ZI_\<ROOT\> | <TR/none/$TMP> | REQ-.. |
| interface | ZI_\<ROOT\> | DDLS | BO data model · design | \<table\> → … | <TR> | REQ-.. |
| interface | ZI_\<COMPOSITE\> | DDLS | composed view · design | ZI_\<ROOT\> → ZC_\<…\> | <TR> | REQ-.. |
| behavior | ZB_\<…\> | BDEF | base behavior contract · design/interaction/save | ZI_\<ROOT\> → ZCL_\<POOL\> | <TR> | REQ-.. |
| behavior | ZCL_\<POOL\> | CLAS | handler logic · interaction/save | implements ZB_\<…\> | <TR> | REQ-.. |
| projection | ZC_\<…\> | DDLS | consumer data contract · design/metadata | ZI_\<…\> → SRVD | <TR> | REQ-.. |
| projection | <projection BDEF> | BDEF | exposed operations · design/interaction | projects ZB_\<…\> | <TR> | REQ-.. |
| metadata | ZDLX_\<…\> | DDLX | @UI/@Search annotations · metadata | annotates ZC_\<…\> | <TR> | REQ-.. |
| access | <DCL> | DCLS | row security · interaction | entry-point entity | <TR> | REQ-.. |
| exposure | ZSRVD_\<…\> | SRVD | exposed entities · metadata | ZC_\<…\> → SRVB | <TR> | REQ-.. |
| exposure | ZSRVB_\<…\> | SRVB | protocol + publish · metadata | → OData `$metadata` | <TR> | REQ-.. |

Add only the rows the program actually has. Delete template rows that do not
apply. Never paste source into the Role cell — one short phrase only.

## 3. How to read

1. Read the **chain map** → find the layer the task touches.
2. Read the **one artifact row** → get its type, upstream/downstream and TR.
3. Open `spec.md` at that section for the requirement.
4. Read live SAP only for that artifact:
   - `SAPContext(action="deps")` for upstream contracts / KTD.
   - `SAPContext(action="impact", type="DDLS")` for downstream blast radius.
   - `SAPRead(type="DDLS|DDLX|BDEF|SRVD|SRVB", name=...)` for the artifact.
   - `SAPRead(type="API_STATE", name=...)` before using a CDS view — prefer C1/C2.
   - `SAPRead(action="diff", from=..., to=...)` for a change, not two full reads.
5. Never read the whole stack. Never mirror source into this file.

## 4. When someone edited in SAP outside the agent

Do not try to re-sync the whole stack. Detect, locate, record:

```
SAPRead(type="INACTIVE_OBJECTS")                              # 1 call, unactivated edits
SAPTransport(action="list", status="*", user="*", summary=true)
SAPTransport(action="get", id=<new TR>)                        # only on a hit
SAPRead(type="VERSIONS", name=<hit>)                           # only on a hit
SAPRead(type="<TYPE>", name=<hit>, action="diff", from=..., to=..., force_refresh=true)
SAPContext(action="impact", type="DDLS", name=<hit>)           # downstream of the hit
```

Compare with `last_tr_check` / `last_tr_seen` above.

- No new TR and no inactive object → the index is still usable; continue.
- Hit → list the affected objects to the user and ask before changing anything.
- Add **one new row** to `CHANGELOG.md` with `Scope` = only the affected objects
  and the TR that carried the change. **Never edit or delete an old row.**
- Edit only the affected rows in the artifact table; update `last_tr_check` and
  `last_tr_seen`. Do not append a second log.
- If a source read looks stale after an external edit, pass `force_refresh=true` —
  ARC-1 caches source. Without it the cache can hide the change.
- Objects created/changed in `$TMP` or a local package may never appear in a TR
  scan. `INACTIVE_OBJECTS` and `VERSIONS` cover the rest; if still unclear, ask.

## 5. Verification reminders (RAP is not classic)

| Symptom | Check before blaming the code |
|---|---|
| PATCH ok but DB still old | data in transactional buffer, not saved yet; read local mode |
| UI field not refreshed | side effect tells the client to re-GET; determination may already have run |
| draft edit but active unchanged | draft table ≠ active table (`IsActiveEntity = false`) |
| 403 | authorization / DCL / communication setup, not data flags |
| 412 | ETag / `If-Match` stale |
| Field or facet missing | DDLX target, `@Metadata.allowExtensions`, `@Metadata.ignorePropagatedAnnotations`, then `$metadata` |
| Save did not persist | `failed` / `reported`, `CHECK_BEFORE_SAVE`, saver method, transaction contract |

Save sequence is not a fixed "validation → determination → finalize" chain:
triggers follow the behavior model. Persistence ownership differs by managed,
unmanaged, and managed with unmanaged save. EML bypasses HTTP but still enters the
RAP runtime — do not put `COMMIT WORK` in a handler.

## 6. Limits

Runtime details vary by ABAP Platform release, OData V2/V4 binding, draft vs
non-draft, and managed vs unmanaged implementation. Confirm against SAP Help for
the release in use. This index is a navigation aid, not a specification.
