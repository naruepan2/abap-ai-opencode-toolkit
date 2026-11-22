# Requirement checks by program type

The per-type checklist to apply while planning, after the model in step 3 is
chosen. Read it when writing the plan or the Pre-Flight scope, not while
surveying options.

Gather only the checks relevant to the chosen design:

- **Reports**: selection fields/ranges and defaults, authorization, expected row
  volume, foreground/background use, and required output behavior.
- **SALV/ALV**: read-only versus editable, columns, sorting/totals, layout
  variants, user actions, and export/spool needs.
- **Function modules**: caller contract, RFC/update-task requirements, exception
  behavior, idempotency, and which layer owns the transaction/commit.
- **Enhancements**: business execution point, available supported extension
  points, filters, side effects, and upgrade impact.
- **RAP**: transactional lifecycle, draft requirement, authorization/locking,
  messages, service protocol, and required actions/validations/determinations.
