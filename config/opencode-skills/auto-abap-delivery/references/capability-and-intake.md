# Capability audit and intake

## Live discovery
- Enumerate MCP servers, tool names/schemas, read/write/destructive classification, health, identity, SID/client, authorization, object coverage, source read/edit, activation, ABAP Unit, ATC, trace, diff, lock, and transport capabilities.
- Save `capability-snapshot.yaml`. Refresh after restart, configuration change, unknown-tool response, or resume.
- Classify `sap-abap-docs` separately as a read-only knowledge/documentation channel (release matrix, released API, community), not an ADT engine. Record its live availability and degrade to official docs/browser or `UNVERIFIED` when absent.

## Client and phase gates
- Name the development, runtime/preview, data-validation and dump clients before any data or runtime claim. A zero-row query in the wrong client is not evidence that data is absent; a dump from another client does not prove failure in the approved target. Reject a runtime claim whose relevant client cannot be accessed.
- Re-check tool availability, destination/client, package allowlist, write permission, object-type support, profile hash and known quirks before each of discovery, write, verification and recovery — not only once at session start. A disabled or denied tool requires re-arm or owner action; never silently switch destinations.

## Intake order
1. Business outcome, current/expected behavior, work type, ticket/spec, sample input/output, deadline, desired `READY_FOR_UAT` boundary.
2. Read-only target discovery: product/release, ABAP platform, database, language version, current client, object metadata, TADIR, package, original system, active/inactive source, lock, dependencies, test classes, ATC findings, and TR when available.
3. Ask only unresolved landscape mapping: Workbench, unit-test, sandbox, customizing/configuration master, authorization, integration, UAT, and production clients.
4. Resolve package, TR/task, naming, test-data policy, sensitive fields, external destinations, ATC variants, and trace permission.
5. Produce an assignment contract and request approval.

Never store passwords, tokens, tickets, private keys, or client secrets. Store a secure destination alias only.

## Test and runtime capability checks
During live discovery verify whether the MCP surface can create/update class test includes and run ABAP Unit, and whether service-binding publish/OData preview is available. Record `UNAVAILABLE` rather than inferring from object type. A missing runner is a tooling-evidence limitation, not permission to create a permanent test driver. Capture the AUnit runner result and the exact test location in the capability snapshot.
