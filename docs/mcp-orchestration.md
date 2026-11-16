# Running several SAP MCP servers without lying to yourself

`docs/mcp-capability-matrix.md` answers *which engine can do which job*. This page
answers *what happens when two of them are on at once, and who decides*. Every claim
below is tied to a file or a documented behaviour; the checks at the end reproduce the
facts in one command.

---

## 1. What is actually true when servers run together

| Claim | Verdict | Evidence |
|---|---|---|
| Tool names collide | No | OpenCode names a tool `<server>_<tool>` and keeps `-`, so `arc1-ds4-100_SAPRead` is unique. Verified against the live catalog: no duplicate name. |
| The servers share state | No | One process per server. Caches, locks and HTTP clients are per process. |
| A read can return source written by another engine | No, with one window | ARC-1 revalidates every cached read with the object's ETag (`src/cache/caching-layer.ts:141-153`), so a source read after a foreign write fetches the new text. The exception is ARC-1's own 120 s post-activation window (`ACTIVATION_FRESH_MS`). |
| Two engines can corrupt one object by writing at the same time | No | ADT serialises writes: lock, `PUT` with `lockHandle`, unlock (`src/adt/crud.ts:67-83`); the loser's 423 is read as a lock-handle failure (`src/adt/errors.ts:771`). |
| Two engines can lose an update | **Yes** | Sequential read-modify-write has no conflict detection: engine A reads v1, engine B writes v2, A writes based on v1 and v2 is gone. The write path sends no ETag precondition. |
| One engine's prompt text leaks into another's | No | Each agent has its own system prompt. OpenCode also drops a server's `<mcp_instructions>` from an agent whose permissions deny every tool of that server. |
| The model picks a server deterministically | No | Availability is not routing. Three engines with overlapping verbs (read, search, write) leave the choice to the model unless it is constrained. |

So "more than one server enabled" is not the hazard. **The hazard is two write-armed
servers pointed at the same client while an object is being edited twice**, plus the
human cost of not knowing which engine produced a fact.

---

## 2. Coverage: arc-1 vs ai-dev

Neither replaces the other. ai-dev is **wider**; arc-1 is **deeper on SAP-side
operations and policy**. Counting tools misleads in both directions: arc-1 exposes 12
verbs, but `SAPDiagnose` alone dispatches 26 actions, and ai-dev exposes 75 small tools
that a single ARC-1 verb covers.

| Job | ai-dev | arc-1 |
|---|---|---|
| Read source, search objects, grep | yes | yes |
| Create / edit ABAP objects | yes (`create_object`, `write_source`, `edit_source`) | yes (`SAPWrite`) |
| Activate | yes | yes (`SAPActivate`) |
| Domain / data element / table type | **no** | yes (`SAPWrite` `DOMA`/`DTEL`/`TTYP`) |
| Tables and structures | yes | yes |
| CDS impact and dependencies | yes | yes (`SAPContext`) |
| ATC | yes | yes (`SAPDiagnose` `atc`) |
| ABAP Unit | yes | yes (`SAPDiagnose` `unittest`) |
| CDS test cases | no | yes (`CDS_TESTCASES`) |
| **Debugger** (attach, step, variables, breakpoints) | **yes, only here** | no |
| Dumps, SQL trace, SQL statements, gateway errors, auth trace | partial | yes (`SAPDiagnose`) |
| Transport read / create | yes | yes |
| **Transport release / delete / reassign** | **no** | yes (`SAPTransport`) |
| Table preview and free SQL | yes (`run_query`) | yes (`SAPQuery` `sql`) |
| Long text and application log | partial | yes (`SAPQuery` `long_text`, `application_log`) |
| abapGit / gCTS | no | yes (`SAPGit`) |
| **UI5 / Fiori app files** | **yes, only here** | no |
| **ABAP Cloud migration planning, API release state** | **yes, only here** | no |
| RAP service binding publish / unpublish | yes | no |
| Package allowlist, deny actions, auth scopes | not documented | yes |

Rule of thumb:

- **ai-dev** owns the edit loop, the debugger, and the frontend/migration jobs.
- **arc-1** owns analysis, DDIC entity types, transport lifecycle, abapGit, and the
  data/SQL surface.
- When both could do a job, prefer the one whose write scope you can prove.

---

## 3. The model: three layers

**Layer 1 — process.** Is the server connected at all? `mcp.servers.<name>.disabled`.
Anything not needed for the current task stays disabled. Today only two ADT engines
are ever live at once. `fr0ster/mcp-abap-adt` is **not configured at all** — there is
no entry for it in `opencode.json`, so it cannot connect and costs no context. It stays
out for two reasons that still hold: its credentials travel as env vars (its
authentication guide has no keychain route) and nothing wires it to the launcher.
Not because of CDS — it does cover DDL, DDLX, BDEF, SRVD and SRVB; what it lacks is
DCL and the classic views.

**Layer 2 — permission.** Which agent may call which server? V2 `permissions` entries
match the normalized `<server>_<tool>` action, and a deny hides the tool *and* drops
that server's instructions from that agent's prompt. A custom subagent uses its own
permission list, not its parent's, so this is the layer that stops two agents from
reaching for different engines on the same job.

```jsonc
{
  "agents": {
    "abap-developer": {
      "permissions": [
        { "action": "arc1*", "resource": "*", "effect": "deny" }
      ]
    },
    "abap-runtime-debugger": {
      "permissions": [
        { "action": "ai-dev*", "resource": "*", "effect": "deny" }
      ]
    }
  }
}
```

`*` matches zero or more characters, so `arc1*` covers the server whatever the
name-normalization does with `-`. Agent rules are appended after global rules and the
last match wins; a deny placed globally can therefore be re-allowed by an agent. Keep
the deny in the agent that needs it.

**Status: documented, not configured.** `opencode.json` carries no `agents` block and
no `permission` entry today, so this layer is not enforced — every agent sees every
connected server and picks by name. That is why §5's rule is a rule for the model
rather than a mechanism.

**Layer 3 — posture.** What is the engine allowed to do *in SAP*? This is not a tool
list. `SAPWrite` disappears when the launcher does not pass `-AllowWrites`, and the
same binary can be read-only on one profile and write-armed on another. `sap-mcp.ps1`
is the single place that decides, and `tools_now.py` prints the result.

---

## 4. Posture: what each flag unlocks

ARC-1 ships read-only. Defaults come from `src/adt/safety.ts:92-104`; the opt-in
table below is the vendor's own (`docs.arc-1-mcp.com/local-development`, "What's
blocked by default").

| Capability | Flag | Default | Blast radius if enabled |
|---|---|---|---|
| Object writes | `-AllowWrites` | off | create/update/delete/activate, ceiling `$TMP,Z*,Y*` |
| Named table preview | `-AllowDataPreview` | off | reads business data, unlocks `long_text` and `application_log` |
| Freestyle SQL | `-AllowFreeSql` | off | any `SELECT` the SAP user may run |
| Transport mutations | `-AllowTransportWrites` | off | **no package check** — release/delete hits any transport unless `-AllowedTransports` is set |
| Git mutations | `-AllowGitWrites` | off | abapGit/gCTS writes |

Two facts that change how you read that table:

1. **Data preview + free SQL do not require writes.** The vendor documents that pair
   as the read-only way to get table preview and SQL. Enabling both leaves the engine
   unable to change a single object. What it does change is *what data the agent can
   read* — that is a policy decision, not a safety-bug decision.
2. **Release has no package gate.** `checkTransport` (`src/adt/safety.ts:335-357`)
   checks `allowWrites`, `allowTransportWrites` and the transport whitelist only. An
   empty `SAP_ALLOWED_TRANSPORTS` means every transport is fair game, including one
   carrying another team's objects. Keep transport writes off and release by hand, or
   pass `-AllowedTransports` explicitly.

Neither `SAP_ALLOW_DATA_PREVIEW` nor `SAP_ALLOW_FREE_SQL` widens the package ceiling,
and `SAP_ALLOWED_PACKAGES` never gates reads (`src/adt/safety.ts:250`). It gates
create/update/delete/activate against the object's **real** package, fail-closed:
create checks the parent package, activation re-reads the object's package and aborts
the whole batch if one object is outside (`src/handlers/activate.ts:301-314`).

---

## 5. The rule

> **One object, one writer, one session.** Any number of readers may look at the same
> object; a second engine may only *write* it after the first is done and the object is
> re-read. Every finding names the engine and tool that produced it.

This replaces "one writer per task", which was both too strict (two write-armed engines
are fine on different objects) and too vague (it never said what breaks). The precise
version follows from §1: concurrent writes are serialised by the ADT lock, sequential
ones are not, and the only unrecoverable outcome is the lost update.

Two corollaries:

- **Verify with a different engine than the one that wrote** — that is a read, and
  ETag revalidation makes it trustworthy. It is the cheapest correctness check we have.
- **Never cite two engines for one fact.** If they disagree, one of them is reading a
  different version; resolve that first.

---

## 6. Verify, don't remember

```bash
python scripts/tools_now.py          # live servers + armed posture, per profile
python scripts/session_context.py    # the digest line the session already uses
```

`tools_now.py` reads the launcher command from the OpenCode MCP config, joins it to
`sap/profiles.json`, and prints `POST profile <name> <SYS>/<client> pkgs <ceiling>
transport=… data=… sql=… git=…`. When a server is not a `sap-mcp.ps1` launch it says
`POST unknown` instead of assuming read-only, and `--check` fails when two write-armed
servers share one system/client.

The posture is derived from files outside this repository on purpose: the repo is
shareable, the config holds customer hostnames and usernames.

---

## 7. Keeping this page true

Re-derive the facts rather than trusting the prose:

```bash
git clone --depth 1 https://github.com/arc-mcp/arc-1 /tmp/arc-1
grep -n "Allowed\|allowWrites" /tmp/arc-1/src/adt/safety.ts
grep -n "invalidate\|revalidat" /tmp/arc-1/src/cache/caching-layer.ts
```

If a claim here stops matching the source, fix the claim — not the source.
