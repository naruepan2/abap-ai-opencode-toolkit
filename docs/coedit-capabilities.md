# Co-edit capability matrix — per harness

A capability is true **for one harness, at one snapshot date**. Two installations
can disagree on whether a field exists. Never copy a row from another harness.
The matrix lives here so a rule in `docs/catalog.md` §"Co-edit contract" can point
at evidence instead of trusting memory.

Source labels: `LIVE` = tool schema mounted in that harness; `SRC` = installed
package source; `INPUT` = another harness's document, not evidence here.

## OpenCode — verified 2026-11-19

Writer: `ai-dev` (the ARC-1 package has CAS code but `SAPWrite` is **not mounted**;
do not claim an ARC-1 write guard in this harness).

| Need | Tool / field | Label | Notes |
|---|---|---|---|
| fresh source + hash | `get_source(include_hash=true)` → `{source, sourceHash}` | LIVE | `include` / `method` narrows `CLAS` to include or method |
| guarded edit | `edit_source(expected_source_hash=<fresh hash>, method=...)` | LIVE | field is **optional** — the caller must always send it |
| guarded full write | `write_source(expected_source_hash=..., mode="update")` | LIVE | same optionality |
| lock / unlock | `lock_object` → `lock_handle`; `unlock_object` | LIVE | no standby owner query; handle exists only after lock |
| activate | `activate` / `activate_multiple` | LIVE | per batch |
| inactive beacon | `get_inactive_objects()` | LIVE | one call |
| light state check | `SAPDiagnose(action="object_state", name, type)` | LIVE | active/inactive etag + byteLength + **sha256** + `divergent` + `hasInactiveDivergence`; SRC: `arc-1/dist/adt/diagnostics.js:36-70` |
| fresh ARC-1 read | `SAPRead(type, format="editable", force_refresh=true)` | LIVE | `{source, sourceHash}` of ARC-1; use for observation, not to verify an ai-dev write |
| diff / versions | `SAPRead(action="diff", force_refresh=true)`, `VERSIONS`, `VERSION_SOURCE` | LIVE | only on a hit |
| cheap beacons | `SAPTransport(list, summary=true)`, `SAPRead(type="INACTIVE_OBJECTS")`, `SAPRead(type="DEVC")` | LIVE | hints, never guards |
| graph | `SAPContext(action="impact" \| "deps" \| "usages")` | LIVE | `impact` alone is partial for RAP |
| CAS internals | `expectedSourceHash` schemas lines 677/789; `assertSourceHash` under lock at 430-432 and `source-precondition.js:7` | SRC | `arc-1@1.10.1` installed locally |
| ai-dev CAS field | `expected_source_hash` in `vsp-win32-x64.exe` (4 hits) and in mounted schema | LIVE+SRC | an earlier claim that ai-dev has no CAS came from scanning only `.js`; it is wrong here |

Cache facts for this package version (SRC, `arc-1/dist/cache/caching-layer.js:27,34`):
`ACTIVATION_FRESH_MS = 120_000`; inactive-list TTL 60s. A read just after
activation can be stale — use `force_refresh` or a different engine.

## Read-only probe result — DS4/100, 2026-11-19

Target: a demo program in package `ZABAPGIT_DEMOS` (no customer data). No write,
no lock, no activation.

| Check | Result |
|---|---|
| `SAPDiagnose(object_state)` twice | identical `active.sha256` (`6670b612…`) and etag; `hasInactiveDivergence=false` |
| `SAPRead(format="editable", force_refresh=true)` twice | identical `sourceHash` (`6670b612…`), same 10,538-byte source |
| `ai-dev.get_source(include_hash=true)` on the same object | `sha256:56d1fbe0…` — same byte length, **different hash** |

Conclusion: hash stability holds within one engine, and hashes must not be
compared across engines. `object_state` and ARC-1 editable read agree here.

## Sandbox test — DS4/100, 2026-11-19

Controlled object `ZCOEDIT_SANDBOX` (PROG) created in `$TMP`; it is a **local**
object and is not in transport `DS4K904994` — the test proves detection after a
baseline hash, not an object membership change in a released TR. No customer
object was touched.

| Step | Evidence | Result |
|---|---|---|
| baseline A | `object_state.active.sha256 = 784ba5ab…`; local raw-byte SHA-256 = same; ai-dev `sourceHash = 242e63c5…` | ARC-1 hash matches raw bytes; ai-dev hash differs |
| simulate external edit B | `write_source(expected=ai-A)` → B, activated; no new version | success |
| detection | `object_state.active.sha256 = b72445d9…` ≠ stored `784ba5ab…`; `hasInactiveDivergence=false` | **external activated edit detected**; TR feed not needed |
| CAS guard | `edit_source(expected=ai-A)` → `SOURCE_DRIFT`, current `504fce22…`; source still B | no overwrite |
| undo | `write_source(expected=ai-B)` with pre-image A → activated; `object_state.active.sha256 = 784ba5ab…` | restored by forward write under CAS |
| cache | `format="editable"` plain vs `force_refresh=true` after activation → same hash | cache window not demonstrated here |

`coedit_baseline.py` used `.baseline/blobs/sha256/784ba5ab…` with intent
`CHG-SANDBOX-A`; `attach` recorded the post-hash.

Cleanup: both artifacts were deleted through temporary `sap-gui` and verified
gone with read-only ADT calls (`DS4K904994` → 400 does not exist;
`ZCOEDIT_SANDBOX` → 404 not found). `sap-gui` was returned to `enabled: false`.

How to delete a TR with the mounted GUI tools: SE10 → Display →
`Edit > Find...` → type the request number → in the hit list use
`Position cursor` (F2) → back on the main list `Request/Task > Delete...` →
confirm. A direct `sap_set_focus` on the list label is **not** enough — SE10
keeps its own list cursor. `arc1.SAPTransport` and ai-dev expose no delete
action, so this GUI path is the only mounted one.

## Second sandbox test — object inside a real open TR, 2026-11-19

`ZCOEDIT_SANDBOX2` was created in transportable package `Z001` inside open TR
`DS4K904996` (`SAPTransport(get)` listed it as the single object, status `D`,
`locked=true`). `SAPRead(VERSIONS)` showed only revision `00000` from creation —
no new revision after the later activations.

| Test | Evidence | Result |
|---|---|---|
| baseline A | `object_state.sha256 = d104fa71…`; ai-dev hash `6e16b80a…` | stored via `coedit_baseline.py`, intent `CHG-TR-A` |
| edit B activated in the open TR | `active.sha256 = 3c09c029…`; TR still `D`, 1 object | **detected** even with a live TR feed |
| cache | primed `SAPRead` text, wrote C via ai-dev, reread plain vs `force_refresh` → both showed C | 120 s stale window **not reproduced** here; `format="editable"` also sends `Cache-Control: no-cache`. Do not claim it as proven. |
| three-way, non-overlapping | pre A(L2-A), post B(L2-B), current C(L3-C) → wrote merged `L2-A + L3-C` under CAS of C | external L3 edit preserved, AI write undone |
| three-way, overlapping | pre P(L2-A), post Q(L2-Q), current R(L2-R) → hunk L2 overlaps | **no write**; `UNDO_CONFLICT` artifact created for human decision; source stayed at R |

Cleanup for this second sandbox was done manually by the user after `sap-gui`
Scripting was unavailable (`sapgui/user_scripting` disabled). Verified gone with
read-only ADT calls: `DS4K904996` → 400 does not exist; `ZCOEDIT_SANDBOX2` →
404 not found. The GUI policy file now allows `SE38` for future sessions.

## Object-family capability matrix — DS4/100, 2026-11-20

Read-only probes against the object-type list supplied for the index study.
Methods: `SAPSearch(objectType=<type>)`, `SAPRead(format="editable",
force_refresh=true)`, `SAPDiagnose(action="syntax", source=<source with an
in-memory comment block>)`. No SAP write. Comment results are summarised here;
the block format and placement live in `docs/coedit-index.md`.

| Family | Search | Editable source + hash | Syntax check | Comment block | Note |
|---|---|---|---|---|---|
| PROG | yes | yes | yes | `*` pass | |
| CLAS | yes | yes | yes | `*` pass | |
| INTF | yes | yes | yes | `*` pass | |
| FUNC | yes | yes | yes | `*` pass | ARC-1 reads by name; ai-dev needs `parent` |
| FUGR | yes | **no** | no | n/a | use its `INCL` members instead |
| INCL | yes | yes | needs a master program | not proven standalone | syntax check refuses an include without its master |
| TRAN | yes | no | n/a | n/a | metadata only |
| DDLS | yes | yes | yes | `//` pass | |
| DDLX | yes | yes | yes | `//` pass | |
| STOB | yes (`STOB/DO`) | via **DDLS** type | yes | `//` pass | `SAPRead` has no `STOB` type; URI is `/sap/bc/adt/ddic/ddl/sources/...` |
| DCLS | yes | yes | yes | `//` pass | |
| BDEF | yes | yes | yes | `//` pass | |
| SRVD | yes | yes | yes | **rejected** | `"Comments are not supported and will be deleted on save"` |
| SRVB | yes | no | no | n/a | not in the editable text-source list |
| TABL / VIEW / DTEL / DOMA / TTYP / SHLP / ENQU / MSAG / AUTH | yes | no | n/a | n/a | metadata; SHLP has its own JSON text output, not editable |
| ENHO | yes | in schema, not probed | UNVERIFIED | UNVERIFIED | |
| STRU / TYPE / XSLT / IWMO / IWSV / IWPR / ENHS / SXCI / UI5B / WDYN / WAPA / BIMP | mixed | **not in mounted `SAPRead` type union** | n/a | n/a | search only for most; `TOBJ` search returned none |

The mounted `format="editable"` text-source list is exactly: PROG, INCL, CLAS,
INTF, FUNC, DDLS, DCLS, BDEF, SRVD, DDLX. Anything outside it has no
`{source, sourceHash}` pair from this tool and cannot be a source-comment node in
the index.

TADIR SQL (`SELECT ... FROM tadir`) is **not available**: `SAP_ALLOW_FREE_SQL`
is false in this harness. Use `SAPSearch(searchType="tadir_lookup")` or
`SAPRead(type="DEVC")` for object discovery instead.

## Other harnesses

Do **not** fill this section from OpenCode evidence. Each harness must record its
own `tools/list` snapshot with version and date. A field absent from that snapshot
means the operation is read-only or needs a human gate, even if another harness has it.

## Rules

1. Re-check the matrix when an MCP server, adapter, or schema version changes.
2. A hash is engine-scoped. Store `engine` next to every hash. Never compare an
   ai-dev `sourceHash` with an ARC-1 `object_state.sha256` — canonicalization can
   differ. Use one engine for a write's pre/post pair; use `object_state` only as
   a separate observation beacon.
3. `expected_source_hash` is optional in the schema but mandatory in our method.
4. ETag is cached inside ARC-1 but not exposed as a tool parameter — do not build
   a rule that depends on conditional GET/304.
5. When a required field is missing, stop or downgrade to read-only/human gate.
   Do not invent the capability.
