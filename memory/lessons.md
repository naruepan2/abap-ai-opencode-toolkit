# Lessons

> One row per lesson. Only durable, reusable lessons — not conversation filler.
> A lesson becomes a skill candidate only after the same correction appears twice
> (or once if the risk is high).

| Date | What happened | Evidence | Generalizable? | Target |
|---|---|---|---|---|
| 2026-11-13 | งาน ZDEMO01: ต้องแยกแถว history ออกจากแถวที่ต้องสร้าง DO ใหม่ ไม่งั้น guardrail 041 บล็อกงานทั้งที่ยังเหลือยอด | `reports/DECISIONS.md` v6, test plan | yes — pattern "history vs actionable row" | memory / future skill `sap-ztable-history-persistence` |
| 2026-11-13 | ก่อน deploy ต้องตรวจว่า source ที่ dump มาจาก CLI ภาษาไทยไม่เพี้ยน | v6 Thai chars 1,986, source md5 | yes — SAP/Thai source handling | memory rule |
| 2026-11-13 | เลือกใช้ ADT สำหรับ source/DDIC และ SAP GUI สำหรับ runtime/policy-blocked ช่วยลดการเดา | session ZDEMO01 | yes — tool routing | tool-map |
| 2026-11-13 | Preload `lt_so_lips_pre` เก็บ `LIPS-VBELN/POSNR` (เลข DO) แต่ READ ด้วยเลข SO — ไม่มีทาง match | debug line 5290, LIPS/VBFA | yes — name keys by source, not by shape | skill/future SAP Z-table pattern |
| 2026-11-13 | `BAPI_OUTB_DELIVERY_CREATE_SLS` สร้าง DO ได้แต่คืน `DELIVERY` ว่างเมื่อ `NUM_DELIVERIES > 1` | BAPI signature + DO 1041100092/18:06:31 | yes — import/check count, recover from LIPS | memory / future skill |
| 2026-11-13 | Batch split ต้องมี main item ใน `ITEM_CONTROL` ด้วย `CHG_DELQTY = 'X'` เมื่อ main item ส่ง qty 0 | `lt_item_data`/`lt_item_control` debug | yes — BAPI contract | memory / future skill |
| 2026-11-13 | ปุ่ม custom บน SAP GUI toolbar ไม่ทำงานถ้า session window ไม่มี OS focus; ปุ่ม ALV พื้นฐานยังทำงาน | `windows-mcp` USER_CONTROL + toolbar tests | yes — SAP GUI automation | tool-map |

## How to add

- Date: `YYYY-MM-DD`
- What happened: one line, concrete
- Evidence: file/path, command output, test result
- Generalizable: yes/no + why
- Target: `memory` / `agent` / `skill` / `script-or-check` / `AGENTS.md`
