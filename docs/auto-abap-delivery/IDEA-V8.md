# Idea Draft: SAP ABAP Agentic Development Operating Model

> สถานะ: **Concept / Idea Draft** สำหรับนำไปวิจารณ์ ทดลอง และปรับใช้ต่อ ไม่ใช่ข้อกำหนดสุดท้าย
>
> เป้าหมาย: ออกแบบ Agent และ Skill สำหรับบทบาท SAP ABAP Developer ให้ AI ช่วยทำงานได้มากที่สุด แต่ยังคงอยู่ภายใต้ขอบเขต หลักฐาน การตรวจสอบ และสิทธิ์ที่ควบคุมได้

## 1. Executive idea

แนวคิดหลักไม่ใช่ “ให้ AI เขียน ABAP เร็วที่สุด” แต่คือ “สร้างระบบงานที่ทำให้ AI เดินงานได้เองอย่างมีวินัย ตั้งแต่รับ requirement จนส่งมอบหลักฐานการทดสอบ”

สิ่งที่ควรยืมจากแนวคิด pstack คือ:

1. มี **playbook แยกตามชนิดงาน** แทน prompt เดียวที่พยายามครอบคลุมทุกกรณี
2. มี **verification skill ของ repo และ SAP landscape นี้โดยเฉพาะ**
3. งานจะถือว่าเสร็จเมื่อมีหลักฐาน ไม่ใช่เมื่อ AI บอกว่าเสร็จ
4. ถ้าตรวจสอบไม่ได้ ให้รายงานว่า `INCONCLUSIVE` หรือ `BLOCKED` แทนการเดา
5. ใช้ checkpoint และไฟล์สถานะเพื่อให้งาน long-run ไม่หลุด scope เมื่อ context ถูกตัดหรือเริ่ม session ใหม่

## 2. สิ่งที่ควรเพิ่มลงในสอง repo

แนวทางที่แนะนำคือให้ทั้งสอง repo ใช้ **workflow contract เดียวกัน** แต่มี adapter ต่างกัน

- `abap-ai-opencode-toolkit`: เก็บ implementation สำหรับ OpenCode เช่น commands, agents, hooks และ tool routing
- `abap-copilot-kit`: เก็บ implementation สำหรับ GitHub Copilot เช่น `.agent.md`, `SKILL.md`, prompt files และ VS Code instructions
- แยกแกนกลางที่เป็นกลางต่อ host ไว้ใน `shared/` หรือสร้าง repo กลางอีกหนึ่ง repo แล้ว sync เข้าแต่ละ toolkit

โครงสร้างที่เสนอ:

```text
shared/
  contracts/
    task-state.schema.json
    evidence.schema.json
    tool-capability.schema.json
  playbooks/
    new-program.md
    change-request.md
    bug-fix.md
    refactor.md
    emergency-fix.md
  templates/
    draft-spec.md
    implementation-plan.md
    test-plan.md
    handoff.md
    changelog-entry.md
  policies/
    sap-system-safety.md
    write-gates.md
    evidence-policy.md
    production-policy.md
```

**เหตุผล:** ถ้าแยก logic ตาม host ตั้งแต่ต้น สอง repo จะ drift เร็วมาก ควรให้ host-specific agent เป็นเพียง adapter ส่วน state machine, quality gates, artifact format และ safety contract ใช้ชุดเดียวกัน

## 3. Agent architecture: ทีมเสมือนแบบมี Coordinator

ไม่แนะนำให้ agent ทุกตัวแก้ source ได้ทั้งหมด เพราะจะทำให้ ownership ไม่ชัดและ audit ยาก ควรใช้ coordinator หนึ่งตัว และ specialist agent หลายตัว

### 3.1 ABAP Delivery Lead Agent

หน้าที่:

- รับงานและจำแนกเป็น New Program, Change Request, Bug Fix, Refactor หรือ Investigation
- ตรวจสอบข้อมูลก่อนเริ่มงาน
- เรียก Tool Capability Audit
- ทำ Grill-Me interview
- สร้าง Draft Spec, plan และ task ledger
- กระจายงานให้ specialist
- เป็นเจ้าของ scope และสถานะรวม
- ขออนุมัติเฉพาะจุดที่มีความเสี่ยงหรือ irreversible

ข้อห้าม:

- ห้ามเขียน code ก่อน requirement gate ผ่าน
- ห้ามอ้างว่าทดสอบสำเร็จ ถ้าไม่มี evidence artifact
- ห้ามเปลี่ยน system, client, package, transport หรือ target object จากค่าที่ผู้ใช้ยืนยัน

### 3.2 Requirement Analyst Agent

หน้าที่:

- ถามคำถามแบบ Grill-Me
- อ่าน Functional Spec, PRD, ticket, source เดิม และตัวอย่างข้อมูล
- สรุป business rule, acceptance criteria, negative case และ non-goal
- ระบุ assumption และ unresolved question อย่างชัดเจน

### 3.3 Reverse Engineer / Impact Analyst Agent

ใช้กับโปรแกรมเดิมหรือ Change Request:

- fresh-read source จาก SAP
- ดึง dependency, where-used, DDIC/CDS/RAP relationship
- แยก observed fact ออกจาก inference
- ทำ impact map ก่อนแก้ไข
- ตรวจ lock, inactive version, transport ownership และ source drift

ค่าเริ่มต้นควรเป็น read-only

### 3.4 ABAP Developer Agent

- implement ทีละ vertical slice
- syntax check และ activate เฉพาะ object ที่อยู่ใน approved plan
- ไม่ขยาย scope เอง
- บันทึก changed object, reason และ diff summary ทุกครั้ง
- pause เมื่อพบ requirement ambiguity หรือพบผลกระทบเกิน scope

### 3.5 ABAP Test Engineer Agent

- สร้าง test matrix จาก acceptance criteria
- ใช้ ABAP Unit, CDS Test Double Framework, SQL Test Double Framework, Function Module Test Double Framework หรือ RAP transactional buffer doubles ตามชนิดงาน
- กรณีไม่มี test double ที่เหมาะสม ให้สร้าง deterministic internal-table fixture ใน local test class แทนการสร้าง Z test program แบบถาวรโดยอัตโนมัติ
- ถ้าต้องอาศัยข้อมูลจริง ให้ query แบบ read-only, จำกัดจำนวนแถว, mask ข้อมูลสำคัญ และบันทึก query/evidence
- ทำ regression test สำหรับพฤติกรรมเดิมที่ต้องคงอยู่

### 3.6 Quality Auditor Agent

- review diff เทียบ spec และ non-goal
- ตรวจ syntax, activation, ABAP Unit, ATC/SCI, authorization, performance และ clean-core compatibility ตาม landscape
- ตรวจว่าหลักฐานใหม่กว่า source revision ล่าสุด
- ห้าม auditor ใช้ผลสรุปจาก developer อย่างเดียว ต้องอ่าน evidence และ diff โดยตรง

### 3.7 Documentation & Handoff Agent

- update Draft Spec เป็น As-Built Spec
- เพิ่ม changelog
- สรุป objects changed, transport, test evidence, known limitation และ manual UAT steps
- สร้างข้อความแจ้งผู้ใช้ว่า AI validation ครบส่วนใด และส่วนใดยังต้อง UAT โดยผู้ใช้

## 4. ใช้ Playbook ไม่ใช้ Mega-Agent อย่างเดียว

ควรมี router ที่เลือก playbook ตามงาน:

| Work type | Playbook | Stop condition สำคัญ |
|---|---|---|
| New Program | `new-program` | ไม่มี package, transport, naming rule, input/output หรือ acceptance criteria |
| Change Request | `change-request` | impact map ไม่ครบ หรือ compatibility behavior ไม่ชัด |
| Bug Fix | `bug-fix` | reproduce ไม่ได้ หรือไม่มี evidence ของปัญหาก่อนแก้ |
| Refactor | `refactor` | ไม่มี characterization test ของ behavior เดิม |
| Emergency Fix | `emergency-fix` | target เป็น PRD, ไม่มี approver หรือ rollback plan |

Router ต้องเลือกจาก evidence ไม่ใช่แค่ keyword เช่นคำว่า “แก้โปรแกรม” อาจเป็น bug fix, CR หรือ refactor ก็ได้

## 5. Tool Capability Audit: ต้องตรวจเครื่องมือจริงก่อนทำงาน

ตรงนี้ควรเป็น mandatory preflight ไม่ใช่ best effort

### 5.1 สิ่งที่ต้องตรวจ

1. MCP server ใดถูก register อยู่จริง
2. tool name และ schema ที่ host มองเห็นจริง
3. tool เป็น read-only, write, destructive หรือ execution
4. เชื่อมต่อ SAP destination ใด, SID/client ใด
5. user/authorization คืออะไร
6. รองรับ object type ที่ต้องใช้หรือไม่
7. ทำ lock/edit/activate/test/ATC/diff ได้จริงหรือไม่
8. policy เช่น `readOnly`, allowed package/transport และ data preview เปิดหรือปิด
9. health check ผ่านหรือไม่
10. tool manifest เปลี่ยนจากครั้งก่อนหรือไม่

### 5.2 Capability matrix ที่ควรสร้างทุก session

```yaml
capability_snapshot:
  captured_at: 2026-11-20T12:00:00+07:00
  target:
    system: DEV
    client: "100"
  capabilities:
    read_source: available
    where_used: available
    edit_source: approval_required
    activate: available
    abap_unit: available
    atc: available
    table_preview: denied
    transport_release: denied
  evidence:
    - tool-discovery-output.json
    - healthcheck-output.json
```

ห้ามใช้รายการ tool จากเอกสารหรือ memory อย่างเดียว ต้องตรวจ live tool surface ก่อนเริ่มงาน และ refresh เมื่อ session ใหม่, MCP restart, configuration hash เปลี่ยน หรือ tool call ตอบว่า unknown/unsupported

## 6. Grill-Me Gate ก่อนเขียนโค้ด

ควรถามเป็นรอบ ไม่ถาม 30 ข้อในครั้งเดียว

### รอบ A: Business outcome

- ปัญหาปัจจุบันคืออะไร ใครได้รับผลกระทบ
- ผลลัพธ์ที่ถูกต้องหน้าตาอย่างไร
- ตัวอย่าง input/output ที่คาดหวัง
- acceptance criteria และกรณีที่ต้อง reject

### รอบ B: SAP context

- SID/client และ environment
- object ใหม่หรือของเดิม ใช้ชื่ออะไร
- package, software component, transport
- ABAP Platform/S/4HANA release และ ABAP Cloud restriction
- entry point: report, class, BAdI, enhancement, RAP, CDS, OData, job, IDoc, RFC หรือ form

### รอบ C: Data and security

- ตาราง/CDS/API ที่เกี่ยวข้อง
- ปริมาณข้อมูลโดยประมาณ
- authorization object และ sensitive fields
- ต้อง commit/update จริงหรือ simulation ได้
- ต้องรองรับ background, parallel processing หรือ retry หรือไม่

### รอบ D: Delivery and test

- backward compatibility
- expected unit/integration/UAT coverage
- ตัวอย่างข้อมูลจริงที่อนุญาตให้อ่าน
- performance target
- rollback requirement

เมื่อข้อมูลไม่ครบ Agent ต้องสร้าง Draft Spec ที่มี `TBD`, assumption และ decision request ห้ามเติมรายละเอียดเอง

## 7. Draft Spec as the source of truth

ไฟล์หลักที่เสนอ:

```text
work/<task-id>/
  00-intake.md
  01-draft-spec.md
  02-impact-analysis.md
  03-implementation-plan.md
  04-test-plan.md
  05-task-ledger.yaml
  06-evidence-index.md
  07-handoff.md
  CHANGELOG.md
  evidence/
```

หัวข้อหลักใน `01-draft-spec.md`:

- Context and problem
- Goal
- In scope
- Out of scope
- Current behavior
- Expected behavior
- Business rules
- Interfaces and data
- Authorization and security
- Performance and volume
- Acceptance criteria
- Test scenarios
- Assumptions
- Open questions
- Approved decisions
- Planned SAP objects
- Rollback approach

ควรใช้ spec hash หรือ revision ID เช่น `SPEC-R003` เพื่อให้รู้ว่า implementation และ evidence ถูกสร้างจาก spec เวอร์ชันใด

## 8. Long-run control เพื่อแก้ปัญหา context window

หัวใจคือ **externalized state** ไม่ฝากความจำไว้ใน conversation

`05-task-ledger.yaml` ควรมี:

```yaml
task_id: ABAP-CR-2026-014
spec_revision: SPEC-R003
status: implementing
current_slice: S03
target:
  system: DEV
  client: "100"
  package: ZPKG_APP
  transport: DEVK900123
scope_guard:
  allowed_objects:
    - ZCL_ORDER_SERVICE
  prohibited:
    - database-schema-change
    - production-write
completed:
  - S01-reproduce
  - S02-impact-analysis
next:
  - implement-null-check
  - run-unit-tests
blocked: []
last_verified_source_hash: sha256:...
latest_evidence_id: EV-0018
```

ทุก slice ต้องจบด้วย checkpoint:

1. ทำอะไรไป
2. object/diff ใดเปลี่ยน
3. validation อะไรผ่าน/ไม่ผ่าน
4. evidence อยู่ไหน
5. spec revision ใด
6. ขั้นตอนถัดไป
7. ต้องถามผู้ใช้หรือไม่

หาก resume หลัง context reset ให้เริ่มจาก ledger + spec + evidence index แล้ว fresh-read SAP source เพื่อหาความต่าง ห้าม resume จาก summary เพียงอย่างเดียว

## 9. Incremental development loop

เสนอ loop ต่อหนึ่ง vertical slice:

1. **Select slice**: เลือก acceptance criterion ขนาดเล็กหนึ่งชุด
2. **Fresh read**: อ่าน source และ dependency ล่าสุด
3. **Precondition check**: system/client/object/lock/hash/transport
4. **Implement**: แก้เฉพาะ scope ของ slice
5. **Static validation**: syntax + activation
6. **Focused test**: unit/test double/internal-table fixture
7. **System cross-check**: query/read-only integration check ถ้าจำเป็น
8. **Independent review**: Auditor ตรวจ diff + evidence
9. **Checkpoint**: update ledger/spec/changelog
10. **Proceed or stop**: ไป slice ถัดไปเฉพาะเมื่อ gate ผ่าน

ไม่ควรพยายามเขียนทั้งหมดแล้วค่อย ATC ตอนท้าย เพราะ root cause จะย้อนหาได้ยากและ evidence จะปนกันหลาย change

## 10. Testing strategy แบบหลายชั้น

### Level 0: Compile evidence

- syntax check
- activation result
- inactive object check

### Level 1: Deterministic unit test

- local test class
- internal-table fixtures
- seam/interface injection
- ABAP OO Test Double Framework
- SQL/CDS/FM/AMDP test doubles ตาม dependency

ตัวอย่าง test dataset ควรมีอย่างน้อย:

- happy path
- empty input
- duplicate key
- boundary date/amount
- unauthorized or invalid status
- large-volume representative set
- regression case ของ defect เดิม

### Level 2: Read-only system cross-check

- query ข้อมูลจริงตัวอย่างแบบจำกัด row count
- เปรียบเทียบ expected calculation กับผลจริง
- ไม่เปลี่ยน application data
- บันทึก timestamp, selection/filter และ data fingerprint

### Level 3: Integration validation

- service binding/OData preview
- RAP behavior/action
- job execution หรือ controlled transaction flow
- ต้องระบุ rollback และ authorization ก่อนรัน

### Level 4: Quality gates

- ATC/SCI
- priority 1/2 findings ต้องเป็น fail gate โดยค่าเริ่มต้น
- priority 3 ต้องมี disposition: fix, accepted risk หรือ not applicable
- performance trace เมื่อ logic แตะข้อมูลมากหรือมี nested access

### Level 5: Human UAT

AI แจ้งให้ผู้ใช้ทดสอบ scenario ที่ต้องใช้ business judgment พร้อม step, test data และ expected result ไม่ใช่เพียงบอกว่า “กรุณาทดสอบ”

## 11. Evidence contract

คำว่า Done ต้องอ้างถึง evidence อย่างน้อย:

```yaml
evidence:
  id: EV-0018
  task_id: ABAP-CR-2026-014
  spec_revision: SPEC-R003
  source_revision: sha256:...
  target: DEV/100
  object: ZCL_ORDER_SERVICE
  checks:
    syntax: passed
    activation: passed
    abap_unit: 12/12 passed
    atc: 0 priority-1, 0 priority-2, 2 priority-3 reviewed
  captured_at: 2026-11-20T12:30:00+07:00
  limitations:
    - end-to-end invoice posting requires business UAT
```

Evidence ต้องหมดอายุถ้า source hash, spec revision, target system/client หรือ relevant dependency เปลี่ยน

## 12. Safety and approval model

### Auto-permitted

- read source/metadata
- search/where-used
- generate local draft documents
- syntax analysis ที่ไม่เปลี่ยน SAP
- query test doubles/local fixtures

### Execute with policy and recorded approval

- create/edit/activate SAP object
- run test ที่อาจมี side effect
- create transport
- apply ATC quick fix
- preview business data

### Always human-controlled

- production write
- transport release/import
- destructive delete
- mass data correction
- security/authorization change
- external outbound call ที่มีผลธุรกิจ

Agent ต้องตรวจ permission จาก live tool policy ไม่ใช่สมมติจากชื่อ tool

## 13. Changelog และ decision log

แยกสองอย่าง:

- `CHANGELOG.md`: เปลี่ยนอะไรใน deliverable
- `DECISIONS.md`: ทำไมจึงเลือกแนวทางนี้ ทางเลือกใดถูกปฏิเสธ

รายการ changelog ที่ดี:

```text
### 2026-11-20 - SPEC-R003 / Slice S03
- Changed: เพิ่ม validation เมื่อ delivery quantity มากกว่า open quantity
- Objects: ZCL_SO_DELIVERY_VALIDATOR
- Reason: AC-07
- Tests: UT-07A, UT-07B, REG-02 passed
- Evidence: EV-0018
- Risk: No database schema or interface change
```

## 14. Definition of Done

งานจะเป็น `DONE` เมื่อ:

- spec ไม่มี unresolved blocker
- ทุก acceptance criterion map ไปยัง implementation และ test evidence
- source ที่ทดสอบตรงกับ source hash ปัจจุบัน
- syntax/activation ผ่าน
- unit/regression test ผ่าน
- ATC gate ผ่านหรือมี approved disposition
- changelog และ as-built document update แล้ว
- manual UAT package พร้อม
- known limitation และ rollback ระบุชัด

หาก AI ตรวจ integration ไม่ได้ ให้สถานะ `READY_FOR_UAT` ไม่ใช่ `DONE`

## 15. แนวคิดเพิ่มเพื่อไม่ให้ multi-agent กลายเป็น overhead

### 15.1 ใช้ virtual roles ไม่จำเป็นต้อง spawn agent ทุกครั้ง

งานเล็กอาจให้ Coordinator ทำหลาย role ตามลำดับ แต่ต้องแยก artifact และ review pass ส่วนงานใหญ่จึงค่อย delegate จริง

### 15.2 Risk-based depth

- `LOW`: comment, text, isolated calculation มี unit test
- `MEDIUM`: business logic, CDS, BAdI, report selection
- `HIGH`: posting, update task, authorization, integration, transport/release

ระดับความเสี่ยงเป็นตัวกำหนดจำนวนคำถาม, reviewer, test layer และ approval gate

### 15.3 Separate evidence from narrative

ให้ผล tool เก็บเป็น JSON/YAML และสร้าง Markdown summary ภายหลัง ช่วยลด hallucination และสามารถ rerun comparison ได้

### 15.4 Stop-the-line policy

หยุดทันทีเมื่อ:

- system/client ไม่ตรง
- object ถูก lock โดยผู้อื่น
- source hash เปลี่ยนหลัง approval
- transport ไม่ตรงหรือไม่มีสิทธิ์
- reproduce bug ไม่ได้
- requirement conflict
- test มี side effect ที่ยังไม่อนุมัติ
- tool capability ที่จำเป็นไม่พร้อม

### 15.5 Budget and loop guard

- จำกัด repair loop ต่อ slice เช่น 3 รอบ
- หาก error signature เดิมเกิดซ้ำ 2 รอบ ให้เปลี่ยน hypothesis หรือ escalate
- ห้าม rerun check เดิมโดยไม่มี source/config/evidence เปลี่ยน
- บันทึก `attempt`, `hypothesis`, `change`, `result` ป้องกัน recheck ซ้ำ

## 16. Skills ที่ควรสร้างก่อน

ลำดับ MVP ที่แนะนำ:

1. `abap-tool-surface-audit`
2. `abap-work-intake-grill`
3. `abap-draft-spec`
4. `abap-task-ledger`
5. `abap-change-impact`
6. `abap-slice-implementation`
7. `abap-verification`
8. `abap-evidence-pack`
9. `abap-handoff`
10. playbook router สำหรับ New / Change / Bug / Refactor

ไม่ควรเริ่มจาก mega-skill ที่รวมทุกอย่าง เพราะจะกิน context, debug ยาก และ reuse ต่ำ

## 17. ตัวอย่างคำสั่งใช้งาน

```text
เริ่มงาน Change Request สำหรับ ZCL_SO_ALLOCATION ใน DEV/100
ยังไม่มี Functional Spec ให้ทำ Grill-Me ก่อน
ห้ามแก้ source จนกว่าฉันจะ approve Draft Spec
หลัง approve ให้ implement ทีละ slice, run ABAP Unit และ ATC
ทุก checkpoint ให้ update task ledger และ evidence index
ห้าม release transport
```

ผลที่คาดหวัง:

1. capability snapshot
2. คำถามรอบแรก
3. Draft Spec
4. impact analysis
5. implementation/test plan
6. approval checkpoint
7. incremental implementation
8. evidence pack
9. `READY_FOR_UAT` handoff

## 18. Roadmap

### Phase 1: Foundation

- shared contracts
- tool-surface audit
- Grill-Me + Draft Spec
- task ledger + checkpoint
- New/Change/Bug playbooks

### Phase 2: Verification

- ABAP Unit/ATC adapters
- evidence schema
- source hash/freshness rules
- test fixture generator
- auditor agent

### Phase 3: Controlled autonomy

- host-specific routing สำหรับ OpenCode และ Copilot
- resumable execution
- loop guards
- risk-based approvals
- automatic handoff generation

### Phase 4: Learning loop

- capture failure patterns
- maintain verification skill เมื่อ tool/system เปลี่ยน
- metrics: lead time, first-pass test rate, rework count, repeated-check count, blocked reasons
- promotable lessons: session finding -> reviewed project rule/skill update

## 19. ข้อสรุป

แนวคิดนี้ควรมองเป็น **ABAP Delivery Operating System สำหรับ AI** มากกว่า agent ตัวเดียว โดยมีสี่แกน:

1. **Spec before code**
2. **Live capability check before tool use**
3. **Small slice + verify + checkpoint**
4. **Evidence before Done**

จุดที่สำคัญที่สุดไม่ใช่จำนวน agent แต่คือ shared state, stop conditions, evidence freshness และการบังคับให้ทุกการเปลี่ยนแปลงย้อนกลับไปหา acceptance criterion ได้

## 20. แหล่งแนวคิดที่ใช้ประกอบ

- CodeSook, “pstack the right way”: แนวคิด playbook, verification skill, stop-the-line, checkpoint และ evidence-driven completion
- SAP Help Portal: ABAP Unit, test double frameworks และ ATC workflow
- MCP ABAP ADT projects: ตัวอย่าง live tool discovery, read/write policies, ABAP Unit, ATC, source diff และ audit-oriented guardrails
- Repo ของผู้ใช้และ companion repository: แนวทาง coordinator, read-only delegation, long-task control, MCP surface audit และ new-program scaffolding


---

# Extension V2: Explicit Auto ABAP Dev Mode

> ส่วนขยายนี้เพิ่มแนวคิดจาก `mattpocock/skills` และบทความ pstack ของ Nokka โดยออกแบบให้ workflow **ไม่ทำงานอัตโนมัติกับทุกคำขอ** แต่เริ่มทำงานเฉพาะเมื่อผู้ใช้เรียก Skill/Mode โดยชัดแจ้งเท่านั้น

## 21. หลักการเปิดใช้งาน: Explicit Invocation Only

Skill นี้ต้องเป็น **opt-in autonomous mode** ไม่ใช่ global coding rule

ชื่อที่เสนอ:

- Skill: `auto-abap-dev`
- Agent/Coordinator: `ABAP Auto Delivery Lead`
- Invocation examples:
  - `/auto-abap-dev start`
  - `Use auto-abap-dev for CR-1024`
  - `เปิด Auto ABAP Dev Mode สำหรับ ZCL_SO_ALLOCATION`

### 21.1 Trigger contract

Skill ทำงานเมื่อพบเงื่อนไขทั้งหมด:

1. ผู้ใช้เรียกชื่อ Skill/Mode โดยตรง
2. ผู้ใช้ระบุเป้าหมายงาน หรือยอมให้เริ่ม Intake เพื่อค้นหาเป้าหมาย
3. Agent แสดง Mode Banner ว่าโหมด autonomous ถูกเปิดแล้ว
4. ผู้ใช้ยืนยัน target system/client ก่อนเกิด SAP write ครั้งแรก

Skill ต้องไม่ถูก auto-trigger จากข้อความทั่วไป เช่น:

- “ช่วยดู class นี้หน่อย”
- “อธิบาย dump นี้”
- “เขียนตัวอย่าง ABAP”
- “คิดว่า logic นี้ถูกไหม”

กรณีเหล่านี้ใช้ normal assistant mode เท่านั้น เว้นแต่ผู้ใช้เรียก `/auto-abap-dev`

### 21.2 Session lease

การเปิดโหมดควรมี lease จำกัดขอบเขต:

```yaml
auto_mode:
  mode: auto-abap-dev
  lease_id: AUTO-2026-0014
  task_id: CR-1024
  status: active
  target: DEV/100
  expires_when:
    - ready_for_uat
    - user_cancels
    - blocked_requiring_business_decision
    - target_system_changes
    - 8_hours_without_checkpoint
```

Mode ปิดโดยอัตโนมัติเมื่อส่งมอบ `READY_FOR_UAT`, ผู้ใช้สั่งหยุด, เปลี่ยน target หรือพบ blocker ที่ต้องตัดสินใจเชิงธุรกิจ ห้ามให้ mode ค้างข้ามงานแล้วนำ autonomy ไปใช้กับคำขออื่น

## 22. สิ่งที่นำเพิ่มจาก Matt Pocock Skills

### 22.1 Small and composable skills

ไม่สร้าง Skill เดียวที่มี instruction หลายพันบรรทัด แต่ให้ `auto-abap-dev` เป็น orchestrator ที่เรียก Skill ขนาดเล็ก เช่น:

- `abap-grill-with-docs`
- `abap-build-glossary`
- `abap-diagnose-bug`
- `abap-impact-analysis`
- `abap-tdd`
- `abap-verify-slice`
- `abap-audit-delivery`
- `abap-prepare-uat`

ข้อดีคือแก้ failure mode รายจุดได้ และนำ Skill เดิมไปใช้ใน playbook อื่นได้

### 22.2 Grill with docs, not chat only

ระหว่าง Grill-Me ให้สร้างเอกสารจริงทันที:

- `GLOSSARY.md`: ภาษาร่วมของธุรกิจและ SAP object
- `DECISIONS.md`: การตัดสินใจและทางเลือกที่ไม่เลือก
- `01-draft-spec.md`: current/expected behavior
- `OPEN-QUESTIONS.md`: เฉพาะคำถามที่ค้นจาก repo/SAP ไม่ได้

Agent ต้องสำรวจ source, DDIC, CDS, where-used และเอกสารใน repo ก่อนถามผู้ใช้ เพื่อลดคำถามที่ AI ตอบเองได้จากหลักฐาน

### 22.3 TDD and disciplined diagnosis

สำหรับ Bug Fix:

1. Reproduce defect
2. Capture failing evidence
3. ตั้งสมมติฐานหลายข้อ
4. ตัดสมมติฐานด้วยหลักฐาน
5. เขียน regression test ที่ fail ก่อน
6. แก้ code ขั้นต่ำ
7. ทำให้ test ผ่าน
8. Refactor โดย behavior ต้องคงเดิม
9. Run wider regression และ ATC

สำหรับ New/Change Request ให้เริ่มจาก acceptance test หรือ unit-test scenario ของ slice ก่อน implementation เมื่อ architecture รองรับ

### 22.4 Shared language

ชื่อ method, class, test และเอกสารควรสอดคล้องกับ glossary ของโครงการ ลดการใช้คำหลายชุดกับ concept เดียว และช่วยให้ session ถัดไปอ่าน state ได้เร็วขึ้น

## 23. Auto ABAP Dev Tool เป็น bounded autonomy ไม่ใช่ blind autonomy

ผู้ใช้ทำหน้าที่ Project Owner:

1. เรียก mode
2. ตอบ Grill-Me
3. Approve Draft Spec และ autonomy envelope หนึ่งครั้ง
4. ปล่อย Agent ทำงานต่อเนื่อง
5. กลับมารับ UAT package
6. Feedback แล้วเปิด iteration ใหม่

Agent ทำงานแทนตั้งแต่ develop ถึง testing ได้ แต่ต้องอยู่ใน **autonomy envelope** ที่ผู้ใช้อนุมัติ

```yaml
autonomy_envelope:
  target:
    system: DEV
    client: "100"
  allowed_packages:
    - ZSD_APP
  allowed_transports:
    - DEVK900123
  allowed_objects:
    - ZCL_SO_ALLOCATION
    - ZCL_SO_ALLOCATION_TEST
  permitted_actions:
    - read
    - search
    - lock
    - edit
    - syntax_check
    - activate
    - run_abap_unit
    - run_atc
    - read_test_data
  prohibited_actions:
    - delete_object
    - release_transport
    - import_transport
    - production_write
    - mass_update
    - send_external_message
  data_policy:
    max_preview_rows: 100
    sensitive_fields: mask
  repair_budget:
    max_attempts_per_slice: 3
    max_same_error_repeats: 2
```

การกระทำที่อยู่ใน envelope ไม่ต้องถามซ้ำทุกครั้ง ส่วนสิ่งที่อยู่นอก envelope ต้องหยุดและขออนุมัติ

## 24. Front Door เดียวและ Router ภายใน

ผู้ใช้ควรจำคำสั่งเดียวคือ `/auto-abap-dev`

Coordinator ทำงานดังนี้:

1. Classify: New / Change / Bug / Refactor
2. เลือก playbook
3. แสดงเหตุผลที่เลือก
4. ใส่ทุกขั้นลง task ledger
5. ถ้าข้ามขั้น ต้องบันทึก `SKIPPED` พร้อมเหตุผล ห้ามหายไปเงียบ ๆ
6. เรียก Skill ย่อยตามขั้น

ตัวอย่าง:

```yaml
playbook_execution:
  selected: bug-fix
  reason: user reported existing behavior differs from expected result
  steps:
    - id: reproduce
      status: completed
      evidence: EV-0003
    - id: diagnose
      status: completed
      evidence: EV-0007
    - id: regression-test-red
      status: completed
      evidence: EV-0010
    - id: implement
      status: in_progress
    - id: verify
      status: pending
    - id: prepare-uat
      status: pending
```

## 25. Long-running autonomous state machine

```text
OFF
  -> INVOKED
  -> CAPABILITY_AUDIT
  -> INTAKE_AND_GRILL
  -> SPEC_DRAFTED
  -> WAITING_SPEC_APPROVAL
  -> AUTONOMY_ENVELOPE_APPROVED
  -> IMPACT_ANALYSIS
  -> PLAN_READY
  -> IMPLEMENT_SLICE
  -> VERIFY_SLICE
  -> AUDIT_SLICE
  -> CHECKPOINT
       -> next slice: IMPLEMENT_SLICE
       -> recoverable failure: REPAIR_LOOP
       -> business ambiguity: BLOCKED
  -> FULL_REGRESSION
  -> FINAL_ATC_AND_AUDIT
  -> DOCUMENTATION
  -> READY_FOR_UAT
  -> OFF
```

Human checkpoint หลักมีเพียง:

- Spec + plan approval
- การเปลี่ยน autonomy envelope
- irreversible/high-risk action
- business ambiguity
- UAT feedback

สิ่งอื่นให้ Agent เดินต่อเองถ้ามี evidence และอยู่ใน envelope

## 26. Never block on human, but never guess business intent

เพื่อทำงานระยะยาว Agent แบ่งการตัดสินใจเป็นสามกลุ่ม:

### A. Reversible and inside envelope: ทำต่อได้

- แก้ source ใน object ที่อนุมัติ
- เพิ่ม local ABAP Unit test
- activate ใน DEV
- rerun focused test
- update Markdown/YAML artifacts

### B. Reversible but uncertain: เลือกทางปลอดภัยและบันทึก assumption

- ตั้งชื่อ private helper
- จัดโครงสร้าง test fixture
- refactor ภายในที่ interface ไม่เปลี่ยน

ถ้า assumption กระทบ acceptance criterion ต้องย้ายไปกลุ่ม C

### C. Business, irreversible or outside envelope: หยุด

- เปลี่ยน pricing/accounting rule
- เพิ่ม database field หรือ public API
- เปลี่ยน authorization
- release/import transport
- production data write
- ลบ object

## 27. Three loops of the Auto Mode

### Delivery loop

`Requirement -> Spec -> Plan -> Slice -> Test -> Audit -> Checkpoint`

### Repair loop

`Failure -> Classify -> New hypothesis -> Minimal change -> Rerun affected check`

ห้ามรัน check เดิมซ้ำถ้า source, test data, configuration หรือ hypothesis ไม่เปลี่ยน

### Learning loop

`Recurring failure -> Candidate lesson -> Evidence -> Human review -> Encode in script/schema/lint/skill`

บทเรียนใหม่ห้ามเขียนเข้า production skill เองทันที ให้สร้าง `lesson-candidate.md` รอ Project Owner approve เพื่อป้องกัน Agent สร้างกฎจากเหตุการณ์ครั้งเดียว

## 28. Verification Skill เฉพาะ SAP Landscape

ควรมี project-specific adapter บอกว่า Agent พิสูจน์งานอย่างไร เช่น:

```yaml
verification_profile:
  object_types:
    CLAS:
      static_checks:
        - syntax_check
        - activate
      focused_tests:
        - abap_unit_class
      quality:
        - atc_object
    DDLS:
      static_checks:
        - syntax_check
        - activate
      focused_tests:
        - cds_test_double
      quality:
        - atc_object
    BDEF:
      static_checks:
        - validate_behavior
        - activate
      focused_tests:
        - rap_transactional_buffer_test
      quality:
        - validate_service_binding
```

Verification profile ต้องสร้างจาก MCP tool surface ที่ตรวจพบจริง ถ้าไม่มี tool สำหรับขั้นใด ให้ mark `UNAVAILABLE` และปรับสถานะสุดท้ายเป็น `READY_FOR_MANUAL_TEST` หรือ `INCONCLUSIVE` ตามผลกระทบ

## 29. Agent Team Execution Model

เพื่อไม่ให้หลาย Agent แก้ source ชนกัน:

- Delivery Lead เป็นเจ้าของ ledger และ scope
- Analyst, Reverse Engineer, Tester และ Auditor ใช้ read-only โดยค่าเริ่มต้น
- Developer เป็น writer หลักเพียงหนึ่งตัวต่อ object
- Test Engineer เขียนเฉพาะ test include/test class ที่มอบหมาย
- Auditor ห้ามแก้ production code แต่ส่ง finding กลับเข้า repair queue
- Coordinator ตรวจ lock และ source hash ก่อนทุก write

ใช้ fresh context สำหรับ specialist หาก host รองรับ แต่ต้องส่ง bounded task packet ไม่ส่ง conversation ทั้งหมด:

```yaml
task_packet:
  role: quality-auditor
  objective: audit slice S04
  spec_revision: SPEC-R004
  allowed_reads:
    - ZCL_SO_ALLOCATION
    - evidence/EV-0021.json
  expected_output:
    - findings.yaml
    - verdict
  prohibited:
    - source_write
    - scope_change
```

## 30. UAT Handoff Package

เมื่อ Auto Mode จบ ผู้ใช้ควรได้รับ package ที่ review ได้ในครั้งเดียว:

- Executive summary
- Spec revision และ autonomy envelope ที่ใช้
- Changed SAP objects
- Before/after behavior
- Acceptance criteria traceability
- ABAP Unit result
- ATC result
- System data cross-check result
- Known limitations
- Unverified areas
- Exact UAT scenarios
- Test data หรือวิธีหา test data
- Expected result ต่อ scenario
- Transport และ deployment status
- Rollback instructions
- Evidence index

สถานะสุดท้าย:

- `READY_FOR_UAT`: AI checks ที่วางแผนไว้ผ่าน แต่ยังรอ business UAT
- `READY_FOR_MANUAL_TEST`: tool ไม่สามารถทำ integration validation บางส่วน
- `BLOCKED`: ต้องการ decision/access/tool
- `FAILED_SAFE`: เกิน repair budget และหยุดโดยไม่ขยาย scope

## 31. Recommended initial implementation

เริ่มจากสิ่งที่ใช้งานจริงได้ก่อน:

### Release A: Controlled Auto Mode

- explicit invocation gate
- capability audit
- Grill-Me + Draft Spec
- one-time autonomy envelope approval
- New / Change / Bug router
- task ledger
- slice loop
- ABAP Unit + ATC evidence
- UAT handoff

### Release B: Resumable Bot

- session lease
- source/evidence hash
- fresh-context specialist packets
- repair budget and loop detection
- evidence freshness invalidation

### Release C: Self-improving with approval

- lesson candidates
- failure-pattern metrics
- proposed skill patches
- verification-profile maintenance
- Project Owner approval before promotion

## 32. Recommended Skill boundary

`auto-abap-dev/SKILL.md` ควรเล็กและทำหน้าที่ control plane:

- enforce explicit invocation
- initialize/resume lease
- route playbook
- enforce gates
- load only the reference needed for the current state
- write checkpoint before context-heavy transitions

รายละเอียดควรแยกไปที่:

```text
auto-abap-dev/
  SKILL.md
  references/
    state-machine.md
    invocation-contract.md
    autonomy-envelope.md
    capability-audit.md
    grill-and-spec.md
    new-program-playbook.md
    change-request-playbook.md
    bug-fix-playbook.md
    refactor-playbook.md
    verification.md
    testing.md
    evidence-contract.md
    uat-handoff.md
  scripts/
    init-workspace.py
    validate-ledger.py
    validate-evidence.py
    detect-stale-evidence.py
    build-uat-pack.py
  assets/
    templates/
```

## 33. Updated core position

Auto ABAP Dev Tool ที่เหมาะสมไม่ใช่ Agent ที่ “มีสิทธิ์ทำทุกอย่าง” แต่เป็น Agent ที่:

- เริ่ม autonomy เฉพาะเมื่อผู้ใช้เรียก
- ได้ขอบเขตและสิทธิ์เป็น lease ต่อหนึ่งงาน
- เดินงานเองได้โดยไม่ถามเรื่องเล็กซ้ำ ๆ
- หยุดเฉพาะ business decision, irreversible action หรือสิ่งนอก scope
- แสดงหลักฐานทุกขั้น
- ส่งมอบที่ `READY_FOR_UAT`
- ล้าง autonomy เมื่อจบงาน

นี่ทำให้ผู้ใช้ทำหน้าที่เหมือน Project Owner จริง คือกำหนด outcome และ guardrails แล้วรอรับ UAT package แทนการต้องเฝ้า Agent ทุก tool call

## 34. Additional idea sources

- Matt Pocock, `skills`: small composable skills, Grill-Me/Grill-with-Docs, shared glossary, TDD, disciplined bug diagnosis และ feedback loops
- Nokka, DEV Community pstack series: front door เดียว, playbook routing, skipped-step visibility, reversible-vs-irreversible decisions, verification skill ต่อโครงการ และการเปลี่ยนความผิดพลาดซ้ำให้เป็นบทเรียนใน structure

---

# Extension V3: Autonomous ABAP Engineering Loop and Dynamic Agent Team

> เป้าหมายของส่วนนี้คือทำให้ AI ไม่เพียงเขียน source แต่ต้องออกแบบ test, ทดสอบงานตัวเอง, วิจารณ์ผลลัพธ์, ซ่อมข้อผิดพลาด และเลือกโครงสร้างทีมย่อยให้เหมาะกับชนิดและความเสี่ยงของ SAP development object ในแต่ละงาน

## 35. หลักการ: No Untested Change

ทุก production-code change ต้องมี verification plan ก่อนแก้ source และมี evidence หลังแก้ source การ activate ผ่านไม่เท่ากับ logic ถูกต้อง

Agent ต้องสร้าง `change-to-test traceability`:

```yaml
change_test_trace:
  - acceptance_criterion: AC-07
    changed_objects:
      - ZCL_SO_ALLOCATION
    risks:
      - open_quantity_below_zero
      - duplicate_delivery_reference
    tests:
      - UT-07-normal
      - UT-07-boundary-zero
      - UT-07-duplicate
      - REG-03-partial-delivery
    evidence:
      - EV-0041
```

ถ้า object ไม่สามารถทำ automated unit test ได้ Agent ต้องสร้าง verification ที่ใกล้เคียงที่สุด และรายงาน residual risk ห้ามละเว้นการทดสอบแบบเงียบ ๆ

## 36. Dynamic Team Planner

Coordinator สามารถกำหนดจำนวน sub-agent เอง แต่ต้องพิจารณาจาก work profile ไม่ใช่สร้างหลาย agent เพื่อความดูดี

### Input สำหรับ Team Planner

- ประเภทงาน: New, Change, Bug, Refactor, Migration
- SAP landscape: ECC, S/4HANA, ABAP Cloud
- object types และ dependency breadth
- Clean Core impact
- authorization/security impact
- data mutation และ financial impact
- integration boundaries
- data volume/performance risk
- testability
- parallelizable workstreams
- MCP/tool capabilities ที่มีจริง

### Suggested team sizes

#### Small: 1 coordinator, no spawned sub-agent

ใช้เมื่อ:

- object เดียว
- isolated calculation
- dependency ต่ำ
- ไม่มี database update หรือ external interface
- test fixture สร้างได้ง่าย

Coordinator สลับ role ภายในตามลำดับ: Developer -> Tester -> Reviewer แต่ต้องใช้ review pass แยกจาก implementation pass

#### Medium: 3 roles

- Delivery Lead / Developer
- Test Engineer
- Independent Auditor

ใช้กับ report, class, CDS หรือ BAdI ที่มี business rule หลายกรณี หรือแตะข้อมูลจริงแต่ไม่มี high-risk posting

#### Large: 5-7 roles

- Delivery Lead
- Requirement/Functional Analyst
- SAP Solution & Clean Core Architect
- ABAP Developer หนึ่งคนต่อ workstream
- Test Engineer
- Integration/Performance Specialist
- Quality Auditor

ใช้เมื่อมี RAP BO, OData/API, multiple object types, posting/update, migration, authorization หรือ cross-system integration

### Guardrail

- หนึ่ง production object มี writer ได้ครั้งละหนึ่ง agent
- Auditor ห้ามแก้ production source
- Tester ห้ามเปลี่ยน expectation เพื่อทำให้ test ผ่าน
- Developer ห้ามลบ/ลด assertion โดยไม่มี approval
- จำนวน agent สูงสุดควรถูกจำกัด เช่น 7 active roles และลดเหลือ role เดียวเมื่อ task ไม่สามารถ parallelize ได้

## 37. Team Plan Artifact

ก่อนเริ่มงาน Coordinator สร้าง:

```yaml
team_plan:
  task_id: CR-1024
  complexity: high
  risk_score: 78
  selected_roles:
    - role: delivery-lead
      mode: coordinator
    - role: sap-architect
      mode: read_only
    - role: abap-developer
      owns:
        - ZBP_I_SALESALLOC
        - ZCL_SALESALLOC_SERVICE
    - role: test-engineer
      owns:
        - local_test_classes
        - cds_test_fixtures
    - role: auditor
      mode: read_only
  omitted_roles:
    - role: performance-specialist
      reason: expected volume below threshold and no nested database access
  parallel_tracks:
    - impact_analysis
    - test_scenario_design
  sequential_gate:
    - implementation_after_spec_approval
```

ถ้าไม่มีระบบ sub-agent จริง ให้ Coordinator จำลอง role passes ด้วย fresh context packet และแยก output artifact เหมือนเป็นคนละ reviewer

## 38. Scenario Generator ต่อ Development Object

Test Engineer ต้องสร้าง scenario จาก 6 แหล่ง:

1. Acceptance criteria
2. Business invariants
3. Object-specific failure modes
4. Dependency behavior
5. Historical defect/regression cases
6. Boundary and malformed inputs

### Common scenario catalog

- Happy path
- Empty/initial value
- Minimum/maximum boundary
- Duplicate key
- Missing master data
- Invalid status transition
- Authorization denied
- Lock/concurrent update
- Partial success/partial delivery
- Currency and unit conversion
- Date/time zone and period boundary
- Decimal/rounding/overflow
- Reprocessing/idempotency
- External timeout/retry
- High data volume
- Commit/rollback failure
- Legacy behavior regression

## 39. Object-specific Test Strategy

### Class / Interface

- ABAP Unit local test class
- dependency injection
- ABAP OO Test Double Framework
- verify output, state and collaborator interaction

### Function Module / Function Group

- ABAP Unit wrapper or Function Module Test Double Framework เมื่อ release รองรับ
- exceptions, TABLES/CHANGING mutation, update-task behavior
- RFC serialization และ remote error case ถ้าเป็น RFC-enabled

### Executable Report

- แยก selection handling, data retrieval และ presentation ออกจากกัน
- unit test service/calculation classes
- test selection variants และ authorization
- validate background execution และ spool behavior ถ้าเกี่ยวข้อง

### CDS / DCL / Metadata Extension

- CDS Test Double Framework
- cardinality, association, filter, aggregation และ parameter tests
- authorization tests สำหรับ DCL
- analytical semantics และ currency/unit annotations

### RAP Business Object

- behavior/action/determination/validation tests
- transactional buffer double หรือ EML test
- draft/non-draft, lock, feature control, authorization และ failed/reported mapping
- save sequence, late numbering และ side effects

### DDIC Table / Structure / Data Element / Domain

- activation/dependency impact
- conversion and compatibility risk
- foreign key/search help/lock object behavior
- migration/data-conversion plan เมื่อเปลี่ยน persisted structure

### BAdI / Enhancement / Exit

- multiple implementation/filter scenarios
- caller context
- standard fallback
- behavior when enhancement is inactive
- S/4HANA and Clean Core relevancy

### OData / REST / SOAP / RFC / IDoc

- contract, serialization and mapping
- authentication/authorization
- timeout, retry and duplicate message
- idempotency
- error payload and application log
- no outbound call to real external system without allowance

### Forms and Output

- data provider unit tests
- template/interface consistency
- language, page break, empty field, long text and amount formatting
- rendered comparison/manual inspection evidence when automation is limited

### Background Job / Workflow

- scheduling parameters
- restartability
- duplicate execution
- status transition
- lock and commit behavior
- application log and notification

### AMDP / HANA-heavy logic

- AMDP Test Double Framework when supported
- NULL semantics, client handling, aggregation and precision
- representative-volume performance test
- explain plan/SQL trace only when tooling permits

## 40. Self-Testing Engineering Loop

ต่อหนึ่ง slice ใช้ loop แบบ Red -> Green -> Review -> Harden:

1. Read acceptance criterion and current source
2. Generate risk-based scenarios
3. Add characterization test for existing behavior when changing legacy code
4. Create failing test or capture failing reproduction
5. Implement minimum change
6. Run focused syntax/activation/test
7. Diagnose failure by evidence
8. Repair within budget
9. Run regression neighborhood
10. Run object-level ATC
11. Independent audit
12. Mutation challenge or adversarial review
13. Update evidence and checkpoint

### Repair loop rules

- รอบ 1: ตรวจ implementation defect
- รอบ 2: ตรวจ test data, dependency assumption และ test-double setup
- รอบ 3: reconsider design/hypothesis
- error signature เดิมซ้ำ 2 ครั้งโดยไม่มีการเปลี่ยน hypothesis ให้ stop and escalate
- ห้ามแก้ expected result เพื่อให้ test ผ่าน เว้นแต่ spec revision ได้รับ approval
- ห้าม suppress ATC finding โดยไม่บันทึก justification

## 41. Independent Self-Review

AI ผู้เขียน source ไม่ควรเป็นผู้ตัดสินสุดท้ายเพียง pass เดียว ให้ Auditor รับ bounded packet:

- approved spec revision
- diff
- current source hash
- test plan
- raw test/ATC evidence
- known assumptions

Auditor ตรวจ:

- scope compliance
- missing scenario
- false-positive test
- assertion quality
- untested branch
- authorization/security
- database access/performance
- Clean Core and released API usage
- backward compatibility
- evidence freshness

Auditor ตอบได้เฉพาะ `PASS`, `PASS_WITH_RISK`, `REWORK`, `INCONCLUSIVE`

## 42. Test Quality Controls

การมี test ไม่ได้แปลว่า test ดี ต้องตรวจเพิ่ม:

- test ต้อง fail กับ defect เดิมก่อนแก้ เมื่อทำได้
- assertion ต้องตรวจผลธุรกิจ ไม่ใช่เพียง `sy-subrc`
- test ต้อง deterministic และไม่ขึ้นกับเวลาหรือข้อมูลสุ่มโดยไม่ควบคุม
- test fixture ต้องเล็กและอ่านได้
- test ไม่แก้ productive/business data
- negative cases ต้องตรวจข้อความ/exception ที่คาดหวัง
- regression test ห้ามถูกลบหลัง bug fix
- coverage ใช้เป็น indicator ไม่ใช่เป้าหมายเดียว

### Mutation challenge แบบ lightweight

ก่อนปิด slice Auditor อาจถาม:

- ถ้ากลับเครื่องหมาย `>` เป็น `>=` test ใดจะจับได้
- ถ้าข้าม authorization check test ใดจะ fail
- ถ้าผลรวมไม่แปลงหน่วย test ใดจะ fail
- ถ้า external call ถูกส่งซ้ำ test ใดจะจับ idempotency

ไม่จำเป็นต้องแก้ source จริงเสมอไป หาก tool ไม่รองรับ แต่ต้องพิสูจน์ว่า test suite ตรวจ defect class สำคัญได้

## 43. Cross-check กับ SAP System Data

หลัง unit test ผ่าน ถ้า autonomy envelope อนุญาต:

- query production-like data จาก DEV/QAS แบบ read-only
- จำกัด row count
- mask sensitive fields
- บันทึก selection/filter และ data fingerprint
- เปรียบเทียบกับ independently calculated expected result
- ห้ามใช้ข้อมูลจริงแทน unit test เพราะข้อมูลจริงอาจไม่ครอบคลุม edge case

ระบบจริงใช้ยืนยัน integration assumptions ส่วน test double ใช้ยืนยัน deterministic business logic ทั้งสองอย่างไม่ทดแทนกัน

## 44. Risk-based Test Depth

```yaml
test_depth:
  low:
    required:
      - syntax
      - activation
      - focused_unit
      - object_atc
  medium:
    required:
      - characterization_or_unit
      - negative_and_boundary
      - regression_neighborhood
      - object_atc
      - independent_review
  high:
    required:
      - unit_and_integration
      - authorization
      - concurrency_or_idempotency
      - performance
      - full_impacted_package_atc
      - independent_audit
      - rollback_validation
```

High risk ได้แก่ financial posting, inventory, pricing, authorization, external integration, mass update, public API, persisted DDIC change และ transport-sensitive cross-object change

## 45. Completion Decision

Coordinator อนุญาตให้ไป `READY_FOR_UAT` เมื่อ:

- ทุก acceptance criterion มี test/evidence หรือ explicit manual-UAT mapping
- focused และ regression tests ผ่าน
- Auditor ไม่ให้ `REWORK`
- source/evidence freshness ตรงกัน
- ATC gate ผ่าน
- residual risks ถูกบันทึก
- UAT scenarios สร้างจากช่องว่างที่ AI test ไม่ได้

หาก automated test ไม่สามารถทำได้เพราะข้อจำกัด object/tool ให้ลงสถานะ `READY_FOR_MANUAL_TEST` ไม่ใช่แต่ง evidence หรือรายงานว่า test ผ่าน

## 46. Suggested Coordinator Decision Formula

Team Planner อาจใช้คะแนนเพื่อช่วยตัดสิน ไม่ใช่กฎตายตัว:

```text
risk score =
  business criticality (0-20)
+ data mutation (0-15)
+ integration breadth (0-15)
+ object/dependency complexity (0-15)
+ authorization impact (0-10)
+ migration/clean-core impact (0-10)
+ testability uncertainty (0-10)
+ performance risk (0-5)
```

- 0-24: single-agent role passes
- 25-54: Developer + Tester + Auditor
- 55-100: 5-7 role team with architect/integration/performance specialization

คะแนนเป็นค่าเริ่มต้น Coordinator ต้องบันทึกเหตุผลหาก override

## 47. Final Position

AI ใน Auto ABAP Delivery Mode ต้องทำหน้าที่เป็น loop engineer:

`Understand -> Design -> Test-design -> Implement -> Execute tests -> Critique -> Repair -> Regress -> Audit -> Evidence -> UAT handoff`

ความเป็น autonomous ไม่ได้วัดจากจำนวน tool calls ที่ AI ทำเอง แต่วัดจากความสามารถในการ menemukan defect ของตัวเอง, ซ่อมโดยไม่หลุด scope, สร้างหลักฐาน และรู้ว่าเมื่อใดต้องหยุดให้มนุษย์ตัดสินใจ

---

# Extension V4: SAP-Native Engineering Guardrails

> Decision: **ควรเพิ่ม V4** เพราะ V3 ครอบคลุม workflow, dynamic team และ self-testing แล้ว แต่ยังไม่มี SAP-native guardrail ที่ละเอียดพอสำหรับ security, transaction consistency, locking, client isolation, performance, lifecycle/API stability และ migration governance
>
> หลักของ V4 คือ Agent ไม่เพียงถามว่า “code ทำงานหรือไม่” แต่ต้องพิสูจน์ว่า “ปลอดภัย, consistent, upgrade-stable, client-safe, performant และเหมาะกับ SAP landscape นี้หรือไม่”

## 48. Guardrail Resolution by Landscape

ก่อนวางแผนหรือสร้าง source Agent ต้องสร้าง `sap_engineering_profile.yaml` จากระบบจริง:

```yaml
sap_engineering_profile:
  product: S4HANA_PRIVATE_EDITION
  release: "2025"
  abap_platform: "2025"
  language_version: standard_abap
  target_direction: abap_cloud
  database: hana
  client: "100"
  clean_core_policy: required
  released_api_policy: prefer_c1
  atc_variants:
    local: Z_DEV_DEFAULT
    security: Z_CVA
    cloud_readiness: ABAP_CLOUD_READINESS
    s4_readiness: S4HANA_READINESS
  available_analysis:
    - abap_unit
    - atc
    - sat
    - st05
    - sql_monitor
```

ห้ามใช้ guardrail ชุดเดียวแบบตายตัวกับ ECC 6.0, S/4HANA Private Edition และ BTP ABAP Environment ต้อง resolve ตาม release และเครื่องมือจริง

## 49. Mandatory Guardrail Domains

ทุก slice ต้องประเมินโดเมนต่อไปนี้ และ mark เป็น `PASS`, `NOT_APPLICABLE`, `MANUAL_EVIDENCE_REQUIRED` หรือ `BLOCKED`:

1. Language and API compatibility
2. Security and input trust
3. Authorization
4. Client isolation
5. Transaction and update consistency
6. Locking and concurrency
7. Database access and performance
8. Exception and cleanup behavior
9. Testability and observability
10. Transport and lifecycle
11. Migration and Clean Core
12. Data privacy and external side effects

## 50. Language and API Guardrail

### Rules

- ตรวจ language version ของ object ก่อนสร้างหรือแก้ code
- ใน ABAP Cloud/restricted language version ให้ใช้เฉพาะ object/API ที่มองเห็นและ released ตาม contract ที่อนุญาต
- C1 ใช้สำหรับ stable system-internal consumption; C0 เป็น extension contract ไม่ควรถูกตีความเป็น general consumption API
- Deprecated API ต้องมี successor assessment
- Decommissioned API เป็น fail gate
- Standard ABAP บน ECC/S/4HANA ยังใช้ classic API ได้ แต่ต้องบันทึก migration debt และ S/4HANA impact
- ห้าม copy demo code จาก keyword documentation ไป production โดยไม่ตรวจ release, authorization, error handling และ business semantics

### Agent evidence

```yaml
api_assessment:
  object: ZCL_ORDER_SERVICE
  language_version: abap_for_cloud_development
  dependencies:
    - name: I_SalesOrderTP
      release_state: released
      contract: C1
    - name: SAP_INTERNAL_CLASS
      release_state: not_released
      verdict: prohibited
```

## 51. Secure Coding Guardrail

### Mandatory threat review

Agent ต้องตรวจ input ที่มาจาก:

- selection screen/UI
- OData/REST/SOAP/RFC/IDoc
- files and logical paths
- database/customizing maintained by users
- message queue/event payload
- external command or URL
- dynamic class/method/function/table/field names

### Prohibited by default

- ต่อ dynamic SQL condition ด้วย string จาก external input
- dynamic table/column/method/function call โดยไม่ allowlist
- physical file path จากผู้ใช้โดยตรง
- OS command execution โดยไม่มี approved logical command และ authorization
- HTML/JavaScript output ที่ไม่ encode ตาม context
- log credential, token, password, sensitive payload หรือ full personal data
- outbound HTTP/RFC call ใน unit test

### Required controls

- Prefer host variables และ static ABAP SQL
- Dynamic identifier ใช้ allowlist จาก DDIC/configuration ที่เชื่อถือได้
- Validate canonical form, length, range, domain และ business state
- ใช้ logical file/path และ approved framework
- แยก technical error จาก user-safe message
- รัน ATC security/CVA variant เมื่อ available

## 52. Authorization Guardrail

Agent ต้องไม่สรุปว่า UI, transaction code หรือ service binding ป้องกัน backend logic เพียงพอ

### Checklist

- ระบุ protected operation และ authorization object
- ตรวจ authorization ที่ service/application boundary ก่อนอ่านหรือเปลี่ยนข้อมูล
- ทดสอบ allowed และ denied case
- ห้าม `AUTHORITY-CHECK` แล้วละเลย `sy-subrc`
- ห้าม hard-code user/role
- Background/RFC/technical user ต้องประเมิน authorization แยกจาก dialog user
- RAP ต้องตรวจ global/instance authorization และ feature control ตาม behavior
- Update task ห้ามเป็นที่พึ่งสำหรับ authorization check เพราะ update processing ไม่ทำ authorization check แทน caller

## 53. Client Isolation Guardrail

### Rules

- Business application ใช้ current client โดยค่าเริ่มต้น
- `USING CLIENT`, cross-client read/write และ client-independent table access เป็น high-risk
- Native SQL/ADBC/AMDP ต้องจัดการ client อย่างชัดเจน เพราะไม่มี implicit client handling แบบ ABAP SQL
- AMDP ควรใช้ client-safe pattern
- Unit/integration test ต้องตรวจว่า data ของ client อื่นไม่รั่ว
- Agent ห้าม seed test data ข้าม client

### Fail conditions

- query client-dependent table ผ่าน Native SQL โดยไม่มี client restriction
- generic table tool เปิด cross-client โดยไม่มี explicit approval
- write statement เปลี่ยน client อื่น

## 54. Transaction and SAP LUW Guardrail

### Design questions

- Business transaction boundary อยู่ที่ไหน
- ใครเป็น owner ของ `COMMIT WORK`/rollback
- ใช้ update task, bgRFC, tRFC/qRFC หรือ RAP save sequence หรือไม่
- partial success ยอมรับได้หรือไม่
- retry แล้วเกิด duplicate หรือไม่

### Rules

- Reusable class/BAdI/FM ไม่ควร issue `COMMIT WORK` เอง เว้นแต่ contract ระบุชัด
- ห้าม `COMMIT WORK` ใน loop
- ห้าม commit เพื่อแก้ visibility problem ของ test
- ตรวจ synchronous/asynchronous semantics ของ `COMMIT WORK AND WAIT`
- Update function module ห้ามทำ forbidden commit/rollback และต้องออกแบบ error handling ตาม update model
- Integration ต้องมี idempotency key/status และ retry strategy
- Unit test ต้องไม่ commit business data จริง
- RAP ให้เคารพ transactional buffer และ save sequence ห้าม bypass ด้วย direct commit

### Required scenarios

- update success
- high-priority update failure
- rollback
- duplicate retry
- partial external failure
- restart after process termination

## 55. Locking and Concurrency Guardrail

### Rules

- Change transaction ต้องมี lock strategy ก่อน read-modify-write
- ใช้ DDIC lock object หรือ RAP locking/ETag ตาม model
- lock key ต้องแคบพอ ไม่ปล่อย key ว่างจน lock ทั้งชุดโดยไม่ตั้งใจ
- จัดการ `FOREIGN_LOCK`, timeout/wait และ user feedback
- ระบุ `_SCOPE` และ lock ownership ให้สัมพันธ์กับ SAP LUW/update task
- ปลด lock ใน success และ error path
- Fresh-read + source hash ใช้กับ source-edit concurrency แต่ไม่แทน business-data enqueue lock
- Test concurrent update, stale ETag และ duplicate submission เมื่อเกี่ยวข้อง

## 56. Database and Performance Guardrail

### Static rules

- Restrict rows with selective conditions
- Select only required columns
- Prefer mass operation, join, view, subquery หรือ aggregation ที่ database
- หลีกเลี่ยง ABAP SQL ใน loop
- หลีกเลี่ยง repeated reads; cache เฉพาะเมื่อ consistency model ยอมรับ
- ตรวจ internal table access pattern; large lookup ควรใช้ hashed/sorted key ที่เหมาะสม
- ตรวจ `FOR ALL ENTRIES` empty-driver behavior และ duplicate semantics ใน legacy code
- หลีกเลี่ยง `SELECT *` โดยไม่มีเหตุผล
- ห้ามเพิ่ม secondary index อัตโนมัติจาก static guess ต้องมี runtime evidence และ DBA/architecture approval
- Table buffering ใช้เฉพาะข้อมูลอ่านบ่อย เปลี่ยนน้อย และยอมรับ buffering semantics ได้

### Runtime evidence triggers

ต้องใช้ SAT, ST05, SQL Monitor, SQL trace หรือ equivalent เมื่อ:

- high-volume object
- SQL ใน nested loop
- mass processing/background job
- response-time acceptance criterion
- migration to HANA
- ATC performance finding
- new index proposal

Agent ต้องแยก static smell กับ measured bottleneck ห้าม refactor performance จาก intuition อย่างเดียว

## 57. Exception, Cleanup and Error Contract

### Rules

- ใช้ class-based exception สำหรับ recoverable technical/business failure ตาม release
- exception interface ต้องบอก caller ว่าจัดการอะไรได้
- ห้าม catch `cx_root` แล้ว ignore
- preserving previous exception/cause เมื่อ wrap
- cleanup resource, lock และ temporary state ในทุก failure path
- `CLEANUP` ใช้เมื่อ context จะ unwind ไป handler ภายนอกและต้องคืน consistent state
- user message, application log และ technical diagnostics ต้องแยกกัน
- background/integration process ต้องให้ correlation ID, object key และ retryability

### Test scenarios

- expected business exception
- unexpected dependency exception
- cleanup/lock release
- no sensitive information leakage
- retryable vs non-retryable classification

## 58. ATC, SCI, CVA and Quality Governance

Agent ต้อง discover check variants ที่องค์กรกำหนดจริง ไม่ hard-code variant จาก documentation

### Gate sequence

1. Syntax/activation
2. Focused ABAP Unit
3. Object-level local ATC
4. Security/CVA check เมื่อ available
5. Affected package/transport ATC
6. S/4HANA or cloud-readiness variant เมื่อเกี่ยวข้อง
7. Baseline/exemption review

### Guardrails

- ห้าม suppress pragma/pseudo comment เพื่อปิด finding โดยไม่มี finding ID, rationale และ approver
- Existing baseline debt แยกจาก new finding
- New priority 1/2 finding เป็น fail gate โดยค่าเริ่มต้น
- Exemption ต้องมี expiry/owner/reason
- Transport release อยู่นอก autonomous envelope โดยค่าเริ่มต้น
- ATC บน production ไม่ใช่ default เพราะอาจสร้าง load; ใช้ development/test หรือ central check system

## 59. Test Framework Selection Guardrail

เลือก test framework จาก dependency:

- OO dependency: ABAP OO Test Double Framework
- ABAP SQL dependency: ABAP SQL Test Double Framework
- CDS logic/filter/calculation: CDS Test Double Framework
- Function Module dependency: Function Module Test Double Framework เมื่อ release รองรับ
- AMDP: AMDP Test Double Framework
- RAP: transactional buffer double หรือ mock EML ตาม capability

### Important limitation

CDS unit tests เหมาะกับ logic เช่น expressions, calculations, conversions, filters, `WHERE`, `HAVING`, `ON`; ไม่ใช่ performance test และไม่ใช่เครื่องมือพิสูจน์ทุก property ของ CDS entity

### Test isolation

- no productive data mutation
- no real outbound call
- deterministic clock/UUID/number-range adapter เมื่อจำเป็น
- fixture ต้องระบุ client, currency, unit, timezone และ decimal semantics

## 60. RAP-Specific Guardrail

RAP object ต้องตรวจเพิ่มเติม:

- strict mode requirement
- managed vs unmanaged ownership
- validation กับ determination ไม่สับสนกัน
- action/function contract
- global/instance authorization
- feature control
- pessimistic lock/ETag/total ETag
- draft lifecycle และ resume lock
- early/late numbering
- failed/reported message mapping
- additional/unmanaged save
- side effects สำหรับ UI reload ไม่ถูกใช้แทน business logic
- direct database update ไม่ bypass transactional buffer

Agent ต้องสร้าง test matrix สำหรับ create/update/delete, action, validation, draft activate/discard, stale ETag, authorization และ save failure ตาม behavior ที่ประกาศ

## 61. Transport and Object Lifecycle Guardrail

ก่อนแก้ object:

- ตรวจ TADIR/package/software component
- ตรวจ original system และ namespace
- ตรวจ transport/task ownership
- ตรวจ lock/inactive version/parallel editor
- fresh-read source และ hash ก่อน write
- dependency object ต้องอยู่ใน transport sequence ที่ถูกต้อง
- ห้ามย้าย package หรือลบ object โดย autonomy ปกติ
- ห้าม release/import transport
- DDIC persisted change ต้องมี conversion/downtime/data migration assessment
- Generated object ต้องแก้ผ่าน source owner ไม่แก้ generated artifact โดยตรง

## 62. ECC-to-S/4HANA and Clean Core Guardrail

### New development

- Standard-first and configuration-first
- Prefer released extension points/APIs
- เลือก on-stack vs side-by-side จาก transactional consistency, latency, data ownership และ lifecycle
- บันทึก Clean Core classification และ upgrade coupling

### Existing custom code

- ใช้ custom code analysis ก่อน conversion
- ตรวจ S/4HANA readiness/Simplification Database
- หลัง conversion ตรวจ SPDD, SPAU, SPAU_ENH และ local S/4HANA ATC ตามกระบวนการของโครงการ
- แยก remediation ที่จำเป็นต่อ conversion ออกจาก modernization/refactor เพื่อควบคุม scope
- Runtime usage evidence ช่วยตัดสิน retire/retain/remediate แต่ห้ามลบจาก static assumption

## 63. Observability and Operations Guardrail

งาน background, interface และ autonomous processing ต้อง operationally supportable:

- correlation ID / business key
- Application Log หรือ framework log ที่เหมาะสม
- status and retry state
- no secret/personal data leakage
- job/RFC/IDoc/OData error mapping
- restartability และ duplicate prevention
- monitoring owner และ runbook
- log retention ตาม policy

Agent ต้องทดสอบว่า error ไม่หายไปใน job log เพียงข้อความกว้าง ๆ และผู้ดูแลสามารถหา root cause จาก key/evidence ได้

## 64. Destructive and External Side-Effect Gate

การกระทำต่อไปนี้ต้อง human approval เสมอ:

- mass update/delete
- production data change
- transport release/import
- standard modification
- cross-client operation
- schema/index change
- authorization role/object change
- real email/payment/posting/external API call
- job scheduling ที่เกิด business effect
- replay IDoc/event/RFC ที่อาจ duplicate transaction

Test mode ต้องใช้ simulation/test double/sandbox destination ก่อนเสมอ

## 65. Guardrail-as-Code

หลักที่ deterministic ควรลง script/schema/linter แทน prose:

```text
guardrails/
  profiles/
    ecc.yaml
    s4hana-standard-abap.yaml
    s4hana-abap-cloud.yaml
    btp-abap.yaml
  rules/
    security.yaml
    authorization.yaml
    client-isolation.yaml
    luw-and-commit.yaml
    locking.yaml
    sql-performance.yaml
    api-release.yaml
    transport.yaml
    destructive-actions.yaml
  scripts/
    resolve_profile.py
    validate_guardrail_report.py
    detect_commit_in_reuse_layer.py
    detect_dynamic_sql_risk.py
    validate_test_traceability.py
    validate_atc_evidence.py
```

Skill ทำหน้าที่ orchestration ส่วน ATC/CVA และ deterministic validators ทำหน้าที่ enforcement

## 66. Guardrail Report Artifact

```yaml
guardrail_report:
  task_id: CR-1024
  spec_revision: SPEC-R006
  source_hash: sha256:...
  landscape_profile: s4hana-standard-abap
  checks:
    api_release: PASS
    security: PASS
    authorization: PASS
    client_isolation: PASS
    luw_consistency: PASS_WITH_RISK
    locking: PASS
    performance: MANUAL_EVIDENCE_REQUIRED
    testability: PASS
    transport: PASS
    clean_core: PASS_WITH_DEBT
  risks:
    - id: RISK-12
      area: luw_consistency
      detail: downstream legacy FM performs commit internally
      disposition: integration test required
  blockers: []
```

`READY_FOR_UAT` ต้องอ้างถึง guardrail report revision เดียวกับ source และ test evidence

## 67. Updated Engineering Loop

```text
Discover Landscape
-> Resolve SAP Guardrail Profile
-> Capability Audit
-> Grill and Spec
-> Architecture / Clean Core Decision
-> Threat + Authorization + LUW + Lock Analysis
-> Dynamic Team Plan
-> Test Scenario Design
-> Implement Slice
-> Unit/Test-Double Execution
-> Security + Client + Concurrency Review
-> Runtime Performance Evidence when Triggered
-> ATC/CVA/Readiness Checks
-> Independent Audit
-> Repair Loop
-> Guardrail Report
-> UAT Handoff
```

## 68. Final V4 Decision

V4 ไม่ควรเพิ่ม “กฎการเขียนสวย” จำนวนมาก แต่ควรเพิ่ม guardrail ที่ป้องกัน defect แบบ SAP-specific ซึ่ง syntax check และ unit test ธรรมดาจับไม่ได้ ได้แก่:

1. wrong client access
2. missing authorization
3. broken SAP LUW/commit ownership
4. missing enqueue/ETag concurrency control
5. unsafe dynamic SQL or dynamic call
6. unmeasured SQL/performance design
7. unreleased/deprecated API coupling
8. invalid RAP transactional behavior
9. transport/lifecycle inconsistency
10. conversion and Clean Core debt hidden from Project Owner

ดังนั้นข้อสรุปคือ **ควรเลื่อนเป็น V4** และให้ `SAP Guardrail Profile + Guardrail Report` เป็น mandatory artifacts ของ Auto ABAP Delivery Mode

## 69. Authoritative SAP Sources Used for V4

- SAP Help Portal: Secure Programming for ABAP and ABAP Security Notes
- ABAP Keyword Documentation: SQL injection, client handling, SAP LUW, COMMIT WORK, SAP locks, exceptions and CLEANUP
- SAP Help Portal: ABAP Cloud Development Model and released API contracts
- SAP Help Portal: ABAP SQL performance notes; SAT, ST05, SQL Monitor and SQL Performance Tuning Worklist
- SAP Help Portal: ABAP Unit and CDS/SQL/FM/AMDP/RAP test doubles
- SAP Help Portal: ATC, central checks, baselines, exemptions and transport checking
- SAP Help Portal: RAP behavior, determinations, validations, locking, ETag and side effects
- SAP Custom Code Migration Guide for SAP S/4HANA 2025

---

# Extension V5: Unattended Long-Run Execution

> เป้าหมาย: หลัง Project Owner อนุมัติ Draft Spec, execution plan และ autonomy envelope แล้ว AI ต้องทำงานต่อได้โดยไม่รบกวนผู้ใช้ จนกระทั่งส่งมอบ `READY_FOR_UAT`, พบ blocker ที่ต้องใช้การตัดสินใจของมนุษย์ หรือหยุดแบบปลอดภัย

## 70. Execution Contract: Approve Once, Run to Gate

ก่อนเริ่ม unattended run ต้อง freeze contract ต่อไปนี้:

- Approved spec revision and hash
- SAP target SID/client
- Package, transport request and task
- Allowed objects/object patterns
- Permitted and prohibited actions
- Test-data and external-call policy
- Required ATC/security/readiness variants
- Runtime and repair budgets
- Stop/escalation conditions
- Final target state, default `READY_FOR_UAT`

หลัง Project Owner สั่ง `START AUTONOMOUS DEVELOPMENT` Agent ไม่ควรถามยืนยันเรื่องเดิมซ้ำ และไม่ควร pause เพื่อรายงาน progress ปกติ

## 71. Non-Interrupt Policy

### Silent continuation

Agent ทำต่อเองเมื่อเหตุการณ์:

- reversible
- อยู่ใน approved scope
- อยู่ใน autonomy envelope
- ไม่มี business ambiguity
- ไม่แตะ production/irreversible action
- evidence ยืนยันว่าขั้นก่อนหน้าผ่าน

ตัวอย่าง: เพิ่ม local test class, แก้ implementation ภายใน approved object, activate DEV object, rerun ABAP Unit, rerun object ATC, update ledger และสร้าง documentation

### Deferred reporting

สิ่งที่ไม่ต้อง interrupt แต่ต้องบันทึก:

- warning ที่ไม่ block acceptance criteria
- ATC priority 3 ที่มี approved disposition rule
- alternative implementation ที่ไม่ได้เลือก
- repair attempt ที่สำเร็จภายใน budget
- technical debt ที่ไม่เพิ่ม business risk ทันที

### Interrupt only on decision boundary

ส่ง notification เมื่อ:

1. ผลลัพธ์เป็น `READY_FOR_UAT`
2. ต้องเปลี่ยน approved spec/scope
3. ต้องทำ irreversible/high-risk action
4. target SID/client/package/TR ไม่ตรง contract
5. source drift หรือ lock conflict ที่ resolve อย่างปลอดภัยไม่ได้
6. ต้องใช้ released API/extension point ที่ไม่มี หรือจำเป็นต้องเลือก business trade-off
7. repair budget หมด
8. required MCP/tool/capability หายไประหว่าง run
9. security, authorization, data-privacy หรือ transaction-consistency blocker
10. runtime budget/lease หมด

Agent ห้าม interrupt เพียงเพื่อถามว่า “ให้ทำต่อไหม” หาก next step อยู่ใน approved plan

## 72. Durable Run State

Unattended run ต้องไม่พึ่ง conversation context ใช้ durable state:

```yaml
run_state:
  run_id: RUN-CR1024-001
  task_id: CR-1024
  mode: unattended
  status: implementing
  spec_revision: SPEC-R006
  spec_hash: sha256:...
  autonomy_envelope_hash: sha256:...
  checkpoint_sequence: 18
  current_slice: S04
  current_step: focused_abap_unit
  last_successful_step: activation
  last_source_hash: sha256:...
  lease_expires_at: 2026-11-20T21:00:00+07:00
  heartbeat_at: 2026-11-20T14:35:00+07:00
  recovery_count: 1
  notification_state: none
```

ทุก write, activation, test, repair และ audit ต้องเป็น resumable step มี idempotency key และ evidence ID

## 73. Lease, Heartbeat and Watchdog

- Run lease จำกัดเวลา เช่น 8 ชั่วโมงหรือหนึ่ง execution window
- Heartbeat update หลังจบ tool operation หรืออย่างน้อยทุก 5-10 นาทีสำหรับงานยาว
- Watchdog ตรวจ stalled state, repeated tool failure, expired credential และ lost MCP connection
- เมื่อ process restart ให้ resume จาก last committed checkpoint ไม่เริ่มใหม่ทั้งหมด
- Before resume ต้อง fresh-read system/client/object/source/lock/TR และ invalidate stale evidence
- หากไม่สามารถพิสูจน์ state เดิมได้ ให้ `PAUSED_SAFE` และแจ้งผู้ใช้เพียงครั้งเดียว

## 74. Work Queue and Slice Scheduler

Plan ถูกแปลงเป็น dependency-aware queue:

```yaml
work_queue:
  - id: S01
    objective: reproduce current defect
    depends_on: []
    status: completed
  - id: S02
    objective: add regression test
    depends_on: [S01]
    status: completed
  - id: S03
    objective: implement quantity calculation fix
    depends_on: [S02]
    status: completed
  - id: S04
    objective: validate partial delivery and unit conversion
    depends_on: [S03]
    status: running
  - id: S05
    objective: full regression and UAT pack
    depends_on: [S04]
    status: queued
```

Scheduler parallelize เฉพาะ read-only analysis, test design และ independent audit ที่ไม่แก้ object เดียวกัน Production-object write ต้อง serialize ต่อ object

## 75. Recovery and Retry Policy

แบ่ง failure:

- `TRANSIENT`: timeout, temporary lock, MCP transport issue; retry with bounded exponential backoff
- `REPAIRABLE`: syntax/test/ATC defect; enter engineering repair loop
- `STALE_STATE`: source/TR/spec changed; refresh and re-evaluate
- `POLICY_BLOCK`: action outside envelope; stop and escalate
- `BUSINESS_BLOCK`: expected behavior ambiguous/conflicting; stop and escalate
- `FATAL_SAFE`: wrong system/client, credential identity mismatch, evidence corruption; terminate lease

ห้าม retry action ที่อาจสร้าง side effect หากไม่มี idempotency proof

## 76. Notification Policy

Default notification model:

- Start receipt: แจ้งครั้งเดียวว่า run เริ่มแล้ว พร้อม run ID และ frozen scope
- No routine progress interruption
- Blocked notification: ส่งครั้งเดียว พร้อม decision request ที่ตอบได้ทันที
- Completion notification: ส่งเมื่อ `READY_FOR_UAT`
- Optional digest: สรุปทุก 2 ชั่วโมงเฉพาะกรณีผู้ใช้ opt-in

Completion message ต้องมี:

- final state
- changed objects
- test/ATC/guardrail summary
- residual risk
- UAT client and scenarios
- transport status
- explicit statement that production deployment/release has not been performed

## 77. Decision Inbox

เมื่อ block ห้ามส่งคำถามกระจัดกระจาย ให้รวมเป็น decision packet:

```yaml
decision_request:
  id: DEC-004
  severity: blocking
  context: no released API for required pricing detail
  options:
    - id: A
      choice: use classic API in Standard ABAP
      impact: medium clean-core debt
    - id: B
      choice: side-by-side service
      impact: higher delivery effort and integration scope
    - id: C
      choice: reduce scope
      impact: acceptance criterion AC-09 removed
  recommendation: A
  required_from_owner: choose A, B or C
```

Agent หยุดเฉพาะ branch ที่ block หาก workstream อื่นยังปลอดภัยและไม่ขึ้นกับ decision ให้ทำต่อได้

## 78. Source Drift and Human Co-Editing

- ก่อนทุก write ทำ fresh read + hash + lock/ETag check
- หากคนแก้ source ระหว่าง run ห้าม overwrite
- วิเคราะห์ diff ว่า overlap หรือไม่
- Non-overlapping change อาจ rebase ได้เมื่อ tool รองรับและ audit ใหม่
- Overlapping/business-impact change ให้ pause affected slice
- Evidence ที่เกิดก่อน source drift ต้อง stale โดยอัตโนมัติ
- ห้าม assume ว่า lock อย่างเดียวป้องกัน change ทั้งหมด

## 79. Isolation and Safe Workspace

- ใช้ dedicated transport task หรือ approved task ownership
- หนึ่ง Agent writer ต่อ object
- Test data ใช้ test double ก่อน, Sandbox/DEV data ตาม policy
- ห้าม real external destination
- ห้าม production connection ใน unattended write mode
- Generated artifacts และ evidence แยกตาม run ID
- Cleanup temporary test artifacts เมื่อสำเร็จ หรือบันทึกรายการค้างเมื่อ cleanup ไม่สำเร็จ

## 80. Resource Budget

```yaml
run_budget:
  wall_clock_hours: 8
  max_tool_calls: 500
  max_repairs_per_slice: 3
  max_same_error_repeats: 2
  max_active_subagents: 7
  max_data_preview_rows: 100
  max_parallel_read_tracks: 3
```

เมื่อใกล้ budget limit Agent ต้องจัดลำดับงานที่จำเป็นต่อ safe checkpoint ก่อน ห้ามเร่งข้าม test/audit เพื่อให้เสร็จ

## 81. Final States

- `READY_FOR_UAT`: planned AI validation ผ่านครบ
- `READY_FOR_MANUAL_TEST`: automated capability ไม่เพียงพอ แต่ implementation/evidence พร้อมให้ทดสอบต่อ
- `BLOCKED_OWNER_DECISION`: ต้องการ business/architecture/governance decision
- `BLOCKED_TOOLING`: MCP/tool/access ไม่เพียงพอ
- `PAUSED_SAFE`: lease/runtime/crash recovery ไม่สามารถพิสูจน์ state ได้
- `FAILED_SAFE`: repair budget หมดและไม่มี unsafe change ค้าง
- `CANCELLED`: ผู้ใช้ยกเลิกและ Agent ทำ cleanup/checkpoint แล้ว

สถานะต้องไม่เป็น `DONE` ก่อน UAT และ production approval

## 82. UAT and Production Boundary

Unattended development สิ้นสุดที่ `READY_FOR_UAT` เท่านั้น:

1. แจ้ง Project Owner
2. ให้ UAT pack และ expected results
3. รอ UAT feedback
4. หาก fail ให้เปิด iteration ใหม่โดยคง traceability
5. หาก pass ให้สร้าง production-readiness recommendation
6. Transport release/import, production deployment และ productive data operation ต้องเป็น separate explicit command และ approval workflow

Approval สำหรับ development ห้ามถูกนำไปตีความว่าอนุญาต production

## 83. Recommended Command Contract

```text
/auto-abap-delivery start-unattended CR-1024

Target: S4D/100
Spec: SPEC-R006
Stop at: READY_FOR_UAT
Notifications: blocked-or-complete
Runtime lease: 8h
Production actions: prohibited
```

Agent ตอบ start receipt ครั้งเดียว แล้วทำงานต่อจนถึง terminal/decision state

## 84. Final V5 Position

แนวคิดที่เหมาะสมคือ `approve once, run to gate` ไม่ใช่ `ask before every step`

ผู้ใช้และ AI แยกกันทำงานได้จริงเมื่อมี:

- frozen execution contract
- explicit autonomy envelope
- durable state/checkpoints
- heartbeat/watchdog
- idempotent/resumable steps
- bounded retry and repair budget
- source-drift protection
- notification only on blocked/completed
- hard boundary before UAT and production

ความเงียบระหว่าง run ไม่ได้หมายถึงขาดการควบคุม ทุก action ต้องถูกบันทึกและตรวจย้อนหลังได้ เพียงแต่ไม่รบกวน Project Owner จนกว่าจะถึง decision boundary

---

# Extension V6: Run State Machine, Decision Inbox UX, and Restart Recovery

> V6 converts unattended execution into an implementable orchestration contract. It defines legal state transitions, persistence boundaries, user-facing decision handling, and deterministic recovery after an Agent or MCP restart.

## 85. Run State Machine Design

### 85.1 Design principles

1. A state describes a durable business phase, not a temporary UI message.
2. Every state transition is persisted before the next side-effecting action.
3. A command is accepted only when legal for the current state.
4. A transition records actor, reason, timestamp, input revision, source hash, and evidence IDs.
5. `READY_FOR_UAT` is the terminal state for autonomous development. UAT and production use separate workflows.
6. Restart recovery never assumes the previous action succeeded. It reconciles against SAP first.
7. Any state may transition to `CANCELLING`; destructive rollback is not assumed to be possible.

### 85.2 Top-level states

```text
DRAFT
  -> AWAITING_APPROVAL
  -> QUEUED
  -> STARTING
  -> RUNNING
       -> BLOCKED
       -> PAUSING -> PAUSED
       -> RECOVERING
       -> VERIFYING_FINAL
  -> READY_FOR_UAT

Exceptional terminal states:
  FAILED_SAFE
  CANCELLED
  SUPERSEDED
```

### 85.3 RUNNING substates

```text
RUNNING
  ├─ DISCOVERING
  ├─ ANALYZING_IMPACT
  ├─ PLANNING_TEAM
  ├─ DESIGNING_TESTS
  ├─ IMPLEMENTING_SLICE
  ├─ ACTIVATING
  ├─ TESTING_FOCUSED
  ├─ REPAIRING
  ├─ TESTING_REGRESSION
  ├─ RUNNING_ATC
  ├─ AUDITING
  ├─ DOCUMENTING
  └─ BUILDING_UAT_PACK
```

Substates are durable because restart behavior differs. For example, an interrupted source write requires reconciliation, while interrupted documentation generation can normally be rerun safely.

### 85.4 State definitions

| State | Meaning | Entry requirement | Legal exits |
|---|---|---|---|
| `DRAFT` | Intake/spec is incomplete | Skill explicitly invoked | `AWAITING_APPROVAL`, `CANCELLED` |
| `AWAITING_APPROVAL` | Spec, plan, and envelope ready for owner | hashes generated and validation passed | `QUEUED`, `DRAFT`, `CANCELLED` |
| `QUEUED` | Approved run waits for worker/window | approval signature matches hashes | `STARTING`, `CANCELLED`, `SUPERSEDED` |
| `STARTING` | Preflight and lease acquisition | worker assigned | `RUNNING.DISCOVERING`, `BLOCKED`, `FAILED_SAFE` |
| `RUNNING.*` | Autonomous work is active | valid lease and target identity | another run substate, `BLOCKED`, `PAUSING`, `RECOVERING`, `VERIFYING_FINAL` |
| `BLOCKED` | Owner/tool/policy decision required | blocking event persisted | previous resumable state, `CANCELLED`, `SUPERSEDED` |
| `PAUSING` | Agent is reaching safe checkpoint | pause requested or budget nearly exhausted | `PAUSED`, `FAILED_SAFE` |
| `PAUSED` | Safe durable checkpoint exists | no active write operation | `RECOVERING`, `CANCELLED`, `SUPERSEDED` |
| `RECOVERING` | Reconcile durable state with SAP reality | restart, lease loss, or stale state | prior safe substate, `BLOCKED`, `FAILED_SAFE` |
| `VERIFYING_FINAL` | Full evidence and guardrail consolidation | all slices completed | `READY_FOR_UAT`, `RUNNING.REPAIRING`, `BLOCKED`, `FAILED_SAFE` |
| `READY_FOR_UAT` | Development and planned AI validation completed | final evidence manifest signed | separate UAT workflow only |
| `FAILED_SAFE` | Run cannot continue safely | safe stop report generated | new run/iteration only |
| `CANCELLED` | Owner cancelled and cleanup/checkpoint completed | cancellation report | none |
| `SUPERSEDED` | New spec/run replaces this run | replacement run ID recorded | none |

### 85.5 Transition record

```yaml
transition:
  transition_id: TRN-000184
  run_id: RUN-CR1024-001
  from: RUNNING.ACTIVATING
  to: RUNNING.TESTING_FOCUSED
  occurred_at: 2026-11-20T14:42:10+07:00
  actor: agent:abap-developer-01
  reason: object activation reconciled successfully
  command_id: CMD-000091
  spec_revision: SPEC-R006
  source_before: sha256:old
  source_after: sha256:new
  evidence:
    - EV-ACT-0042
  lease_fencing_token: 27
```

The fencing token prevents a stale worker from continuing after a newer worker acquires the lease.

### 85.6 Command model

Commands are intent; events are observed facts.

```yaml
command:
  command_id: CMD-000091
  type: ACTIVATE_OBJECT
  run_id: RUN-CR1024-001
  expected_state: RUNNING.ACTIVATING
  target:
    system: S4D
    client: "100"
    object: ZCL_SO_ALLOCATION
  preconditions:
    source_hash: sha256:new
    transport: S4DK900123
    lock_owner: agent-runner
  idempotency_key: RUN-CR1024-001/ZCL_SO_ALLOCATION/ACTIVATE/sha256:new
```

A command result is not considered committed until the Agent reads SAP again and persists reconciled evidence.

### 85.7 Transition guards

Before every side effect:

- lease is active and fencing token matches
- current SID/client matches execution contract
- spec and autonomy-envelope hashes match
- object is within allowed scope
- source hash and lock state match preconditions
- transport/task remains modifiable and assigned correctly
- action is permitted by policy
- no unresolved blocking decision applies to the slice

Before entering `READY_FOR_UAT`:

- work queue has no running/queued required slice
- all acceptance criteria have automated evidence or explicit manual-UAT mapping
- no `REWORK` audit verdict remains
- final source hashes match test/ATC evidence
- guardrail report has no blocker
- temporary artifacts are cleaned or disclosed
- transport is not released
- UAT package has been generated and validated

## 86. Decision Inbox UX

### 86.1 User experience goal

The Project Owner should not read tool logs. The inbox presents only decisions that genuinely require human authority. Each item must be answerable in less than two minutes unless supporting detail is intentionally expanded.

### 86.2 Inbox layout

```text
Decision Inbox                                      2 Blocking | 1 Advisory

[BLOCKING] DEC-004  Released API unavailable              Due: Now
CR-1024 · Slice S04 · Clean Core
Recommended: Option A · Confidence: Medium
[Review decision]

[BLOCKING] DEC-005  Test client does not permit update     Due: Now
CR-1024 · Integration Test
Recommended: Use Sandbox Client 110
[Review decision]

[ADVISORY] DEC-006  ATC Priority 3 finding accepted
No action required · Included in final risk report
[View]
```

### 86.3 Decision card

Each blocking card contains:

1. **What happened**: one sentence without tool jargon.
2. **Why the Agent cannot decide**: scope, business, security, or irreversible boundary.
3. **Current safe state**: what has and has not changed in SAP.
4. **Affected scope**: slice, objects, acceptance criteria, deadline impact.
5. **Options**: normally 2-4 mutually exclusive choices.
6. **Recommendation**: a single preferred option with rationale and confidence.
7. **Risk comparison**: delivery, Clean Core, functional, operational, and rollback impact.
8. **Required response**: one-click choice, free-text only when an option needs a value.
9. **Continue-safe-work indicator**: whether unaffected branches continue.
10. **Evidence drawer**: source diff, ATC finding, API status, logs, and tool evidence.

### 86.4 Example: Released API decision

```text
DEC-004 · BLOCKING
No released API is available for pricing detail AC-09

The current S/4HANA target requires Clean Core compliance. The only discovered
on-stack API is not released for customer consumption. No production action has
been performed. Slices S01-S03 are complete; S04 is paused.

Recommended: A — Use classic API with documented Clean Core debt
Confidence: Medium

A. Use classic API in Standard ABAP
   Delivery: +1 day | Clean Core: Medium debt | UAT scope: unchanged

B. Build a side-by-side service on SAP BTP
   Delivery: +5-8 days | Clean Core: Preferred | New integration/security scope

C. Remove AC-09 from this release
   Delivery: no delay | Functional scope reduced | Spec revision required

[Choose A] [Choose B] [Choose C] [Reject and add guidance]

Safe continuation: Test documentation and completed-slice audit will continue.
```

### 86.5 Example: Source drift decision

```text
DEC-008 · BLOCKING
ZCL_SO_ALLOCATION changed during the autonomous run

P. Developer changed the same method that Slice S04 is modifying. The Agent did
not overwrite the change. Previous test evidence for this object is now stale.

A. Rebase Agent changes and rerun all affected tests — Recommended
B. Discard Agent changes for S04 and re-plan from the new source
C. Stop this run and hand ownership back to the human developer

[Choose A] [Choose B] [Choose C]
```

### 86.6 Decision lifecycle

```text
OPEN
 -> VIEWED
 -> ANSWERED
 -> VALIDATING
 -> APPLIED

Alternative exits:
 OPEN -> WITHDRAWN       blocker disappeared after reconciliation
 OPEN -> SUPERSEDED      newer decision replaces it
 ANSWERED -> REJECTED    answer violates current policy or became stale
```

An answer includes the decision revision. If evidence changed after the card was shown, the old answer must not be applied automatically.

```yaml
decision_answer:
  decision_id: DEC-004
  decision_revision: 3
  selected_option: A
  answered_by: project-owner
  answered_at: 2026-11-20T15:05:00+07:00
  comment: Accept until released successor is available
  resulting_spec_revision: SPEC-R007
```

### 86.7 Notification behavior

- One notification when a blocking decision is created.
- No reminder spam. Optional reminder after 4 business hours, then once per business day.
- Multiple related blockers should be bundled into one inbox digest, not separate chat messages.
- Advisory items never block the run and appear only in the inbox/final report.
- When answered, only the affected branch resumes. The user receives no extra message unless the decision changes target delivery or risk materially.

## 87. Recovery after Agent Restart

### 87.1 Recovery principle

The ledger says what the Agent intended. SAP says what actually exists. After restart, SAP is the authority for source, activation, lock, transport, and testable object state; the durable ledger is the authority for approved scope and policy.

### 87.2 Recovery phases

```text
1. Acquire recovery lease with a new fencing token
2. Load and validate durable artifacts
3. Identify the last durable transition and in-flight command
4. Re-discover MCP tools and SAP target identity
5. Reconcile the in-flight action against SAP
6. Detect source drift, lock conflict, transport change, and stale evidence
7. Select resume, compensate, repair, or block
8. Persist recovery report
9. Resume from a legal state
```

### 87.3 Example scenario

The Agent restarted after sending an activation command for `ZCL_SO_ALLOCATION`, but before recording the result.

Last persisted state:

```yaml
run_state:
  state: RUNNING.ACTIVATING
  checkpoint_sequence: 18
  fencing_token: 26

in_flight_command:
  command_id: CMD-000091
  type: ACTIVATE_OBJECT
  object: ZCL_SO_ALLOCATION
  expected_source_hash: sha256:new
  activation_result: unknown
  idempotency_key: RUN-CR1024-001/ZCL_SO_ALLOCATION/ACTIVATE/sha256:new
```

### 87.4 Restart reconciliation

The new worker performs read-only checks:

```yaml
recovery_observation:
  target_identity:
    expected: S4D/100
    actual: S4D/100
    match: true
  object:
    name: ZCL_SO_ALLOCATION
    active_source_hash: sha256:new
    inactive_source_exists: false
    activation_status: active
    syntax_status: clean
    lock_owner: none
    transport: S4DK900123
  previous_test_evidence:
    status: stale
    reason: captured before activation reconciliation
```

Decision:

- Do not resend activation because SAP already contains the expected active hash.
- Record synthetic reconciled event `ACTIVATION_CONFIRMED_AFTER_RESTART`.
- Invalidate test evidence captured before the uncertain activation boundary.
- Transition from `RECOVERING` to `RUNNING.TESTING_FOCUSED`.

Recovery report:

```yaml
recovery_report:
  recovery_id: REC-0007
  run_id: RUN-CR1024-001
  previous_worker_token: 26
  new_worker_token: 27
  cause: agent_process_restart
  in_flight_command: CMD-000091
  reconciliation:
    result: action_already_applied
    sap_active_hash: sha256:new
    command_replayed: false
  invalidated_evidence:
    - EV-TEST-0038
  resume_state: RUNNING.TESTING_FOCUSED
  owner_notification_required: false
```

### 87.5 Alternative recovery outcomes

#### A. Source exists but is inactive

- Re-run syntax check.
- If source hash equals the approved command and syntax is clean, activation may be retried with the same idempotency key and new fencing token.
- If syntax fails, transition to `RUNNING.REPAIRING`.

#### B. Active source hash is the old hash

- The activation did not take effect.
- Verify the inactive source hash and transport/lock.
- Retry only if all preconditions still match.

#### C. Active source hash differs from both old and expected hashes

- A human or another Agent changed the object.
- Do not replay the command.
- Mark all affected evidence stale.
- Open a source-drift Decision Inbox item and transition to `BLOCKED`.

#### D. Target SID/client differs

- Terminate the lease immediately.
- Do not write or activate anything.
- Transition to `FAILED_SAFE` or `BLOCKED_TOOLING` depending on whether the destination mapping can be corrected safely.

#### E. Transport was released during downtime

- Do not create a new transport automatically.
- Transition to `BLOCKED_OWNER_DECISION` with options to assign a new approved TR, hand back ownership, or supersede the run.

### 87.6 Idempotency classification

| Action | Default replay policy after restart |
|---|---|
| Read/search/where-used | Safe to repeat |
| Generate local documentation | Safe with deterministic output path/version |
| Syntax check/ATC/test | Safe to repeat if no business side effect |
| Source write | Reconcile hash first; never blindly replay |
| Activation | Reconcile active/inactive version first |
| Test-data creation | Require unique run marker and cleanup/reconciliation |
| External API/RFC/IDoc send | Never replay without remote idempotency proof |
| COMMIT/posting/mass update | Never replay automatically |
| Transport release/import | Outside unattended development scope |

## 88. Persistence Model

Suggested files per run:

```text
runs/RUN-CR1024-001/
  execution-contract.yaml
  autonomy-envelope.yaml
  run-state.yaml
  work-queue.yaml
  transition-log.jsonl
  command-log.jsonl
  evidence-index.yaml
  decisions/
    DEC-004.yaml
  recovery/
    REC-0007.yaml
  checkpoints/
    CP-000018.yaml
  artifacts/
  uat/
```

`transition-log.jsonl` and `command-log.jsonl` are append-only. Mutable summary files such as `run-state.yaml` are rebuilt from the log when corruption is suspected.

## 89. Minimum Implementation Components

1. **Run Orchestrator**: validates transitions and schedules slices.
2. **Lease Manager**: lease expiry, heartbeat, and fencing token.
3. **Checkpoint Store**: atomic persistence of state and hashes.
4. **SAP Reconciler**: verifies SID/client, object source, activation, lock, and TR.
5. **Policy Engine**: autonomy-envelope and destructive-action guard.
6. **Decision Inbox Service**: decision cards, revisions, answers, and notifications.
7. **Evidence Manager**: evidence freshness and invalidation.
8. **Recovery Controller**: classifies in-flight commands and determines replay policy.
9. **Notification Adapter**: start, blocking, and completion notifications only.
10. **UAT Pack Builder**: final traceability, test results, residual risks, and instructions.

## 90. Acceptance Tests for V6 Orchestration

- Restart before source write: resumes without duplicate write.
- Restart after write but before confirmation: reconciles source hash.
- Restart during activation: chooses replay or confirm correctly.
- Restart after test completion but before evidence commit: reruns test and records one current evidence set.
- Two workers acquire the same run: stale fencing token is rejected.
- Human edits source during run: Agent never overwrites it.
- Decision answer arrives for stale revision: answer is rejected and card refreshed.
- Lease expires during repair: Agent checkpoints and enters `PAUSED`.
- MCP loses write capability: run becomes `BLOCKED_TOOLING`, read-only audit may continue.
- Completion gate with stale evidence: `READY_FOR_UAT` is rejected.
- Cancellation during test: test finishes or times out, cleanup runs, then state becomes `CANCELLED`.
- Production destination appears in configuration: unattended write remains prohibited.

## 91. V6 Recommendation

The State Machine should be implemented before allowing truly unattended SAP writes. Decision Inbox and restart recovery are not optional interface features; they are part of the safety model.

The critical implementation order is:

1. append-only transition/command logs
2. lease and fencing token
3. SAP reconciliation for source/activation/TR
4. transition guards and policy engine
5. checkpoint/resume
6. Decision Inbox
7. notifications
8. advanced parallel scheduling

This order provides safe single-worker recovery first. Multi-agent parallelism should be enabled only after replay, drift, and stale-evidence behavior are proven by orchestration acceptance tests.

---

# Extension V7: Unattended and Attended Interaction Control

> Decision: **V7 is justified.** V6 already provides safe orchestration, recovery, Decision Inbox, evidence, and UAT boundaries. The remaining gap is not another development workflow. It is a unified interaction policy that lets the Project Owner choose how often to participate without creating separate engines for unattended and attended delivery.
>
> Default remains **Unattended Mode**. Attended Mode adds review checkpoints on top of the same state machine, guardrails, testing loop, recovery model, and evidence contract.

## 92. Two independent control dimensions

Do not combine execution behavior and review intensity into one field.

```yaml
interaction_policy:
  execution_mode: unattended | attended
  review_level: standard | guided | controlled | strict | custom
```

- `execution_mode` determines whether scheduled human reviews pause the run.
- `review_level` determines which checkpoints require review when `execution_mode: attended`.
- For `unattended`, `review_level` is recorded as `not_applicable`; Decision Inbox boundaries still apply.

This separation prevents terms such as Controlled or Strict from being confused with task complexity, SAP risk, or AI capability.

## 93. Mode selection before execution

After Spec, plan, and Autonomy Envelope are approved, show a non-blocking default selection:

```text
Execution Mode

● Unattended — Default
  Continue through the approved development lifecycle to READY_FOR_UAT.
  Notify only when blocked or complete.

○ Attended
  Pause at scheduled review checkpoints selected below.

[Start with Unattended] [Configure Attended]
```

Rules:

1. Unattended is preselected, but SAP write must still require an explicit `APPROVE AND START` command.
2. Do not ask for mode selection again when a repository/user default already exists; show the resolved mode in the execution summary with a `Change` action.
3. A mandatory organization/project policy may impose a minimum attended review level for a risk class.
4. The Agent may recommend a stricter level but must distinguish a recommendation from a policy requirement.
5. Store the resolved policy and its source in the execution contract.

```yaml
interaction_resolution:
  execution_mode: unattended
  review_level: not_applicable
  resolved_from: user_default
  agent_recommendation:
    execution_mode: attended
    review_level: guided
    reason:
      - ddic_persistent_change
      - authorization_logic
  mandatory_minimum: none
  owner_override: accepted_unattended
```

## 94. Attended review levels

### 94.1 Standard

Low-interruption milestone review.

Pause after:

- approved plan baseline
- implementation complete
- final verification and UAT pack

Do not pause after every slice. Material architecture or policy issues still go to Decision Inbox immediately.

### 94.2 Guided

Development-cycle review.

Pause after:

- impact analysis
- test design
- each completed vertical slice
- full regression
- UAT pack

Each slice card shows changed objects, source diff summary, acceptance criteria, test results, ATC delta, audit verdict, residual risks, and next slice.

### 94.3 Controlled

Engineering-gate review.

Pause before:

- first write to each production object
- activation of a newly created or materially changed object
- integration test with permitted SAP-side test data

Pause after:

- architecture/Clean Core decision
- security, authorization, LUW, and locking design
- test plan
- ATC/CVA and independent audit

Routine syntax repairs, deterministic local test updates, documentation, and read-only analysis may continue within the approved slice.

### 94.4 Strict

State-changing operation review.

Pause before:

- every source write batch
- every activation batch
- SAP-side test-data creation
- integration side effect
- design-changing repair
- source-drift rebase
- replay after restart when the previous side effect is not conclusively reconciled
- ATC exemption, pragma, or pseudo-comment proposal

Strict does not pause read/search/where-used or deterministic evidence rendering. Irreversible and production actions remain prohibited rather than merely reviewable.

### 94.5 Custom

Policy-defined review using repository, project, or task rules.

```yaml
review_level:
  name: custom
  pause_on:
    - public_interface_change
    - ddic_persistent_change
    - authorization_change
    - clean_core_debt
    - unreleased_api_usage
    - integration_contract_change
    - atc_priority_1_or_2
    - source_drift
    - repair_budget_exceeded
  continue_on:
    - private_method_refactor
    - local_test_class_change
    - syntax_repair
    - focused_test_rerun
    - documentation_update
```

## 95. Review Queue is separate from Decision Inbox

### Decision Inbox

Use only when human authority or judgment is required:

- business rule or scope
- architecture trade-off
- policy exception
- irreversible/high-risk boundary
- unresolved source conflict
- missing released API/extension point
- tool/access blocker

### Review Queue

Use only for scheduled attended checkpoints:

- plan review
- impact review
- test-plan review
- slice completion
- engineering gate
- final verification
- UAT pack review

A scheduled review is not a blocker defect and must not be counted in blocked-time metrics.

```yaml
review_item:
  review_id: REV-0018
  run_id: RUN-CR1024-001
  review_level: guided
  checkpoint_type: slice_completion
  slice_id: S04
  revision: 2
  state: OPEN
  snapshot:
    spec_revision: SPEC-R007
    source_hashes:
      ZCL_SO_ALLOCATION: sha256:...
    evidence_ids:
      - EV-UNIT-0041
      - EV-ATC-0042
      - EV-AUDIT-0043
  actions:
    - approve_and_continue
    - request_changes
    - inspect_diff
    - take_over
    - switch_to_unattended
```

## 96. Review item user actions

### Approve and Continue

Resume from the next legal state. Bind approval to review revision, evidence snapshot, source hashes, and spec revision.

### Request Changes

Require a concise comment plus impacted acceptance criterion or object when known. Transition to `RUNNING.REPAIRING`; do not alter the approved business outcome silently.

### Inspect Diff/Evidence

Read-only action. Does not change Run state or extend the lease by itself.

### Take Over

Transition through `PAUSING` to `PAUSED`. Release Agent write ownership after a safe checkpoint. Produce a handover packet containing current hashes, locks, TR/task, incomplete steps, test status, and resume requirements.

### Switch to Unattended

Allowed only at a safe checkpoint with no unresolved Decision Inbox item, valid autonomy envelope, fresh evidence, and no active side effect.

## 97. Review lifecycle and state machine additions

Add states without duplicating the V6 engine:

```text
RUNNING.<substate>
  -> REVIEW_PENDING
  -> REVIEWING
       -> REVIEW_APPROVED -> RUNNING.<next-substate>
       -> CHANGES_REQUESTED -> RUNNING.REPAIRING
       -> TAKEOVER_REQUESTED -> PAUSING -> PAUSED
       -> MODE_SWITCH_REQUESTED -> RECONFIGURING

RECONFIGURING
  -> RUNNING.<resume-substate>
  -> REVIEW_PENDING
  -> BLOCKED
```

Review lifecycle:

```text
OPEN -> VIEWED -> ANSWERED -> VALIDATING -> APPLIED
OPEN -> SUPERSEDED
OPEN -> WITHDRAWN
ANSWERED -> REJECTED_STALE
```

Review approval becomes stale when source, spec, relevant dependency, target, guardrail profile, or evidence snapshot changes.

## 98. Safe mode switching

### Unattended to Attended

1. Finish or time out the current atomic tool operation.
2. Persist command result and reconcile SAP state.
3. Enter `PAUSING` and create checkpoint.
4. Resolve requested review level.
5. Enter `REVIEW_PENDING` with a current-state review card.

Never stop midway through a source write or activation request.

### Attended to Unattended

Require:

- current review approved
- no open blocking Decision Inbox item
- valid lease
- autonomy envelope covers remaining work
- no mandatory repository/project review gate remains
- explicit confirmation that the run stops at `READY_FOR_UAT`

Persist a policy revision and resume only after it validates against the current state.

### Changing attended level

Increasing review intensity can apply at the next safe checkpoint. Decreasing it requires validation against minimum policy and records the owner override when applicable.

## 99. Review timeout policy

Attended Mode must never silently turn into Unattended Mode.

Default behavior:

- send one `REVIEW_PENDING` notification
- optional reminder after 4 business hours
- one reminder per business day afterward
- keep the run in a safe checkpoint
- renew no write lease while waiting
- on runtime lease expiry, transition to `PAUSED_SAFE`

Never auto-approve because the Project Owner did not respond.

A project may define `auto_pause_after`, but not `auto_continue_after`, for scheduled reviews.

## 100. Batch approval and approval-fatigue controls

Batch approval is allowed only for review items that are:

- reversible
- within one approved slice
- based on the same spec and source snapshot
- not security, authorization, DDIC-persistent, integration-contract, Clean Core exception, source-drift, or production related

Maximum suggested batch size: five review items.

Never batch:

- Decision Inbox choices
- policy exceptions
- irreversible actions
- ATC/CVA exemption proposals
- source-drift resolutions
- cross-client operations
- external side effects

Show deltas from the previous approved checkpoint rather than repeating the entire project history.

## 101. Risk recommendation versus mandatory policy

Keep three concepts distinct:

```yaml
review_governance:
  selected_by_owner: standard
  recommended_by_agent: controlled
  minimum_required_by_policy: guided
  effective_level: guided
```

Resolution priority:

```text
Mandatory organization/project policy
> explicit task selection that is at least the minimum
> repository default
> user default
> system default (unattended)
```

The recommendation must explain concrete triggers, for example:

- persisted DDIC change
- financial posting
- authorization logic
- public OData/RAP contract
- unreleased API request
- external integration
- insufficient automated testability

Do not increase interruption merely because the task is large. Use actual SAP and delivery risks.

## 102. Metrics separation

Track mode effectiveness without rewarding excessive checkpoints.

```yaml
interaction_metrics:
  execution_mode: attended
  review_level: guided
  scheduled_reviews: 7
  owner_changes_requested: 2
  average_review_wait_minutes: 36
  blocking_decisions: 1
  agent_repair_loops: 3
  stale_reviews: 1
  mode_switches: 1
  unattended_runtime_minutes: 184
```

Separate:

- execution time
- owner review wait time
- blocker wait time
- recovery time
- AI repair time

This prevents attended reviews from being misclassified as Agent failure or technical blockage.

## 103. Notification policies

### Unattended

Notify:

- run started
- genuine blocking decision
- `READY_FOR_UAT` or terminal safe state

Do not notify routine progress unless opted in.

### Attended

Notify:

- review item created
- genuine blocking decision
- review became stale due to source/spec change
- `READY_FOR_UAT` or terminal safe state

Do not duplicate a scheduled review as a Decision Inbox notification.

## 104. UX wording

Use this professional wording:

```text
Execution Mode
- Unattended
- Attended

Attended Review Level
- Standard
- Guided
- Controlled
- Strict
- Custom
```

Descriptions:

- **Standard**: Review key delivery milestones.
- **Guided**: Review each development cycle or vertical slice.
- **Controlled**: Approve important SAP engineering gates.
- **Strict**: Approve each state-changing SAP operation batch.
- **Custom**: Apply project-defined review rules.

Machine names:

```yaml
standard: milestone_review
guided: development_cycle_review
controlled: engineering_gate_review
strict: state_change_controlled_review
custom: policy_based_review
```

## 105. Recommended default configuration

```yaml
interaction_policy:
  system_default:
    execution_mode: unattended
    notification_policy: blocked_or_complete

  attended_levels:
    standard:
      pause_after:
        - plan_baseline
        - implementation_complete
        - final_verification

    guided:
      pause_after:
        - impact_analysis
        - test_design
        - each_slice
        - final_regression

    controlled:
      pause_before:
        - first_write_per_production_object
        - material_activation
        - integration_test_with_sap_data
      pause_after:
        - architecture_and_guardrails
        - test_plan
        - atc_cva_and_audit

    strict:
      pause_before:
        - source_write_batch
        - activation_batch
        - sap_test_data_creation
        - integration_side_effect
        - design_changing_repair
        - source_drift_rebase
        - uncertain_replay_after_restart
        - exemption_or_suppression

    custom:
      source:
        - organization_policy
        - repository_policy
        - task_override

  switching:
    allowed: true
    apply_at: safe_checkpoint

  review_timeout:
    auto_continue: false
    reminder_after_business_hours: 4
    lease_expiry_state: PAUSED_SAFE
```

## 106. V7 recheck findings

The current unattended design remains sound. It should not be weakened by adding routine progress prompts. The following improvements are necessary and are included in V7:

1. Separate execution mode from review level.
2. Keep Unattended as the preselected default while still requiring explicit start approval.
3. Separate Review Queue from Decision Inbox.
4. Add `REVIEW_PENDING`, `REVIEWING`, and `RECONFIGURING` states.
5. Make mode switching safe-checkpoint based.
6. Never auto-continue when an attended review times out.
7. Bind review approval to source/spec/evidence revisions.
8. Add takeover and hand-back behavior.
9. Control batch approval to prevent approval fatigue.
10. Distinguish owner selection, Agent recommendation, and mandatory project policy.
11. Separate review wait time from technical blocker and Agent execution metrics.
12. Use Standard, Guided, Controlled, Strict, and Custom as professional review-level wording.

No separate Attended Agent or duplicate Skill is needed. Both modes must use the same SAP delivery engine, guardrails, durable state, recovery controller, evidence model, and final UAT boundary.

## 107. V7 final position

The product model is:

```text
Auto ABAP Delivery
├─ Unattended — default, blocked-or-complete interaction
└─ Attended
   ├─ Standard
   ├─ Guided
   ├─ Controlled
   ├─ Strict
   └─ Custom
```

Unattended optimizes for Project Owner focus. Attended optimizes for visibility, learning, governance, and confidence. Neither mode changes SAP quality requirements or permits production actions. They differ only in when the same evidence-backed lifecycle pauses for human review.


---

# Extension V8: Trust-Calibrated Autonomous Engineering

> V8 changes the initial default for unqualified scope to **Attended / Standard**, while preserving **Unattended** as the target default for scopes that have demonstrated safe delivery. It also adds engineering judgment controls derived from practical agentic ABAP work: reuse-first discovery, simplicity review, test-adequacy audit, consumer-impact analysis, approved project engineering memory, qualified-reviewer routing, and explicit accountability.

## 108. Trust-calibrated default

A single global default is too coarse. Resolve the effective mode by qualification scope:

```yaml
default_policy:
  unqualified_scope:
    execution_mode: attended
    review_level: standard
  qualified_scope:
    execution_mode: unattended
    review_level: not_applicable
  critical_scope:
    execution_mode: attended
    minimum_review_level: controlled
```

Qualification is scoped to Agent version, Skill version, MCP profile/hash, SAP SID/client, package pattern, object types, guardrail profile, and relevant operation classes. Trust in one package or object type must not automatically transfer to another.

Recommended initial qualification evidence:

- 3-5 completed attended runs in the same scope
- zero wrong-system/client writes
- zero unauthorized actions or source overwrite incidents
- zero stale evidence/review approvals accepted
- zero escaped ATC priority 1/2 findings
- zero transport-clutter incidents
- UAT first-pass rate at least 80 percent

These are project defaults, not SAP standards. Organization policy may strengthen them.

## 109. AI as delegated ABAP developer

In qualified Unattended mode, AI performs the developer operations that a human would otherwise approve interactively:

- create approved objects
- edit approved source
- assign/touch objects in the approved transport task
- syntax check and activate
- build and run ABAP Unit/test doubles
- run ATC/CVA/readiness checks
- repair, regress, audit, document, and prepare UAT

All operations remain bounded by DEV target, client, package/TR/task, object patterns, action classes, lease, source hash, lock, evidence, and stop conditions. Transport release/import and production actions remain human authority.

## 110. Attended levels and operation behavior

| Level | Create/write | Activate | Approved transport task | Review pattern |
|---|---|---|---|---|
| Standard | AI acts after approved plan | AI acts | AI acts within scope | Plan, implementation complete, final verification |
| Guided | AI acts per approved slice | AI acts per slice | reported per slice | Impact, tests, every slice, regression |
| Controlled | after engineering gate | before material activation | object set reviewed first | architecture/test/security/ATC gates |
| Strict | approval before each state-changing batch | approval each batch | approval each batch | every state-changing batch |
| Custom | policy-defined | policy-defined | policy-defined | project rules |

Transport touch means object/task assignment and dependency inspection inside the approved development TR/task. It never includes release, import, forwarding, or production deployment.

## 111. Reuse-first discovery

Before creating a new object, inspect:

1. SAP standard/configuration capability
2. released API or extension point
3. existing project object and approved library
4. similar implementation and architecture decision
5. extend/reuse/retire/build trade-off

Create `reuse-assessment.yaml`. Existing code is a candidate, not automatic proof of correctness; reject legacy anti-patterns and unreleased coupling.

## 112. Simplicity and over-engineering gate

Before accepting implementation, justify each new global object, public interface, wrapper, abstraction layer, and generated artifact. Prefer the smallest maintainable solution. Check whether a private method, existing component, standard API, or extension is sufficient. Record speculative reuse and unnecessary delegation layers as audit findings.

## 113. Test adequacy audit

Passing tests are insufficient. An independent test-adequacy review must assess:

- happy, negative, validation-failure, exception, authorization-denied, alternative-flow, boundary, concurrency/idempotency, and regression scenarios as applicable
- test-double fidelity
- assertion strength and defect-detection ability
- untested branches and manual-UAT mapping
- whether the original bug test failed before the fix when feasible

## 114. Consumer-impact analysis

Require consumer-impact analysis for CDS, RAP projections/behaviors/services, OData, RFC/BAPI, IDoc, persisted DDIC, public classes/interfaces, forms, events, and external contracts. Identify additive/removal/semantic changes, consumers, compatibility, versioning, regression tests, and rollout sequence.

## 115. Approved project engineering memory

Load only reviewed repository knowledge:

```text
project-knowledge/
  ABAP_STYLE.md
  NAMING_CONVENTIONS.md
  APPROVED_PATTERNS.md
  REUSABLE_COMPONENTS.md
  RELEASED_API_POLICY.md
  TESTING_STANDARD.md
  CLEAN_CORE_POLICY.md
  FORBIDDEN_PATTERNS.md
  ARCHITECTURE_DECISIONS/
```

AI may produce `lesson-candidate` proposals but must not silently rewrite approved engineering memory.

## 116. Reviewer competency routing

An attended checkpoint is useful only when an appropriately qualified role reviews it. Define required reviewer roles by checkpoint, for example senior ABAP/Clean Core for architecture, Security for authorization, Functional Owner/Test Engineer for test scenarios, ABAP Developer for source diff, and Integration Owner for public contracts. Missing competency creates `REVIEWER_REQUIRED`, not technical `BLOCKED`.

## 117. Accountability matrix

Record AI-executed objects/checks separately from accountable human roles:

- technical reviewer
- functional/UAT owner
- deployment approver
- production authority

Development approval never inherits production authority. AI is executor/orchestrator, not production accountable owner.

## 118. V8 completion additions

`READY_FOR_UAT` additionally requires:

- reuse assessment for new global objects
- simplicity verdict without unresolved `REWORK`
- test adequacy verdict
- consumer-impact report when applicable
- project engineering profile revision used
- required reviewer competency satisfied or explicitly deferred to UAT/manual review
- accountability matrix populated
- autonomy qualification record updated from actual run outcome

## 119. V8 final model

```text
Unqualified scope -> Attended Standard (initial default)
Critical scope    -> Attended Controlled minimum
Qualified scope   -> Unattended eligible/default by policy
```

This retains Long-Run ABAP AI as the destination while keeping Developer and Agent in the loop until evidence supports broader autonomy.
