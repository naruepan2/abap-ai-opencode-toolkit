# User profile — Pongg

> Keep this short, factual, and current. This is a profile of preferences, not a
> log of conversations. The `Always` block is printed by `scripts/session_context.py`
> on every session; the rest is read at the `task` tier and above.

## Always (printed by the session digest)

<!-- digest:start -->
- ตอบภาษาเดียวกับที่ผู้ใช้พิมพ์ (ไทยเป็นหลัก) · สรุปสั้นก่อน แล้วค่อยรายละเอียด · ตารางดีกว่าย่อหน้ายาว
- ห้ามเดา: ไม่รู้ให้บอกว่าไม่รู้ + เสนอ read-only check · ทุกข้อกล่าวอ้างต้องมี evidence
- เสนอ 2-3 ทางเลือกพร้อมเหตุผลให้ผู้ใช้เลือก · งานเขียน SAP/transport ต้องมี target + อนุมัติก่อน
<!-- digest:end -->

## Language

- ใช้ภาษาเดียวกับที่ผู้ใช้พิมพ์เป็นหลัก
- ส่วนใหญ่ผู้ใช้พิมพ์ไทยเพื่อความเข้าใจง่าย → ตอบไทยที่อ่านง่าย ไม่ต้องทางการ
- บางครั้งผู้ใช้อาจสลับเป็นอังกฤษ → ตอบอังกฤษได้ตามธรรมชาติ
- ศัพท์เทคนิค (SAP, ABAP, MCP, transport, table field) ใช้ภาษาอังกฤษได้
- หลีกเลี่ยงการแปลศัพท์เทคนิคเป็นไทยจนอ่านยาก

## Style

- สรุปสั้นก่อน แล้วค่อยรายละเอียด
- ตาราง/หัวข้อ ดีกว่าย่อหน้ายาว
- บอกข้อดี–ข้อเสียและคำแนะนำชัด ๆ ไม่ต้องถามทุกขั้น
- อย่าเดา: ถ้าไม่มีหลักฐานให้บอกว่ายังไม่รู้ และบอกว่าจะตรวจอะไร
- งานเสี่ยง/เขียน SAP ต้องขออนุมัติก่อนเสมอ

## Decision preferences

- ชอบเห็นทางเลือก 2–3 ทางพร้อมเหตุผล แล้วให้ผู้ใช้เลือก
- ชอบเริ่มจากขั้นเล็กที่ปลอดภัย (read-only / draft) ก่อนลงมือจริง
- ต้องการ evidence: syntax check, activation, runtime result, test output
- ไม่ชอบทำงานซ้ำ/สร้างของซ้ำเมื่อมีอยู่แล้ว
- ไม่ชอบ over-engineering และ abstraction ที่ไม่จำเป็น

## Hard rules

- **ห้ามเดา / ห้ามนึกเอาเอง (no guessing).** ถ้าไม่รู้ให้พูดว่า “ไม่รู้” หรือ
  “ยังไม่มีหลักฐาน” แล้วเสนอวิธีตรวจที่ปลอดภัย
- ห้ามแต่งชื่อ field/table/API/ผลลัพธ์ของ tool/ผลเทส/พฤติกรรม SAP ขึ้นมาเอง
- ทุกข้อกล่าวอ้างต้องมี evidence: file:line, command output, DDIC read, test result
- ถ้าเป็นการคาดเดา ให้ติดป้ายชัดว่า `Hypothesis` และบอกว่าจะพิสูจน์อย่างไร
- ถ้า tool/session ใช้งานไม่ได้ ให้รายงานตามจริง ห้ามแทนด้วยการเดาหรือ tool อื่นเงียบ ๆ
- SAP on-demand เท่านั้น: ห้ามเชื่อม SAP ตอนเปิด session
- ห้ามเก็บ password/token ลงไฟล์ทุกกรณี
- SAP write/activate/transport ต้องมี target + transport ที่ชัดเจนและได้รับอนุมัติ
- ห้ามแก้ vendor agents/skills ที่ download มา
- แก้ได้เฉพาะไฟล์ที่ลงท้าย `-by-pongg` และไฟล์ใหม่ที่สร้างเอง
- ก่อนแก้ agent/skill เดิม: เสนอ + รออนุมัติ
- ระวังภาษาไทยเพี้ยน (mojibake) เมื่ออ่าน/เขียนผ่าน PowerShell

## Working habits

- ใช้ `memory/` ต่อโปรเจกต์ + `reports/DECISIONS.md` สำหรับงานยาว
- ชอบroot cause ไม่ใช่ patch อาการ
- ชอบทดสอบกับของจริง (SAP runtime, Z-table, ALV) ไม่ใช่แค่ syntax ผ่าน
- ชอบให้สรุปเป็นขั้นตอน test ที่ทำตามได้
- ถ้า pattern เกิดซ้ำ ≥2 ครั้ง ค่อยเสนอทำเป็น skill

## Environment

- Windows, OpenCode, GitHub Copilot, Claude Code, Codex
- SAP DEV: client 100 (ADT) และ client 900 (SAP GUI)
- MCP หลัก: ADT/SAP AI Dev Toolkit, SAP GUI, ARC-1, browser, open-computer-use
- Vendor agents: 7 ตัวใน OpenCode + 7 ตัวใน Copilot (ห้ามแก้)
- Personal agents: 4 ตัวใน Copilot ที่ลงท้าย `-by-pongg` (แก้ได้)
- OpenCode ยังไม่มี personal agent — ถ้าต้องการให้สร้างใหม่เป็น `*-by-pongg.md`

## Pet peeves

- คำตอบยาวเกินจำเป็น
- อธิบายซ้ำสิ่งที่ผู้ใช้บอกไปแล้ว
- ใช้ tool ซ้ำซ้อน/เรียกหลายตัวเพื่อเรื่องเดียวกัน
- แก้ไฟล์ vendor โดยไม่ถาม
- ภาษาไทยใน source เปลี่ยนเป็น mojibake
