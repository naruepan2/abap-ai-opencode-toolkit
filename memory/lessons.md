# Lessons

> One row per lesson. Only durable, reusable lessons — not conversation filler.
> A lesson becomes a skill candidate only after the same correction appears twice
> (or once if the risk is high).

| Date | What happened | Evidence | Generalizable? | Target |
|---|---|---|---|---|
| 2026-11-13 | งาน ZDEMO01: ต้องแยกแถว history ออกจากแถวที่ต้องสร้าง DO ใหม่ ไม่งั้น guardrail 041 บล็อกงานทั้งที่ยังเหลือยอด | `reports/DECISIONS.md` v6, test plan | yes — pattern "history vs actionable row" | memory / future skill `sap-ztable-history-persistence` |
| 2026-11-13 | ก่อน deploy ต้องตรวจว่า source ที่ dump มาจาก CLI ภาษาไทยไม่เพี้ยน | v6 Thai chars 1,986, source md5 | yes — SAP/Thai source handling | memory rule |
| 2026-11-13 | เลือกใช้ ADT สำหรับ source/DDIC และ SAP GUI สำหรับ runtime/policy-blocked ช่วยลดการเดา | session ZDEMO01 | yes — tool routing | tool-map |

## How to add

- Date: `YYYY-MM-DD`
- What happened: one line, concrete
- Evidence: file/path, command output, test result
- Generalizable: yes/no + why
- Target: `memory` / `agent` / `skill` / `script-or-check` / `AGENTS.md`
