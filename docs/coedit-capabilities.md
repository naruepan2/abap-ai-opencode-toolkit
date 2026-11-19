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
This probe proves the capability, **not** detection of an external edit — that
needs a controlled draft change in a sandbox or a real incident to observe.

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
