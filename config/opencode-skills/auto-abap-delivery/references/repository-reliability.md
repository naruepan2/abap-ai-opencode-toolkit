# Repository reliability and state-change reconciliation

## State-change contract

Before every create/edit/activate, persist an action contract:

```yaml
action_contract:
  command_id: CMD-...
  intended_object: Z...
  intended_action: create | edit | activate
  preconditions: { source_hash: sha256:..., sid_client: ..., transport: ... }
  expected_postconditions: [source_readback, active_or_inactive_state, inventory]
  reconciliation_required: true
```

A success message is a claim, not proof. Read back source, active/inactive state,
package, object inventory and the expected postconditions before continuing.

## Retry rule

On timeout, 409/500, or any ambiguous response, enter `REPOSITORY_RECONCILIATION`.
Never replay a create blindly. A DDLS create may persist TADIR before erroring —
check the existing object and write its source there instead of recreating it.

## Per-object postconditions

- **DDLS**: TADIR exists; source non-empty; active/inactive state known; syntax probe
  completed; no duplicate create after an ambiguous failure.
- **FUGR/FUNC**: main program and `FUNCTION-POOL`; `TOP` and `UXX` include chain;
  function include present; signature matches the approved contract; activation;
  target-client runtime availability — not just local activation success.
- **CLAS**: language version and class properties verified; source read-back;
  activation; test-runner capability recorded (`NOT_RUN_BY_AUNIT_TOOL` if absent).
- **SRVD/SRVB**: version/settings checked; activation order observed; active and
  published states kept separate; no runtime claim before publication.
- **Generic**: source hash and lock state match preconditions; package and transport
  ownership unchanged; no unapproved ghost object left behind.

Tool capability notes expire when the MCP/tool profile hash changes. Re-verify before
relying on a previously observed quirk.
