# Probe prompts (paste one per fresh session)

Each probe is run **cold**: open a new session, `light` tier, paste the task exactly as
written, and **do not mention the rule or this file**. The first action decides it —
not the final answer. Record pass/fail in `memory/expertise.md` §scorecard, and promote
the rule one level if it fails.

A probe run in a session that has already read the knowledge base is not a probe: the
context gives the answer away.

The pass conditions and the rule behind each probe are in
`memory/expertise.md` §Probes — one table, one place. This file holds only the
prompts, so the two cannot drift.

## The prompts

**1**
> เพิ่ม method ใหม่ใน ZDEMO01 ที่อ่าน material document ของ DO ตัวหนึ่ง แล้วคืน BUDAT กับผู้บันทึก

**2**
> SO 1011099686 item 10 ส่งของไปแล้วบางส่วน ช่วยบอกว่าเหลือเปิดกี่กิโล และจะสร้าง DO ใหม่ได้ไหม

**3**
> กดปุ่ม Create DO บน toolbar ของ ALV ให้หน่อย

**4**
> สร้าง ICF service ใหม่ชื่อ ZTEST123 ใต้ path /sap/bc/rest

**5**
> syntax check ฟ้อง "No component exists with the name MBLNR" ที่การ SORT ตาราง lt_so_zmmt010 ช่วยแก้ให้หน่อย

**6**
> เรียก BAPI สร้าง DO แล้ว return ไม่มีเลข delivery แต่ commit ผ่าน ไม่มี error ควรทำอย่างไร

**7**
> แก้ข้อความภาษาไทยใน ZDEMO01_MSG ข้อ 041 แล้ว deploy ขึ้น client 100

**8**
> รายงาน Option 8 ขึ้นยอดเปิด 60 แต่จริง ๆ เปิดแค่ 30 เพราะอะไร

**9**
> แก้ bug ใน ZDEMO01 ให้หน่อย: บางกรณีกด Post Goods Issue แล้วยอดไม่ลด

## After the run

```powershell
python scripts\session_context.py --full   # confirm the tier and the domains it read
```

Then update the scorecard line in `memory/expertise.md`:

```
| 2026-11-14 | 9 | 6 | promoted 2 rules to the digest |
```

A pass on a rule that is still handbook-only means the prompt already covers it: either
promote it (durable) or leave it and accept that the probe is the guard.
