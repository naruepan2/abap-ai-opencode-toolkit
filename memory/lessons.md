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
| 2026-11-13 | ใน S/4HANA ให้อ่าน `MATDOC` แทน `MKPF` + `MSEG` เพราะมีทั้ง header และ item fields ในตารางเดียว | MATDOC DDIC 350 fields; v10 deploy | yes — modern material document read | memory / future skill |
| 2026-11-13 | `sap-gui` อ่าน `%APPDATA%\mcp-sap-gui\policy.json` ครั้งเดียวตอน start; การ restart หน้าต่าง OpenCode ไม่ช่วย เพราะ MCP ถูกถือโดย daemon `opencode-cli.exe serve --service` | audit log: policy event 20:52 (allow SICF) แต่ call 20:54/20:56 ยัง blocked; 4 stack ค้าง 19:45/19:50/20:52 | yes — MCP config reload | memory / tool-map |
| 2026-11-13 | การ kill process ของ MCP server ที่ session ใช้อยู่ ทำให้ tool namespace หายจาก session กลางงาน | `sap-gui` หายจาก catalog หลัง kill 19:45/19:50 | yes — ห้าม kill MCP เพื่อบังคับ reload | memory rule |
| 2026-11-13 | SICF: F5 สร้าง sub-element ได้เฉพาะเมื่อ **select node แม่ใน tree ก่อน**; ไม่ select → เด้ง "Create/Change a Virtual Host"; F9 เป็น wizard (HTML popup อ่านไม่ได้) คนละ flow | popup title "Create/Change a Virtual Host" แล้วค่อยได้ "Create/Change a Service" | yes — SICF procedure | memory / future skill `sap-sicf-service-create` |
| 2026-11-13 | SICF tree เป็น ALV tree: `sap_read_tree`/`sap_find_tree_node_by_path` error "Cannot read tree node keys", และ `sap-gui` ไม่มี coordinate click → ต้องคลิกแถวใน GUI เอง | tool errors on `wnd[0]/usr/cntlALV_TREE` | yes — SICF/SAP GUI tree limits | memory / tool-map |
| 2026-11-13 | อย่าตัดสินว่า "object ไม่มี" จาก popup ของ filter ("Selection criteria did not select any data") — ต้องยืนยันจากตารางหรือ HTTP | node `HCLINTERFACE` มีจริง แต่ filter ตอนนั้นไม่ match | yes — verify before claiming absence | memory rule |
| 2026-11-13 | การส่ง arrow key ผ่าน `open-computer-use` ไป SAP GUI ไม่น่าเชื่อถือ ถ้า window ไม่ได้ foreground (key ไปลงหน้าต่างอื่น) | ctrl+home/down ไปลง VS Code, tree ไม่ถูก select | yes — GUI automation limits | memory / tool-map |
| 2026-11-13 | SICF service verify ได้โดยไม่ต้องมี ADT: `SE16` (ไม่บล็อก, ต่างจาก `SE16N`) อ่าน `ICFSERVICE`/`ICFHANDLER`/`ICFSERVLOC`/`TADIR` + `curl -k` เทียบ 401 กับ 404 | `/sap/bc/rest/HCLInterface` 401, `/sap/bc/rest/NOPE123` 404, ping 200 | yes — verification recipe | memory / future skill |

## How to add

- Date: `YYYY-MM-DD`
- What happened: one line, concrete
- Evidence: file/path, command output, test result
- Generalizable: yes/no + why
- Target: `memory` / `agent` / `skill` / `script-or-check` / `AGENTS.md`
