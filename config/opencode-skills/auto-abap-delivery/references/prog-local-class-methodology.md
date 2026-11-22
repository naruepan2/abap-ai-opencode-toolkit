# Report object design: local vs global classes

Class-first means **methods and classes**, not automatically separate SE24 objects.
For an executable program, local classes are preferred when the behavior is owned only
by that report. Do not force every design into global classes.

## Shapes

- **L1 — one PROG with cohesive local classes**: the report is the only consumer, no
  stable external API or independent lifecycle is needed, and the source stays
  reviewable. Keep `lcl_app`, `lcl_provider`, `lcl_salv`, and `lcl_event_handler` when needed.
- **L2 — local report classes + global reusable logic**: keep local orchestration,
  provider and SALV classes; move shared/domain logic to a global class when another
  object genuinely consumes it. This is the normal report + function-module hybrid.
- **G — thin PROG + global classes**: multiple consumers, a stable API, independent
  lifecycle/ownership, complex security boundary, or source complexity beyond the
  local threshold.

## Thresholds trigger design review, not automatic global classes

```yaml
prog_local_class_policy:
  maximum_local_classes: 4
  maximum_report_source_lines: 800
  maximum_public_methods_per_local_class: 8
  maximum_external_consumers: 0   # applies to L1 only
```

These are project defaults, not SAP limits. Exceeding one is a review signal.

## Responsibilities

- `lcl_app`: build the request and orchestrate authorization, provider, rules and output; expose one main method such as `run`.
- `lcl_provider`: bounded read-only access and normalization; no row-by-row SQL.
- `lcl_salv`: `CL_SALV_TABLE` construction, configuration and display only — no business calculation or SQL.
- `lcl_event_handler`: SALV event handlers and delegation only; keep the handler alive while SALV is displayed.

Place local types and class definitions before the first processing block, then
implementations, then small report events. Prefer methods; use `FORM`/`PERFORM` only
for a recorded exception from the engineering-judgment gate.

## Testing

Do not add inline `FOR TESTING` classes by default. Verify report behavior through
syntax, activation, foreground/background execution, authorization-negative checks,
sampled result cross-check, and ATC. If material reusable rules need ABAP Unit, move
only the rule owner to a justified global class test include.

## Evidence

Record `prog_design_decision`: strategy (`L1`/`L2`/`G`), local and global classes,
external consumers, reuse expectation, unit-test owner, rationale, and any threshold
exceeded. Keep this with the run evidence.

## Fail conditions

An unrecorded `FORM`/`PERFORM` fallback; one local God class owning SQL, rules, SALV, navigation and
authorization; duplicated logic between local and external objects; dynamic
cross-program use of a local class; or global classes created only because OO was
mistakenly assumed to require SE24.
