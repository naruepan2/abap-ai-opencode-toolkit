# Auto ABAP Delivery V8 — qualification policy

`qualification-config.yaml` is a **draft**: `status: draft` and
`qualified_scopes: []`. It unlocks no unattended run. The effective default is
Attended Standard; critical scope is Attended Controlled at minimum. The
`*.example.yaml` file is the untouched upstream template (it contains a fake
`qualified` scope with placeholder hashes — never activate it as-is).

Validate with the repo venv (Python 3.15 has no PyYAML wheel; the validators
fall back to pure-Python `ruamel.yaml`):

```powershell
.venv\Scripts\python.exe config\auto-abap-delivery\validate_qualification_config.py `
  config\auto-abap-delivery\qualification-config.yaml `
  config\auto-abap-delivery\qualification-config.schema.json

.venv\Scripts\python.exe scripts\compatibility_check.py
```

Promotion to `qualified_scope` requires real runs, evidence, and the two
approver roles defined in `promotion_requirements.approval`; never hand-edit a
scope to `qualified` without that record.
