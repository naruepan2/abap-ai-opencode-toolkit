# Skill candidates

> A candidate needs evidence from at least two real sessions (or one high-risk
> incident). Do not create a skill just because it sounds useful.

| Candidate | Trigger | Evidence (>=2) | Target level | Status |
|---|---|---|---|---|
| sap-gui-transaction-tester | ต้องขับ SE16/SE38/VA03/VL03N, อ่าน ALV, จัดการ popup | ZDEMO01 session (SE16, VA03, VL03N, popup handling) | skill | draft when repeated |
| sap-ztable-history-persistence | ออกแบบ/เขียนประวัติลง Z-table (key, PGI_FLAG, idempotent MODIFY) | ZMMT014/ZMMT015 design in ZDEMO01 | skill | draft when repeated |
| sap-adt-deploy-verify | write-source → syntax → activate → inactive → encoding check | ZDEMO01 v2–v6 deployments | skill | evaluate (may overlap abap-development) |
| sap-sicf-service-create | สร้าง/ตรวจ ICF service ใน SICF (select node → F5 → handler → Store → activate) | HCL Interface session 2026-11-13: สร้างผิด dialog เพราะไม่ select node, ใช้ wizard F9 ผิด, verify ด้วย SE16+curl | skill | draft (high-risk incident, 1 session) |

## Rules

- Status: `idea` → `draft` → `testing` → `active` → `rejected`
- Before creating: check whether an existing skill already covers it.
- Draft lives in the normal skills folder but with `status: draft` in frontmatter.
- Promote only after one real task uses the draft successfully.
- Vendor skills stay read-only; new skills are Pongg-owned.
