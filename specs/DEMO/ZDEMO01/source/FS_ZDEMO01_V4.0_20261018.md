**CHANGE REQUEST**

**For Lucky Union Foods Co., Ltd.**

**Split Batch at External WH and Report**

**(ZDEMO01)**

**Document Version: V1.0**

**Date: 23.04.2026**

Approval Signature: MM Functional Specification

**Lucky Union Foods Company Limited**

|     |     |
| --- | --- |
|     |     |
| Approved by: Khun Somchart Chalermthong |     |
| Position: Project Manager |     |
| Approved Date: |     |
|     |     |
|     |     |
|     |     |
|     |     |
|     |     |

Document Change Control

This section provides control for the development and distribution of revisions to the Project Charter up to the point of approval. The Project Charter does not change throughout the project life cycle, but rather is developed at the beginning of the project (immediately following project initiation approval, and in the earliest stages of project planning). The Project Charter provides an ongoing reference for all project stakeholders. The table below includes the revision number (defined within your Documentation Plan Outline), the date of update/issue, the author responsible for the changes, and a brief description of the context and/or scope of the changes in that revision.

|     |     |     |     |
| --- | --- | --- | --- |
| **Revision Number** | **Date of Issue** | **Author(s)** | **Brief Description of Change** |
| 1.0 | 23.04.2026 | Nichchar R. | Initial Document |
| 2.0 | 17.10.2026 | Nichchar R. | CR support FG process |

**Table of Contents**

[1\. Development Summary 5](#_Toc52213582)

[2\. Functional Requirements 6](#_Toc52213583)

[2.1. Authorization 6](#_Toc52213584)

[2.2. Prerequisites / Assumptions 6](#_Toc52213585)

[2.3. Detailed Program Logic 7](#_Toc52213586)

[2.4. Report / Form 25](#_Toc52213587)

[3\. Error Handling 29](#_Toc52213588)

[4\. Testing 29](#_Toc52213589)

[5\. Appendix 29](#_Toc52213590)

# Development Summary

|     |     |     |     |
| --- | --- | --- | --- |
| **Object ID** | ZDEMO01 |     |     |
| **Object Name** | ZDEMO01 |     |     |
| **Program Name** | Goods Receipt at External WH and Report |     |     |
| **Existing program related (If any)** | N/A |     |     |
| **Module** | MM  |     |     |
| **Menu Path** | ZDEMO01 |     |     |
| **WRICEF Type** | Workflow<br><br> Report<br><br> Interface<br><br> Conversion<br><br> Enhancement<br><br> Form | **Complexity** | Very High<br><br> High<br><br> Medium<br><br> Low |
| **Statutory** | Yes  No | **Frequency** | Ad hoc |
| **Processing type** | Online<br><br> Background | **Schedule Job** | No<br><br> Yes, (Please define) |
| **Transaction Code** | ZDEMO01 | **Develop By** | Nichchar Raksasri |
| **Requested by** |     | **Request Date** | 18 October 2026 |

# Functional Requirements

เพิ่มขั้นตอนการทำงานของโปรแกรมลงไปใน standard transaction - Goods Movement (MIGO) กรณีที่มีการทำรับสินค้าจากใบสั่งซื้อเข้าคลังนอก เช่น Pacific หรือ Rakchai จะต้องมีการอัพเดทข้อมูลการรับหรือยกเลิกรับสินค้าลง Customize Table เพื่อทำการ Split Batch ตาม MFG Date และอัพเดทข้อมูลอื่นๆเพิ่มเติม ได้แก่ เลขที่ใบฝาก วันที่ฝาก และ หมายเหตุต่างๆ จากนั้นยังสามารถพิมพ์เอกสารใบฝากห้องเย็นเพือส่งให้ห้องเย็น และพิมพ์เอกสารใบเบิกจากห้องเย็น และยังใช้งานโปรแกรมในการโอนสินค้ากลับจากห้องเย็นมายัง HQ หรือ LC โดยเลือกจากเลขที่ Batch ที่ Split เพื่อให้ได้ข้อมูลการทำ Goods Transfer MVT 311 จากห้องเย็นกลับมา DEMO ทั้งนี้เอกสารจะถูกพิมพ์ลงกระดาษขนาด A4 ด้วยรูปแบบที่กำหนด

## Authorization

|     |     |     |
| --- | --- | --- |
| **Object** | **Description** | **Value** |
| M_MSEG_WMB | Material Documents: Plant | Activity:\*<br><br>Plant: From selection screen |
| M_MSEG_WWA | Goods Movements: Plant | Activity:\*<br><br>Plant: From selection screen |
| M_MSEG_LGO | Goods Movements: Storage Location | Activity:\*<br><br>Storage Location: From selection screen |

## Prerequisites / Assumptions

เพิ่มเงื่อนไขในการตรวจสอบและอัพเดทข้อมูลลง Z-table ในระดับ Item ของหน้า MIGO สำหรับเงื่อนไขต่อไปนี้

### GODYNPRO-GOACTION = “A01” and GODYNPRO-REFDOC = “R01” and GOITEM-BWART = “101” and GOITEM-LGORT is found in ZCAT001 \[ZCAT001-LGORT = 0WR0, 0WP0\]เมื่อ User กด SAVE และได้ Material Document ให้นำข้อมูลจาก MATDOC มา Update ZMMT010 และ ZMMT010-STATUS = N (NEW)GODYNPRO-GOACTION = “A08” and GODYNPRO-REFDOC = “R10” and GOITEM-BWART = “311” and GOITEM-LGORT is found in ZCAT001 \[ZCAT001-LGORT = 0WR0, 0WPC, 0WIS\] and MARA-MTART = ZFINเมื่อ User กด SAVE และได้ Material Document ให้นำข้อมูลจาก MATDOC มา Update ZMMT010 และ ZMMT010-STATUS = N (NEW) นำข้อมูลจาก MCHA-HSDAT (MATDOC-MATNR = MCHA-MATNR และ MATDOC-CHARG = MCHA-CHARG) มาอัพเดท ZMMT010-HSDAT และ ZMMT010-HSDAT_NGODYNPRO-GOACTION = “A03” and GODYNPRO-REFDOC = “R02” and GOITEM-BWART = “102” and GOITEM-LGORT is found in ZCAT001 \[ZCAT001-LGORT = 0WR0, 0WP0\]เมื่อ User กด CHECK, SAVE ให้นำข้อมูล PO, PO Item, material, batch, plant, sloc จาก MIGO มาตรวจสอบใน ZMMT010 ถ้า ZMMT010-STATUS = N (NEW) และ จำนวนในเอกสารที่ทำการยกเลิกเท่ากับ ZMMT010-MENGE ให้ลบรายการนี้ออกจาก ZMMT010ถ้า ZMMT010-STATUS = N (NEW) แต่จำนวนในเอกสารที่ทำการยกเลิก ไม่เท่ากับ ZMMT010-MENGE ให้ Update ZMMT010-MENGE ด้วยจำนวนที่เหลือหลังยกเลิกถ้า ZMMT010-STATUS = S (SPLIT) และต้องการยกเลิกรายการ ให้โปรแกรมแสดงข้อความ “มีข้อมูล PO, PO Item และ Batch ที่ Split แล้วอยู่ใน ZMMT010 ให้ User แก้ไขก่อน”ถ้า ZMMT010-STATUS = U (UPDATE) และต้องการยกเลิกรายการ ให้โปรแกรมแสดงข้อความ “มีการ Update กลับจากคลังนอกแล้วใน ZMMT010 ให้ User ตรวจสอบอีกครั้ง”GODYNPRO-GOACTION = “A03” and GODYNPRO-REFDOC = “R02” and GOITEM-BWART = “312” and GOITEM-LGORT is found in ZCAT001 \[ZCAT001-LGORT = 0WR0, 0WPC, 0WIS\] and MARA-MTART = ZFIN เมื่อ User กด CHECK, SAVE ให้นำข้อมูล material, batch, plant, sloc จาก MIGO มาตรวจสอบใน ZMMT010 ถ้า ZMMT010-STATUS = N (NEW) และ จำนวนในเอกสารที่ทำการยกเลิกเท่ากับ ZMMT010-MENGE ให้ลบรายการนี้ออกจาก ZMMT010ถ้า ZMMT010-STATUS = N (NEW) แต่จำนวนในเอกสารที่ทำการยกเลิก ไม่เท่ากับ ZMMT010-MENGE ให้ Update ZMMT010-MENGE ด้วยจำนวนที่เหลือหลังยกเลิกถ้า ZMMT010-STATUS = U (UPDATE) และต้องการยกเลิกรายการ ให้โปรแกรมแสดงข้อความ “มีการ Update กลับจากคลังนอกแล้วใน ZMMT010 ให้ User ตรวจสอบอีกครั้ง”GODYNPRO-GOACTION = “A03” and GODYNPRO-REFDOC = “R02” and GOITEM-BWART = “123” and GOITEM-LGORT is found in ZCAT001 \[ZCAT001-LGORT = 0WR0, 0WP0\]เมื่อ User กด CHECK, SAVE ให้นำข้อมูล PO, PO Item, material, batch, plant, sloc จาก MIGO มาตรวจสอบใน ZMMT010 ถ้า ZMMT010-STATUS = N (NEW) ให้ Update ZMMT010-MENGE ด้วยการนำจำนวนที่ทำรายการไปบวกเพิ่มใน ZMMT010-MENGEถ้า ZMMT010-STATUS = S (SPLIT) ให้โปรแกรมแสดงข้อความ “มีข้อมูล PO, PO Item และ Batch ที่ Split แล้วอยู่ใน ZMMT010 ให้ User แก้ไขก่อน”ถ้า ZMMT010-STATUS = U (UPDATE) ให้โปรแกรมแสดงข้อความ “มีการ Update กลับจากคลังนอกแล้วใน ZMMT010 ให้ User ตรวจสอบอีกครั้งGODYNPRO-GOACTION = “A02” and GODYNPRO-REFDOC = “R02” and GOITEM-BWART = “122” and GOITEM-LGORT is found in ZCAT001 \[ZCAT001-LGORT = 0WR0, 0WP0\]เมื่อ User กด CHECK, SAVE ให้นำข้อมูล PO, PO Item, material, batch, plant, sloc จาก MIGO มาตรวจสอบใน ZMMT010 ถ้า ZMMT010-STATUS = N (NEW) และ จำนวนในเอกสารที่ทำการยกเลิกเท่ากับ ZMMT010-MENGE ให้ลบรายการนี้ออกจาก ZMMT010ถ้า ZMMT010-STATUS = N (NEW) แต่จำนวนในเอกสารที่ทำการยกเลิก ไม่เท่ากับ ZMMT010-MENGE ให้ Update ZMMT010-MENGE ด้วยจำนวนที่เหลือหลังยกเลิกถ้า ZMMT010-STATUS = S (SPLIT) และต้องการยกเลิกรายการ ให้โปรแกรมแสดงข้อความ “มีข้อมูล PO, PO Item และ Batch ที่ Split แล้วอยู่ใน ZMMT010 ให้ User แก้ไขก่อน”ถ้า ZMMT010-STATUS = U (UPDATE) และต้องการยกเลิกรายการ ให้โปรแกรมแสดงข้อความ “มีการ Update กลับจากคลังนอกแล้วใน ZMMT010 ให้ User ตรวจสอบอีกครั้ง”

เพิ่มเงื่อนไขในการอัพเดทข้อมูลลง Z-table ZMMT014และ ZMMT010 สำหรับเงื่อนไขต่อไปนี้

หากมีการ Cancel Goods issue ref. DO ด้วย T-code: VL09 (Movement Type = 602) หรือ ทำ Goods Return ด้วย T-code = VL02n (Movement Type = 653/655) ให้แก้ไขโปรแกรมที่

BAdI MB_DOCUMENT_BADI → Method MB_DOCUMENT_UPDATE

สำหรับ update Z-table พร้อมการบันทึก **Reversal Material Document จาก VL09** และ **Goods Return จาก VL02n** โดยให้อัพเดท ZMMT014 History Log for MVT601 of Split batch at External WH and Report ด้วยเงื่อนไขดังนี้

แล้วเข้าเงื่อนไขดังต่อไปนี้

Material code ใน VL09 หรือ VL02n = ZMMT013-MATNR

Batch ใน VL09 หรือ VL02n = ZMMT013-CHARG

Plant ใน VL09 หรือ VL02n = ZMMT013-WERKS

Storage location ใน VL09 หรือ VL02n =ZMMT013-LGORT

DO ใน VL09 หรือ VL02n = ZMMT013-VBELN

DO Item ใน VL09 หรือ VL02n = ZMMT013-POSNR

และให้โปรแกรมนำ จำนวนที่ถูกยกเลิกมาบวกกลับไปที่ ZMMT010-MENGE_PD (GR Pending QTY) ลบออกจากMENGE_GI (GI Qty (Collect))

และให้โปรแกรมนำ QTY ของ MM Doc ที่เกิดจาก VL09 หรือ VL02n มาลบจาก ZMMT013-MENGE_GI

Maintain Standard Text สำหรับออกฟอร์ม แยกข้อความตาม Storage Location และตำแหน่งต่างๆในฟอร์ม ได้แก่

|     |     |     |     |
| --- | --- | --- | --- |
| **Standard Text** | **Position** | **Storage Location** | **Value** |
| ZMMF004_TEL_EMAIL | ใบฝากของ, ใบเบิกคลังนอก | \*  | TEL.: 66 (0) 3449 0009-12, 66 (0) 3449 0330-4 FAX: 66 (0) 3449 0008<br><br>MARKETING FAX: 66 (0) 3449 0391 www.luckyunionfoods.com |
| ZMMF004_RECEIVER_0WR0 | ใบฝากของ – เรียน | 0WR0 | บริษัท รักชัยห้องเย็น จำกัด |
| ZMMF004_RECEIVER_0WP0 | ใบฝากของ – เรียน | 0WP0 | บริษัท แปซิฟิค ห้องเย็น |
| ZMMF004_SENDER_0WR0 | ใบฝากของ – จาก: | 0WR0 | แผนกคลังสินค้า |
| ZMMF004_SENDER_0WP0 | ใบฝากของ – จาก: | 0WP0 | แผนกคลังสินค้า |
| ZMMF004_FOOTER_0WR0 | ใบฝากของ – คำลงท้าย | 0WR0 | ทางบริษัทฯ ขอขอบคุณอย่างยิ่งที่<br><br>บริษัท รักชัยห้องเย็น จำกัด<br><br>ให้บริการเป็นอย่างดี |
| ZMMF004_FOOTER_0WP0 | ใบฝากของ – คำลงท้าย | 0WP0 | ทางบริษัทฯ ขอขอบคุณอย่างยิ่งที่<br><br>บริษัท แปซิฟิค ห้องเย็น ให้บริการเป็นอย่างดี |
| ZMMF004_RECEIVER_ISSUE_0WR0 | ใบเบิกคลังนอก – เรียน | 0WR0 | บริษัท รักชัยห้องเย็น จำกัด |
| ZMMF004_RECEIVER_ISSUE_0WP0 | ใบเบิกคลังนอก – เรียน | 0WP0 | บริษัท แปซิฟิค ห้องเย็น |
| ZMMF004_SENDER_ISSUE_0WR0 | ใบเบิกคลังนอก– จาก: | 0WR0 | แผนกคลังสินค้า |
| ZMMF004_SENDER_ISSUE_0WP0 | ใบเบิกคลังนอก – จาก: | 0WP0 | แผนกคลังสินค้า |
| ZMMF004_FOOTER_ISSUE_0WR0 | ใบฝากของ – คำลงท้าย | 0WR0 | ทางบริษัทฯ ขอขอบคุณอย่างยิ่งที่<br><br>บริษัท รักชัยห้องเย็น จำกัด<br><br>ให้บริการเป็นอย่างดี |
| ZMMF004_FOOTER_ISSUE_0WP0 | ใบฝากของ – คำลงท้าย | 0WP0 | ทางบริษัทฯ ขอขอบคุณอย่างยิ่งที่<br><br>บริษัท แปซิฟิค ห้องเย็น ให้บริการเป็นอย่างดี |

|     |     |     |     |
| --- | --- | --- | --- |
| **Standard Text** | **Position** | **Storage Location** | **Value** |
| ZMMF005_TEL_EMAIL | ใบฝากของ, ใบเบิกคลังนอก | \*  | TEL.: 66 (0) 3449 0009-12, 66 (0) 3449 0330-4 FAX: 66 (0) 3449 0008<br><br>MARKETING FAX: 66 (0) 3449 0391 www.luckyunionfoods.com |
| ZMMF005_RECEIVER_0WR0 | ใบฝากของ – เรียน | 0WR0 | บริษัท รักชัยห้องเย็น จำกัด |
| ZMMF005_RECEIVER_0WPC | ใบฝากของ – เรียน | 0WPC | บริษัท แปซิฟิคเชียงใหม่ ห้องเย็น |
| ZMMF005_RECEIVER_0WIS | ใบฝากของ – เรียน | 0WIS | บริษัท ไอเทล สงขลา จำกัด |
| ZMMF005_SENDER_0WR0 | ใบฝากของ – จาก: | 0WR0 | แผนกคลังสินค้า |
| ZMMF005_SENDER_0WPC | ใบฝากของ – จาก: | 0WPC | แผนกคลังสินค้า |
| ZMMF005_SENDER_0WIS | ใบฝากของ – จาก: | 0WIS | แผนกคลังสินค้า |
| ZMMF005_FOOTER_0WR0 | ใบฝากของ – คำลงท้าย | 0WR0 | ทางบริษัทฯ ขอขอบคุณอย่างยิ่งที่<br><br>บริษัท รักชัยห้องเย็น จำกัด<br><br>ให้บริการเป็นอย่างดี |
| ZMMF005_FOOTER_0WPC | ใบฝากของ – คำลงท้าย | 0WPC | ทางบริษัทฯ ขอขอบคุณอย่างยิ่งที่<br><br>บริษัท แปซิฟิคเชียงใหม่ ห้องเย็น ให้บริการเป็นอย่างดี |
| ZMMF005_FOOTER_0WIS | ใบฝากของ – คำลงท้าย | 0WIS | ทางบริษัทฯ ขอขอบคุณอย่างยิ่งที่<br><br>บริษัท ไอเทล สงขลา จำกัด ให้บริการเป็นอย่างดี |
| ZMMF005_RECEIVER_ISSUE_0WR0 | ใบเบิกคลังนอก – เรียน | 0WR0 | บริษัท รักชัยห้องเย็น จำกัด |
| ZMMF005_RECEIVER_ISSUE_0WPC | ใบเบิกคลังนอก – เรียน | 0WPC | บริษัท แปซิฟิคเชียงใหม่ ห้องเย็น |
| ZMMF005_RECEIVER_ISSUE_0WIS | ใบเบิกคลังนอก – เรียน | 0WIS | บริษัท ไอเทล สงขลา จำกัด |
| ZMMF005_SENDER_ISSUE_0WR0 | ใบเบิกคลังนอก– จาก: | 0WR0 | แผนกคลังสินค้า |
| ZMMF005_SENDER_ISSUE_0WPC | ใบเบิกคลังนอก – จาก: | 0WPC | แผนกคลังสินค้า |
| ZMMF005_SENDER_ISSUE_0WIS | ใบเบิกคลังนอก – จาก: | 0WIS | แผนกคลังสินค้า |
| ZMMF005_FOOTER_ISSUE_0WR0 | ใบฝากของ – คำลงท้าย | 0WR0 | ทางบริษัทฯ ขอขอบคุณอย่างยิ่งที่<br><br>บริษัท รักชัยห้องเย็น จำกัด<br><br>ให้บริการเป็นอย่างดี |
| ZMMF005_FOOTER_ISSUE_0WPC | ใบฝากของ – คำลงท้าย | 0WPC | ทางบริษัทฯ ขอขอบคุณอย่างยิ่งที่<br><br>บริษัท แปซิฟิคเชียงใหม่ ห้องเย็น ให้บริการเป็นอย่างดี |
| ZMMF005_FOOTER_ISSUE_0WIS | ใบฝากของ – คำลงท้าย | 0WIS | ทางบริษัทฯ ขอขอบคุณอย่างยิ่งที่<br><br>บริษัท ไอเทล สงขลา จำกัด ให้บริการเป็นอย่างดี |

## Detailed Program Logic

### Customize Table and Structure

Table : ZMMT010

Short Text : Log of Split batch at External WH and Report

|     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
| **Field** | **Key** | **Data Element** | **Data Type** | **Length** | **Short Text** | **Example** |
| BUDAT | X   | MATDOC-BUDAT | DATS | 8   | Posting Date | 18.04.2026 |
| MBLNR | X   | MATDOC-MBLNR | CHAR | 10  | Material Document | 5000002669 |
| ZEILE | X   | MATDOC-ZEILE | NUM | 4   | Material Document Item | 1   |
| MJAHR | X   | MATDOC-MJAHR | NUM | 4   | Material Document Year | 2026 |
| BKTXT | &nbsp; | MATDOC-BKTXT | CHAR | 25  | Header Text | &nbsp; |
| XBLNR | &nbsp; | MATDOC-XBLNR | CHAR | 16  | Delivery Note | 164-Ex/2026 |
| EBELN |     | MATDOC-EBELN | CHAR | 10  | Purchasing Document | 4100002355 |
| EBELP |     | MATDOC-EBELP | NUM | 5   | Purchasing Doc Item | 10  |
| EMLIF |     | MATDOC-EMLIF | CHAR | 10  | Vendor code | &nbsp; |
| MATNR |     | MATDOC-MATNR | CHAR | 40  | Material code | RI3-N0-XXH-3 |
| SGTXT | &nbsp; | MATDOC-SGTXT | CHAR | 50  | Item Text | ONEU9187706 |
| BWTAR | &nbsp; | MATDOC-BWTAR | CHAR | 10  | Valuation Type | 2508010006 |
| CHARG |     | MATDOC-CHARG | CHAR | 10  | Batch | 2508010006 |
| HSDAT | &nbsp; | MATDOC-HSDAT | DATS | 8   | MFG main Batch | 06.12.2025 |
| VFDAT | &nbsp; | MATDOC-VFDAT | DATS | 8   | SLED main Batch | 06.12.2027 |
| CHARG_R | &nbsp; | &nbsp; | NUM | 2   | Bacth split running | 1   |
| CHARG_N | &nbsp; | &nbsp; | NUM | 12  | Batch Split | 250801000601 |
| HSDAT_N | &nbsp; | &nbsp; | DATE | 8   | MFG for batch split | 27.02.2026 |
| STATUS |     | &nbsp; | CHAR | 1   | Status (N, S, U) | New, Split, Update |
| WERKS |     | MATDOC-WERKS | CHAR | 4   | Plant | 1000 |
| LGORT |     | MATDOC-LGORT | CHAR | 4   | Source Storage Location | 0WR0 |
| MEINS |     | MATDOC-MEINS | UNIT | 3   | UoM | KG  |
| MENGE |     | MATDOC-MENGE | UNIT | 13,3 | GR Qty | 24000 |
| MENGE_INITIAL |     | MATDOC-MENGE | UNIT | 13,3 | Initial GR Qty | 24000 |
| MENGE_TF_P | &nbsp; | &nbsp; | UNIT | 13,3 | TF to DEMO Qty | 0   |
| MENGE_TF | &nbsp; | &nbsp; | UNIT | 13,3 | TF to DEMO Qty (Collect) | 0   |
| MENGE_GI | &nbsp; | &nbsp; | UNIT | 13,3 | GI Qty (Collect) | 0   |
| MENGE_PD | &nbsp; | &nbsp; | UNIT | 13,3 | GR Pending Qty | 24000 |
| TFDOC_NO | &nbsp; | &nbsp; | CHAR | 10  | เลขที่ใบฝาก | I69005264 |
| TFDOC_IM | &nbsp; | &nbsp; | NUMC | 2   | เลขที่ใบฝากระดับ Item | 1   |
| TF_DATE | &nbsp; | &nbsp; | DATE | 8   | วันที่ฝาก | 18.04.2026 |
| REMART_SIZE | &nbsp; | &nbsp; | CHAR | 25  | Remark – Size | กล่องละ 20 KG |
| REMARK | &nbsp; | &nbsp; | CHAR | 120 | Remark | Surimi Non MSC PO DEMO 4100002355 |

Table : ZMMT011

Short Text : History Log for MVT311 of Split batch at External WH and Report

|     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
| **Field** | **Key** | **Data Element** | **Data Type** | **Length** | **Short Text** | **Example** |
| BUDAT_311 | X   | MATDOC-BUDAT | DATS | 8   | Posting Date | 15.06.2026 |
| MBLNR_311 | X   | MATDOC-MBLNR | CHAR | 10  | TF Material Document | 4900002669 |
| ZEILE_311 | X   | MATDOC-ZEILE | NUM | 4   | TF Material Document Item | 1   |
| MJAHR_311 | X   | MATDOC-MJAHR | NUM | 4   | TF Material Document Year | 2026 |
| USNAM_311 | X   | MATDOC-USNAM | CHAR | 12  | User Name | WHDWOR0 |
| BUDAT | X   | MATDOC-BUDAT | DATS | 8   | Posting Date | 18.04.2026 |
| MBLNR | X   | MATDOC-MBLNR | CHAR | 10  | Material Document | 5000342111 |
| ZEILE | X   | MATDOC-ZEILE | NUM | 4   | Material Document Item | 1   |
| MJAHR | X   | MATDOC-MJAHR | NUM | 4   | Material Document Year | 2026 |
| BKTXT | &nbsp; | MATDOC-BKTXT | CHAR | 25  | Header Text | &nbsp; |
| MATNR | X   | MATDOC-MATNR | CHAR | 40  | Material code | RI3-N0-XXH-3 |
| BWART | X   | MATDOC-BWART | CHAR | 3   | Movement Type | 311 |
| CHARG | X   | MATDOC-CHARG | CHAR | 10  | Batch | 2508010006 |
| HSDAT | &nbsp; | MATDOC-HSDAT | DATS | 8   | MFG main Batch | 06.12.2025 |
| VFDAT | &nbsp; | MATDOC-VFDAT | DATS | 8   | SLED main Batch | 06.12.2027 |
| CHARG_R | &nbsp; | &nbsp; | NUM | 2   | Batch split running | 1   |
| CHARG_N | &nbsp; | &nbsp; | NUM | 12  | Batch Split | 250801000601 |
| HSDAT_N | &nbsp; | &nbsp; | DATE | 8   | MFG for batch split | 27.02.2026 |
| WERKS | X   | MATDOC-WERKS | CHAR | 4   | Plant | 1000 |
| LGORT | X   | MATDOC-LGORT | CHAR | 4   | Source SLoc. | 0WR0 |
| UMLGO | X   | MATDOC-UMLGO | CHAR | 4   | Receiving SLoc. | 0WNC |
| MEINS | X   | MATDOC-MEINS | UNIT | 3   | UoM | KG  |
| MENGE_TF_P | X   | MATDOC-MENGE | UNIT | 13,3 | TF Qty | 20  |
| TFDOC_NO | &nbsp; | &nbsp; | CHAR | 10  | เลขที่ใบฝาก | I69005264 |
| TFDOC_IM | &nbsp;X | &nbsp; | NUMC | 2   | เลขที่ใบฝากระดับ Item | 1   |
| TF_DATE | &nbsp; | &nbsp; | DATE | 8   | วันที่ฝาก | 18.04.2026 |
| REMART_SIZE | &nbsp; | &nbsp; | CHAR | 25  | Remark – Size | กล่องละ 20 KG |
| REMARK | &nbsp; | &nbsp; | CHAR | 120 | Remark | Surimi Non MSC PO DEMO 4100002355 |
| ISSUE_No. |     | ZMMT012-ISSNO | CHAR | 20  | เลขที่ใบเบิก | PCS No. 001/20242026 |

Table : ZMMT012

Short Text : Issue Doc No. for program Split batch at External WH and Report

|     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
| **Field** | **Key** | **Data Element** | **Data Type** | **Length** | **Short Text** | **Example** |
| CPUDT | X   |     | DATS | 8   | Print Date | 15.06.2026 |
| CPUTM | X   |     | TIMS | 6   | Print Time | 0:00:15 |
| USNAM | X   |     | CHAR | 12  | Create By | DEMOUSER |
| SEQNO | X   |     | NUM | 3   | Running No. | 003 |
| ISSNO | X   |     | CHAR | 20  | Issue Doc no. | PCS NO. 003/15062026 |
| ISSNO_IM | X   |     | NUM | 2   | Issue Doc no. Item | 01  |
| BUDAT | X   | MATDOC-BUDAT | DATS | 8   | Posting Date | 18.04.2026 |
| MBLNR | X   | MATDOC-MBLNR | CHAR | 10  | Material Document | 5000002669 |
| ZEILE | X   | MATDOC-ZEILE | NUM | 4   | Material Document Item | 1   |
| MJAHR | X   | MATDOC-MJAHR | NUM | 4   | Material Document Year | 2026 |
| BKTXT | &nbsp; | MATDOC-BKTXT | CHAR | 25  | Header Text | &nbsp; |
| XBLNR | &nbsp; | MATDOC-XBLNR | CHAR | 16  | Delivery Note | 164-Ex/2026 |
| EBELN | X   | MATDOC-EBELN | CHAR | 10  | Purchasing Document | 4100002355 |
| EBELP | X   | MATDOC-EBELP | NUM | 5   | Purchasing Doc Item | 10  |
| EMLIF | X   | MATDOC-EMLIF | CHAR | 10  | Vendor code | &nbsp; |
| MATNR | X   | MATDOC-MATNR | CHAR | 40  | Material code | RI3-N0-XXH-3 |
| SGTXT | &nbsp; | MATDOC-SGTXT | CHAR | 50  | Item Text | ONEU9187706 |
| BWTAR | &nbsp; | MATDOC-BWTAR | CHAR | 10  | Valuation Type | 2508010006 |
| CHARG | X   | MATDOC-CHARG | CHAR | 10  | Batch | 2508010006 |
| HSDAT | &nbsp; | MATDOC-HSDAT | DATS | 8   | MFG main Batch | 06.12.2025 |
| VFDAT | &nbsp; | MATDOC-VFDAT | DATS | 8   | SLED main Batch | 06.12.2027 |
| CHARG_R | &nbsp; | &nbsp; | NUM | 2   | Bacth split running | 1   |
| CHARG_N | &nbsp; | &nbsp; | NUM | 12  | Batch Split | 250801000601 |
| HSDAT_N | &nbsp; | &nbsp; | DATE | 8   | MFG for batch split | 27.02.2026 |
| STATUS | X   | &nbsp; | CHAR | 1   | Status (N, S, U) | U   |
| WERKS | X   | MATDOC-WERKS | CHAR | 4   | Plant | 1000 |
| LGORT | X   | MATDOC-LGORT | CHAR | 4   | Source Storage Location | 0WR0 |
| UMLGO | X   | MATDOC-UMLGO | CHAR | 4   | Receiving SLoc. | 0WNC |
| MEINS | X   | MATDOC-MEINS | UNIT | 3   | UoM | KG  |
| MENGE_TF_P | &nbsp; | &nbsp; | UNIT | 13,3 | TF to DEMO Qty | 0   |
| TFDOC_NO | &nbsp; | &nbsp; | CHAR | 10  | เลขที่ใบฝาก | I69005264 |
| TFDOC_IM | &nbsp; | &nbsp; | NUMC | 2   | เลขที่ใบฝากระดับ Item | 1   |
| TF_DATE | &nbsp; | &nbsp; | DATE | 8   | วันที่ฝาก | 18.04.2026 |
| REMART_SIZE | &nbsp; | &nbsp; | CHAR | 25  | Remark – Size | กล่องละ 20 KG |
| REMARK | &nbsp; | &nbsp; | CHAR | 120 | Remark | SuriNon MSC PO4100002355 |
| CREATED_BY |     | ZECREATED_BY | CHAR | 12  | Created by |     |
| CREATED_ON |     | ZECREATED_ON | DATS | 8   | Created on |     |
| CREATED_TIME |     | ZECREATED_TIME | TIMS | 6   | Created time |     |
| UPDATED_BY |     | ZEUPDATED_BY | CHAR | 12  | Updated by |     |
| UPDATED_ON |     | ZEUPDATED_ON | DATS | 8   | Updated on |     |
| UPDATED_TIME |     | ZEUPDATED_TIME | TIMS | 6   | Updated time |     |
| LICENSE_NO |     |     | CHAR | 10  | ทะเบียนรถ |     |
| SEAL_NO |     |     | CHAR | 10  | Seal no. |     |
| DEPART_TIME |     |     | CHAR | 8   | Departure time |     |

Table : ZMMT014

Short Text : SO/DO/MM Doc at External Sloc.

|     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
| **Field** | **Key** | **Data Element** | **Data Type** | **Length** | **Short Text** | **Example** |
| BUDAT | X   | MATDOC-BUDAT | DATS | 8   | Posting Date | 18.04.2026 |
| VBELN_SO | X   | VBAP-VBELN | CHAR | 10  | Sale Order | 1011099658 |
| POSNR_SO | X   | VBAP-POSNR | NUM | 6   | Sale Order Item | 000010 |
| ISSNO | X   | ZMMT012- ISSNO | CHAR | 20  | Issue Doc no. | RS2 NO. 003/15062026 |
| ISSNO_IM | X   | ZMMT012-ISSNO_IM | NUM | 2   | Issue Doc no. Item | 01  |
| VBELN_DO | X   | LIPS-VBELN | CHAR | 10  | Delivery Order | 1041100058 |
| POSNR_DO | X   | LIPS-POSNR | NUM | 6   | Delivery Order Item | 000010 |
| ERDAT |     | LIPS- ERDAT | DAT | 8   | DO create on | 19.03.2026 |
| ERZET |     | LIPS-ERZET | TIMS | 6   | DO create time | 10:07:25 |
| ERNAM |     | LIPS-ERNAM | CHAR | 12  | DO created by | R2SD02 |
| LFIMG |     | LIPS-LFIMG | QUAN | 13,3 | DO QTY | 1.000 |
| MEINS |     | LIPS-MEINS | UNIT | 3   | DO UoM | KG  |
| BWART |     | LIPS-BWART | CHAR | 3   | Movement Type | 601 |
| MBLNR |     | MATDOC-MBLNR | CHAR | 10  | Material Document | 4900000001 |
| ZEILE |     | MATDOC-ZEILE | NUM | 4   | Material Document Item | 0001 |
| MJAHR |     | MATDOC-MJAHR | NUM | 4   | Material Document Year | 2026 |
| MENGE_GI |     | MATDOC- MENGE | QUAN | 13  | GI QTY | 0.075 |
| MEINS \_GI |     | MATDOC- MEINS | UNIT | 3   | GI UoM | KG  |
| BUDAT |     | MATDOC-BUDAT | DATE | 8   | Posting Date | 31.01.2026 |
| CPUDT |     | MATDOC-CPUDT | DATE | 8   | Entry Date | 19.03.2026 |
| CPUTM |     | MATDOC-CPUTM | TIMS | 6   | Time of Entry | 10:08:50 |
| BKTXT | &nbsp; | MATDOC-BKTXT | CHAR | 25  | Header Text | &nbsp; |
| XBLNR |     | MATDOC-XBLNR | CHAR | 16  | Delivery Note | 1041100058 |
| MATNR |     | MATDOC-MATNR | CHAR | 40  | Material code | RI3-N0-XXH-3 |
| BWTAR |     | MATDOC-BWTAR | CHAR | 10  | Valuation Type | 2508010006 |
| CHARG |     | MATDOC-CHARG | CHAR | 10  | Batch | 2508010006 |
| HSDAT |     | MATDOC-HSDAT | DATS | 8   | MFG Date | 10.12.2024 |
| STATUS |     | ZMMT010-STATUS | CHAR | 1   | Status (N, U) | New, Update |
| WERKS |     | MATDOC-WERKS | CHAR | 4   | Plant | 1000 |
| LGORT |     | MATDOC-LGORT | CHAR | 4   | Source Storage Location | 0WR0 |
| MEINS |     | MATDOC-MEINS | UNIT | 3   | UoM | KG  |
| TFDOC_NO |     | ZMMT010-TFDOC_NO | CHAR | 10  | เลขที่ใบฝาก | I69005264 |
| TFDOC_IM |     | ZMMT010-TFDOC_IM | NUMC | 2   | เลขที่ใบฝากระดับ Item | 1   |
| TF_DATE | &nbsp; | ZMMT010-TF_DATE | DATE | 8   | วันที่ฝาก | 18.04.2026 |
| REMART_SIZE | &nbsp; | ZMMT010-REMART_SIZE | CHAR | 25  | Remark – Size | กล่องละ 20 KG |
| REMARK | &nbsp; | ZMMT010-REMARK | CHAR | 120 | Remark | Surimi Non MSC PO DEMO 4100002355 |

Table : ZMMT015

Short Text : History Log for MVT601 of Split batch at External WH and Report

|     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
| **Field** | **Key** | **Data Element** | **Data Type** | **Length** | **Short Text** | **Example** |
| BUDAT_601 | X   | MATDOC-BUDAT | DATS | 8   | Posting Date | 15.06.2026 |
| MBLNR_601 | X   | MATDOC-MBLNR | CHAR | 10  | GI Material Document | 4900002669 |
| ZEILE_601 | X   | MATDOC-ZEILE | NUM | 4   | GI Material Document Item | 1   |
| MJAHR_601 | X   | MATDOC-MJAHR | NUM | 4   | GI Material Document Year | 2026 |
| BWART_601 | X   | MATDOC-BWART | CHAR | 3   | Movement Type | 601 |
| USNAM_601 | X   | MATDOC-USNAM | CHAR | 12  | User Name | WHDWOR0 |
| BUDAT | X   | MATDOC-BUDAT | DATS | 8   | Posting Date_311 | 18.04.2026 |
| MBLNR | X   | ZMMT010-MBLNR | CHAR | 10  | Material Document_311 | 4900342111 |
| ZEILE | X   | ZMMT010-ZEILE | NUM | 4   | Material Document Item_311 | 1   |
| MJAHR | X   | ZMMT010-MJAHR | NUM | 4   | Material Document Year_311 | 2026 |
| BKTXT | &nbsp; | ZMMT010-BKTXT | CHAR | 25  | Header Text | &nbsp; |
| MATNR | X   | MATDOC-MATNR | CHAR | 40  | Material code | RI3-N0-XXH-3 |
| BWART | X   | MATDOC-BWART | CHAR | 3   | Movement Type | 311 |
| CHARG | X   | MATDOC-CHARG | CHAR | 10  | Batch | 2508010006 |
| HSDAT | &nbsp; | MATDOC-HSDAT | DATS | 8   | MFG main Batch | 06.12.2025 |
| WERKS | X   | MATDOC-WERKS | CHAR | 4   | Plant | 1000 |
| LGORT | X   | MATDOC-LGORT | CHAR | 4   | Source SLoc. | 0WR0 |
| MEINS | X   | MATDOC-MEINS | UNIT | 3   | UoM | KG  |
| MENGE_TF_P | X   | MATDOC-MENGE | UNIT | 13,3 | TF Qty | 20  |
| TFDOC_NO | &nbsp; | &nbsp; | CHAR | 10  | เลขที่ใบฝาก | I69005264 |
| TFDOC_IM | &nbsp;X | &nbsp; | NUMC | 2   | เลขที่ใบฝากระดับ Item | 1   |
| TF_DATE | &nbsp; | &nbsp; | DATE | 8   | วันที่ฝาก | 18.04.2026 |
| REMART_SIZE | &nbsp; | &nbsp; | CHAR | 25  | Remark – Size | กล่องละ 20 KG |
| REMARK | &nbsp; | &nbsp; | CHAR | 120 | Remark | Surimi Non MSC PO DEMO 4100002355 |
| ISSUE_No. |     | ZMMT012-ISSNO | CHAR | 20  | เลขที่ใบเบิก | PCS No. 001/20242026 |

### Selection Screen

 

**Option 8**

### Input Parameter

| **No** | **Field** | **Description** | **Remark** |
| --- | --- | --- | --- |
| **Option 1** |     |     |     |
| 1   | 🞊 Split and Update Lot number |     | Radio button (1) Default |
| 2   | Material Document | เลขที่เอกสาร | MATDOC-MBLNR |
| 3   | Material Document Year | ปีของเลขที่เอกสาร | MATDOC-MJAHR Default “Current Year” |
| 4   | Material | รหัสวัสดุ | MATDOC-MATNR |
| 5   | Batch | รหัสแบทซ์ที่ใช้รับ | MATDOC-CHARG |
| 6   | Plant | รหัสโรงงาน | MATDOC-WERKS<br><br>Require Field Default “1000” |
| 7   | Stor. Loc. | รหัสพื้นที่จัดเก็บที่ต้องการวัสดุ | MATDOC-LGORT |
| 8   | Purchase Order | เลขที่ใบสั่งซื้อ | MATDOC-EBELN |
| 9   | Posting Date | วันที่บันทึกมูลค่าทางบัญชีใน Material Document | MATDOC-BUDAT<br><br>Require Field<br><br>Default “Current Date” |
| **Option 2** |     |     |     |
| 1   | 🔿 Update Information from External WH |     | Radio button (1) |
| 2   | Material Document | เลขที่เอกสาร | MATDOC-MBLNR |
| 3   | Material Document Year | ปีของเลขที่เอกสาร | MATDOC-MJAHR Default “Current Year” |
| 4   | Material | รหัสวัสดุ | MATDOC-MATNR |
| 5   | Batch | รหัสแบทซ์ที่ใช้รับ | MATDOC-CHARG |
| 6   | Plant | รหัสโรงงาน | MATDOC-WERKS<br><br>Require Field Default “1000” |
| 7   | Stor. Loc. | รหัสพื้นที่จัดเก็บที่ต้องการวัสดุ | MATDOC-LGORT |
| 8   | Purchase Order | เลขที่ใบสั่งซื้อ | MATDOC-EBELN |
| 9   | Posting Date | วันที่บันทึกมูลค่าทางบัญชีใน Material Document | MATDOC-BUDAT<br><br>Require Field<br><br>Default “Current Date” |
| **Option 3** |     |     |     |
| 1   | 🔿 Create Issue document No. | สร้างเลขที่เอกสารใบเบิก เพื่อขอโอนย้ายสต๊อกกลับเข้า LIF | Radio button (1) |
| 2   | 🞎 Change Issue document no. | กรณีต้องการแก้ไขข้อมูลในใบเบิกที่ยังไม่มีการทำรายการ MVT311 | Checkbox |
| 3   | เลขที่ใบฝากห้องเย็น | เลขที่ใบฝากห้องเย็น | ZMMT010-TFDOC_NO |
| 4   | Item no. ใบฝากห้องเย็น | Item no. ใบฝากห้องเย็น | ZMMT010-TFDOC_IM |
| 5   | Material Document | เลขที่เอกสาร | MATDOC-MBLNR |
| 6   | Material Document Year | ปีของเลขที่เอกสาร | MATDOC-MJAHR Default “Current Year” |
| 7   | Material | รหัสวัสดุ | MATDOC-MATNR |
| 8   | Batch | รหัสแบทซ์ที่ใช้รับ | MATDOC-CHARG<br><br>Require Field |
| 9   | Plant | รหัสโรงงาน | MATDOC-WERKS |
| 10  | Destination Stor. Loc. | รหัส Storage location ปลายทาง | MATDOC-LGORT |
| **Option 4** |     |     |     |
| 1   | 🔿 Transfer from External WH to DEMO | โอนย้ายสินค้าจากคลังนอกกลับมายัง DEMO | Radio button (1) |
| 2   | 🞎 Transfer back to โรงนอก | กรณีทำรายการโอนย้ายผิดให้ติ๊ก Transfer to โรงนอกเพื่อโอนย้ายกลับมาก่อนจะทำรายการใหม่อีกครั้ง | Checkbox |
| 3   | Issue No. | เลขที่เอกสารใบเบิก | ZMMT012-ISSNO |
| 4   | เลขที่ใบฝากห้องเย็น | เลขที่ใบฝากห้องเย็น | ZMMT010-TFDOC_NO |
| 5   | Item no. ใบฝากห้องเย็น | Item no. ใบฝากห้องเย็น | ZMMT010-TFDOC_IM |
| 6   | Material Document Year | ปีของเลขที่เอกสาร | MATDOC-MJAHR Default “Current Year” |
| 7   | Material | รหัสวัสดุ | MATDOC-MATNR |
| 8   | Batch | รหัสแบทซ์ที่ใช้รับ | MATDOC-CHARG<br><br>Require Field |
| 9   | Plant | รหัสโรงงาน | MATDOC-WERKS<br><br>Require Field Default “1000” |
| 10  | Destination Stor. Loc. | รหัสพื้นที่จัดเก็บที่ต้องการวัสดุ | MATDOC-LGORT<br><br>Require Field |
| **Option 5** |     |     |     |
| 1   | 🔿 Display Report | เรียกดูรายงาน Stock balance ของคลังนอก | Radio button (1) |
| 2   | 🞎 Compare with MB52 | แงสดงข้อมูล Stock Balance เปรียบเทียบกับ MB52 | Checkbox |
| 3   | Material | รหัสวัสดุ | MATDOC-MATNR |
| 4   | Batch | รหัสแบทซ์ที่ใช้รับ | MATDOC-CHARG |
| 5   | Plant | รหัสโรงงาน | MATDOC-WERKS<br><br>Require Field Default “1000” |
| 6   | Stor. Loc. | รหัสพื้นที่จัดเก็บที่ต้องการวัสดุ | MATDOC-LGORT |
| **Option 6** |     |     |     |
| 1   | 🔿 Upload data for conversion | Upload Excel File เข้า Z-Table สำหรับรายการที่มีอยู่ในคลังนอกก่อนเริ่มใช้งานโปรแกรม | Radio button (1) |
| 2   | Upload File | Upload Excel File | Long text (255) |
| **Option 7** |     |     |     |
| 1   | 🔿 Transfer material to material & move to Ex.WH | Transfer material to material & move to Ex.WH | Radio button (1) |
| 2   | เลขที่ใบฝากห้องเย็น | เลขที่ใบฝากห้องเย็น | ZMMT010-TFDOC_NO |
| 3   | Item no. ใบฝากห้องเย็น | Item no. ใบฝากห้องเย็น | ZMMT010-TFDOC_IM |
| 4   | Material | รหัสวัสดุ | MATDOC-MATNR |
| 5   | Batch | รหัสแบทซ์ที่ใช้รับ | MATDOC-CHARG<br><br>Require Field |
| 6   | Plant | รหัสโรงงาน | MATDOC-WERKS<br><br>Require Field |
| 7   | Source Stor. Loc. | รหัส Storage location ต้นทาง | MATDOC-UMLGO<br><br>Require Field |
| **Option 8** |     |     |     |
| 1   | 🔿 Create DO and PGI at External Sloc. for FG | Create DO and PGI at External Sloc. for FG | Radio button (1) |
| 2   | Material Type | Material Type | MARA- MTART<br><br>Default ZFIN (Maintain in ZCAT001) and Display Field |
| 3   | Sale Order | Sale Order | VBAP-VBELN<br><br>Require Field |
| 4   | Sale Order Item | Sale Order Item | VBAP-POSNR |
| 5   | Material | Material | ZMMT010-MATNR |
| 6   | Plant | Plant | ZMMT010-WERKS<br><br>Require Field Default “1000” |
| 7   | Stor. Loc PGI. | Storage location | ZMMT010- LGORT |

### Output Screen

**Option 1: Split and Update Lot number**

- แสดงเป็น ALV Grid Display หลังจากได้ข้อมูล Goods Receipt Material Document MVT101 จาก MIGO โดยแสดงเฉพาะรายการที่ Status = N
- ทำเครื่องหมายในกล่อง Checkbox สำหรับรายการที่ต้องการ Copy เพื่อ Split Batch
- กดปุ่ม  เพื่อ Copy บรรทัดเท่าจำนวนที่ต้องการ Split
- เปิดช่อง Quantity ให้แก้ไขจำนวนในแต่ละรายการที่ทำการ Split แต่รวมแล้วต้องไม่เกินจำนวน GR Quantity ใน Material Document
- เปิดช่อง Split MFG, Remark – Size, เลขที่ใบฝาก, Item ใบฝาก, วันที่ฝาก และ Remark ให้สามารถกรอกข้อมูลได้ นอกจากนั้นให้แสดงเป็น Display Field
- Batch Split Running ในรายการของ Material document จะเป็น 1 เสมอ
- Batch Split Running ในรายการที่ Copy มาจะ Running เรียงตามลำดับ 1, 2, 3, 4, ...
- Batch Split เป็นข้อมูล Batch ที่อยู่ใน MATDOC-CHARG ต่อท้ายด้วย Batch Split Running
- Split MFG จะต้องมีค่าเสมอ
- ขณะกด SAVE ต้องตรวจสอบว่า Split MFG จะต้องมีค่าเสมอ และ QTY รวมของ Batch ที่ถูก Split จะต้องเท่ากับ MATDOC-MENGE
- หลัง SAVE Status จะถูก Update เป็น S
- กรณีระบุข้อมูลเพื่อทำการ Split Batch มากกว่า 1 Material Document Item และมีรายการใดรายการหนึ่ง Error ระบบจะแสดงข้อความ Error และไม่ Update ข้อมูลลง Z-Table ทั้งหมด
- กดปุ่ม  เพื่อทำการพิมพ์ ใบนำฝากคลังนอก โดย จะแสดงข้อมูลในฟอร์มเฉพาะที่ถูกทำเครื่องหมายใน Checkbox เท่านั้น และ Status <> N

**Option 2: Update Information from External WH**

- แสดงเป็น ALV Grid Display หลังจากทำการ Split Batch ด้วย Option 1 มาแล้วและมี Status &lt;> N แสดงเฉพาะรายการที่ Status <&gt; N
- ถ้า ZMMT010-MATNR = MARA-MATNR และ MARA-MTART = ZFIN แสดงข้อมูลเป็น ALV Grid Display และ แสดงเฉพาะรายการที่ Status = N หรือ U
- ในกรณีที่มีการ Split ข้อมูลผิดพลาด และ TF to DEMO QTY = 0 สามารถกดปุ่ม  เพื่อลบรายการที่ Batch Split Running <> 1 และสามารถกดปุ่ม เพื่อ Copy ข้อมูลที่ต้องการ Split ใหม่ โดย Update Status เป็น S ถ้า ZMMT010- TFDOC_NO = ค่าว่าง และ Update Status เป็น U ถ้า ZMMT010- TFDOC_NO <> ค่าว่าง
- เปิดช่อง Quantity ให้แก้ไขจำนวนในแต่ละรายการที่ทำการ Split แต่รวมแล้วต้องไม่เกินจำนวน GR Quantity ใน Material Document ที่ Split จำนวนแล้ว และ TF to DEMO QTY = 0
- เปิดช่อง Split MFG, Remark – Size, เลขที่ใบฝาก, Item ใบฝาก, วันที่ฝาก และ Remark ให้สามารถกรอกข้อมูลได้ นอกจากนั้นให้แสดงเป็น Display Field
- ขณะกด SAVE ต้องตรวจสอบว่า Split MFG จะต้องมีค่าเสมอ และ QTY รวมของ Batch ที่ถูก Split จะต้องเท่ากับ MATDOC-MENGE
- หลัง SAVE Status จะถูก Update เป็น U เมื่อค่า ZMMT010-TFDOC_NO, ZMMT010- TFDOC_IM และ ZMMT010-TF_DATE
- หาก ZMMT010-TFDOC_NO มีค่าแต่ ZMMT010-TFDOC_IM และ ZMMT010-TF_DATE ไม่มีค่า โปรแกรมจะแสดง Error
- ระบุข้อความใน Remark ในรายการแรกที่ Checkbox เพื่อใช้แสดงหมายเหตุในฟอร์ม ใบนำฝากคลังนอก
- กดปุ่ม  เพื่อทำการพิมพ์ ใบนำฝากคลังนอก และ Excel File ได้อีกครั้ง โดย จะแสดงข้อมูลในฟอร์มเหมือน Option 1 และแสดงเฉพาะรายการที่ถูกทำเครื่องหมายใน Checkbox เท่านั้น และ Status <> N
- หลังจากกดปุ่มพิมพ์ โปรแกรมจะแยกข้อมูล ใบนำฝากคลังนอก เป็น 2 ฟอร์ม คือ
    - ใบนำฝากคลังนอกของ Surimi (Material Type <> ZFIN) : ZMMF004
    - ใบนำฝากคลังนอกของ FG (Material Type = ZFIN) : ZMMF005

**Option 3: Create Issue document No.**

- แสดงเป็น ALV Grid Display หลังจากทำการ Split Batch และ Update เลขที่ใบฝากแล้วใน Option 2 และมี Status = U และ ZMMT010-TFDOC_NO &lt;> ค่าว่าง และดึงข้อมูลมาแสดงเฉพาะ GR Pending Qty &gt; 0 และ ZMMT010-MENGE ลบ ZMMT010-MENGE_TF > 0
- ทำเครื่องหมายใน Checkbox สำหรับรายการที่ต้องการสร้างเลขที่เอกสารใบเบิก และระบุจำนวนที่ต้องการโอนจากในช่อง TF to DEMO Qty พร้อมทั้งระบุ Storage Location ที่ต้องการรับของเข้า
- แก้ไข Remark ในรายการแรกที่ Checkbox โดย Group By Material และ Batch เพื่อใช้แสดงหมายเหตุในฟอร์ม ใบเบิกคลังนอก
- เพิ่มฟิลด์ LICENSE_NO, SEAL_NO, DEPART_TIME ให้กรอกและเก็บลง ZMMT012 ขณะ SAVE ได้ Issue No.
- กดปุ่ม  โปรแกรมจะทำการสร้าง เลขที่เอกสารใบเบิกที่ต้องการพิมพ์เพื่อส่งโรงนอก โดยหลังจากเลือกราย Item ที่ต้องการ และระบุ To Sloc, TF QTY และ Remark เรียบร้อยแล้ว ระบบจะ นำข้อมูลที่เลือกไป Update ลง Z-Table: ZMMT012 ดังนี้

ZMMT012-CPUDT = Entry Date

ZMMT012-CPUTM = Entry Time

ZMMT012-USNAM = SY-UNAME

ZMMT012-SEQNO = Running No.

ZMMT012-BUDAT = ZMMT010-BUDAT

ZMMT012-MBLNR = ZMMT010-MBLNR

ZMMT012-ZEILE = ZMMT010-ZEILE

ZMMT012-MJAHR = ZMMT010-MJAHR

ZMMT012-BKTXT = ZMMT010-BKTXT

ZMMT012-XBLNR = ZMMT010-XBLNR

ZMMT012-EBELN = ZMMT010-EBELN

ZMMT012-EBELP = ZMMT010-EBELP

ZMMT012-EMLIF = ZMMT010-EMLIF

ZMMT012-MATNR = ZMMT010-MATNR

ZMMT012-SGTXT = ZMMT010-SGTXT

ZMMT012-BWTAR = ZMMT010-BWTAR

ZMMT012-CHARG = ZMMT010-CHARG

ZMMT012-HSDAT = ZMMT010-HSDAT

ZMMT012-VFDAT = ZMMT010-VFDAT

ZMMT012-CHARG_R = ZMMT010-CHARG_R

ZMMT012-CHARG_N = ZMMT010-CHARG_N

ZMMT012-HSDAT_N = ZMMT010-HSDAT_N

ZMMT012-STATUS = ZMMT010-STATUS

ZMMT012-WERKS = ZMMT010-WERKS

ZMMT012-LGORT = ZMMT010-LGORT

ZMMT012-MEINS = ZMMT010-MEINS

ZMMT012-UMLGO = To Sloc ในหน้า Screen

ZMMT012-MENGE_TF_P = จำนวนที่ต้องการ Transfer ในหน้า screen (TF QTY)

ZMMT012-TFDOC_NO = ZMMT010-TFDOC_NO

ZMMT012-TFDOC_IM = ZMMT010-TFDOC_IM

ZMMT012-TF_DATE = ZMMT010-TF_DATE

ZMMT012-REMART_SIZE = ZMMT010-REMART_SIZE

ZMMT012-REMARK = ZMMT010-REMARK

โดยสร้างเลขที่เอกสาร Issue No. ด้วยเงื่อนไข ดังนี้

IF MATDOC-LGORT = 0WR0 and MARA-MTART <> ZFIN ให้ขึ้นต้นด้วย RC NO.

IF MATDOC-LGORT = 0WP0 and MARA-MTART <> ZFIN ให้ขึ้นต้นด้วย PCS NO.

ตามด้วย Running no. 3 หลักเริ่มต้นที่ 001

Re-Running By Date +”/” + Current Date

IF MATDOC-LGORT = 0WR0 and MARA-MTART = ZFIN ให้ขึ้นต้นด้วย RC2 NO.

IF MATDOC-LGORT = 0WPC and MARA-MTART = ZFIN ให้ขึ้นต้นด้วย PCC NO.

IF MATDOC-LGORT = 0WIS and MARA-MTART = ZFIN ให้ขึ้นต้นด้วย IS NO.

ตามด้วย Running no. 3 หลักเริ่มต้นที่ 001

Re-Running By Date +”/” + Current Date

ทุกครั้งที่มีการสร้าง Issue no. ภายใน 1 วัน และแยกแต่ละ WH โปรแกรมจะตรวจเลขที่เอกสาร ล่าสุด แล้ว Running เลขถัดไปเพื่อมาเป็นเลขที่เอกสาร และ Update ลง ZMMT012-ISSNO และ เก็บ Item ของเลขที่ใบเบิกใน ZMMT012-ISSNO_IM Group by ZMMT012-ISSNO

- กดปุ่ม  เพื่อทำการพิมพ์ ใบนำเบิกคลังนอก โดย จะแสดงข้อมูลในฟอร์มเฉพาะที่ถูกทำเครื่องหมายใน Checkbox เท่านั้น และ Status = U และ ZMMT010-TFDOC_NO <> ค่าว่าง

และดึงข้อมูล ZMMT012-ISSNO ZMMT012-MENGE_TF_P มาแสดงในฟอร์ม ข้อมูลอื่นๆที่แสดงในฟอร์มสามารถดึงได้จาก ZMMMT010

- หลังจากกดปุ่มพิมพ์ โปรแกรมจะแยกข้อมูล ใบนำเบิกคลังนอก เป็น 2 ฟอร์ม คือ
    - ใบนำเบิกคลังนอกของ Surimi (Material Type <> ZFIN) : ZMMF004
    - ใบนำเบิกคลังนอกของ FG (Material Type = ZFIN) : ZMMF005

- ถ้า Checkbox “Change Issue document no.” = X
    - ดึงข้อมูลต่างๆใน Record ที่ ZMMT012-ISSNO <> ค่าว่าง และ ไม่พบค่า ZMMT011-ISSNO ใน Table ZMMT011 (ยังไม่เคยทำรายการ MVT311)
    - เปิดให้แก้ไขข้อมูล TF QTY จาก ZMMT012-MENGE_TF_P และ Receiving Storage Location จาก ZMMT012-UMLGO โดยหลังจากกดปุ่ม SAVE หรือ Printout โปรแกรมจะนำข้อมูลดังกล่าวจากหน้าจอกลับไป Update ใน ZMMT012-MENGE_TF_P และ ZMMT012-UMLGO
    - หากมีการแก้ไข TF QTY โปรแกรมจะทำการตรวจสอบว่า QTY ที่แก้ไขนั้นจะต้องไม่เกิน ZMMT010-MENGE_PD (GR Pending Qty) หากมีมากกว่า MENGE_PD โปรแกรมจะแสดง Error “จำนวนที่ต้องการเบิกมีมากกว่าสต๊อก”
    - รายการที่นำมาแสดง จะต้องมีค่า ZMMT010-MENGE_PD (GR Pending Qty) <> 0
    - สามารถกดปุ่ม  เพื่อลบรายการที่เคยสร้างไว้ออกได้ โดยก่อนทำการ SAVE โปรแกรมจะทำการตรจสอบอีกครั้งว่า ZMMT012-ISSNO และ ZMMT012-ISSNO_IM ไม่เคยถูกบันทึกลง ZMMT011-ISSNO และ ZMMT011-ISSNO_IM

**Option 4:** **Transfer from External WH to DEMO**

- แสดงเป็น ALV Grid Display หลังจากทำการ Split Batch,Update เลขที่ใบฝาก และสร้าง Issue Doc No. แล้วใน Option 3 และมี Status = U และ ZMMT010- TFDOC_NO &lt;> ค่าว่าง และดึงข้อมูลมาแสดงเฉพาะ GR Pending Qty &gt; 0
- นำข้อมูลจาก ZMMT012 ที่ ZMMT012-ISSNO <> ค่าว่างมาแสดง ดังนี้

ZMMT012-BUDAT ZMMT012-MBLNR ZMMT012-ZEILE ZMMT012-MJAHR ZMMT012-BKTXT ZMMT012-XBLNR ZMMT012-EBELN ZMMT012-EBELP ZMMT012-EMLIF ZMMT012-MATNR ZMMT012-SGTXT ZMMT012-BWTAR

ZMMT012-CHARG ZMMT012-HSDAT ZMMT012-VFDAT ZMMT012-CHARG_R

ZMMT012-CHARG_N ZMMT012-HSDAT_N ZMMT012-STATUS

ZMMT012-WERKS ZMMT012-LGORT ZMMT012-MEINS

ZMMT012-UMLGO ZMMT012-MENGE_TF_P ZMMT012-TFDOC_NO

ZMMT012- TFDOC_IM ZMMT012-TF_DATE ZMMT012-REMARK_SIZE

ZMMT012-REMARK ZMMT012-ISSNO ZMMT012-ISSNO_IM

- นำข้อมูล ZMMT010-MENGE_INITIAL (GR ตั้งต้น) ZMMT010-MENGE (GR หลัง Split แล้ว) ZMMT010-MENGE_TF (QTY ที่โอนกลับ DEMO แล้ว) ZMMT010-MENGE_PD (GR คงเหลือที่ WH) จาก ZMMT010 ที่เข้าเงื่อนไขดังนี้มาแสดง

ZMMT010-BUDAT = ZMMT012-BUDAT

ZMMT010-MBLNR = ZMMT012-MBLNR

ZMMT010-ZEILE = ZMMT012-ZEILE

ZMMT010-MJAHR = ZMMT012-MJAHR

ZMMT010-BKTXT = ZMMT012-BKTXT

ZMMT010-XBLNR = ZMMT012-XBLNR

ZMMT010-EBELN = ZMMT012-EBELN

ZMMT010-EBELP = ZMMT012-EBELP

ZMMT010-EMLIF = ZMMT012-EMLIF

ZMMT010-MATNR = ZMMT012-MATNR

ZMMT010-SGTXT = ZMMT012-SGTXT

ZMMT010-BWTAR = ZMMT012-BWTAR

ZMMT010-CHARG = ZMMT012-CHARG

ZMMT010-HSDAT = ZMMT012-HSDAT

ZMMT010-VFDAT = ZMMT012-VFDAT

ZMMT010-HSDAT_N = ZMMT012-HSDAT_N

ZMMT010-STATUS = ZMMT012-STATUS

ZMMT010-WERKS = ZMMT012-WERKS

ZMMT010-LGORT = ZMMT012-LGORT

ZMMT010-MEINS = ZMMT012-MEINS

ZMMT010-UMLGO = ZMMT012-UMLGO

ZMMT010-TFDOC_NO = ZMMT012-TFDOC_NO

ZMMT010-TFDOC_IM = ZMMT012-TFDOC_IM

ZMMT010-TF_DATE = ZMMT012-TF_DATE

- ทำเครื่องหมายใน Checkbox สำหรับรายการที่ต้องการโอนกลับ DEMO โปรแกรมจะดึงข้อมูล TF QTY จาก ZMMT012-MENGE_TF_P (QTY ที่ต้องการโอนในครั้งนั้นๆ) และ ดึงข้อมูล Receiving Storage Location จาก ZMMT012-UMLGO และเปิดฟิลด์ให้สามารถแก้ไขฟิลด์นี้ได้โดยหลังจากกดปุ่ม  โปรแกรมจะนำข้อมูลดังกล่าวจากหน้าจอกลับไป Update ใน ZMMT012-MENGE_TF_P และ ZMMT012-UMLGO
- แก้ไข Remark ในรายการแรกที่ Checkbox โดย Group By Material และ Batch เพื่อใช้แสดงหมายเหตุในฟอร์ม ใบเบิกคลังนอก
- หลังกดปุ่ม  ระบบจะทำการ Transfer และ สร้างเอกสาร Material Document MVT311 และ Update ข้อมูล TF to DEMO Qty, GR Pending Qty ใน Z-Table และ เก็บรายละเอียดในการทำโอนย้ายลง Z-Table: ZMMT011 ดังนี้

ZMMT011-BUDAT ZMMT011-MBLNR ZMMT011-ZEILE ZMMT011-MJAHR ZMMT011-BKTXT ZMMT011-MATNR ZMMT011-BWART ZMMT011-CHARG ZMMT011-HSDAT ZMMT011-VFDAT ZMMT011-CHARG_R ZMMT011-CHARG_N ZMMT011-HSDAT_N ZMMT011-WERKS ZMMT011-LGORT

ZMMT011-UMLGO ZMMT011-MEINS ZMMT011-MENGE_TF_P

ZMMT011-TFDOC_NO ZMMT011-TFDOC_IM ZMMT011-TF_DATE

ZMMT011-REMART_SIZE ZMMT011-REMARK ZMMT011-ISSUE_No.

- ถ้าใน Option ก่อนหน้ามีการนำข้อมูลเลขที่ใบฝากและ Lot no. มาสร้างใบเบิกมากกว่า 1 ใบ และมีจำนวนเกินจำนวนที่สามารถโอนย้ายได้ โปรแกรม จะทำการตรวจสอบข้อมูลว่า TF QTY ทั้งหมดมากกว่า GR Pending QTY หรือไม่ ถ้าใช่โปรแกรมจะแสดง Error “สต๊อกไม่เพียงพอให้โอนย้าย”

**กรณีทำเครื่องหมาย Checkbox: Transfer back to โรงนอก**

- โปรแกรมจะดึงข้อมูลจาก Z-Table เฉพาะ STATUS = U และ เลขที่ใบฝาก &lt;> ค่าว่าง และมีข้อมูล TF to DEMO Qty &gt; 0
- ทำเครื่องหมายใน Checkbox สำหรับรายการที่ต้องการโอนกลับไปยังคลังนอก และระบุจำนวนที่ต้องการโอนจากในช่อง TF to DEMO Qty พร้อมทั้งระบุ Storage Location
- โปรแกรมจะระบุ Sloc = Destination Sloc และ To Sloc = Source Sloc เพื่อทำรายการโอนของกลับจาก DEMO ไปยังคลังนอก
- โปรแกรมจะระบุ Sloc = และ To Sloc เพื่อทำรายการโอนของกลับจาก DEMO ไปยังคลังนอก
- หลัง SAVE ระบบจะทำการ Transfer และ สร้างเอกสาร Material Document MVT312 และ Update ข้อมูล TF to DEMO Qty, GR Pending Qty ใน Z-Table และ เก็บรายละเอียดในการทำโอนย้ายลง Z-Table: ZMMT011 ดังนี้

ZMMT011-BUDAT ZMMT011-MBLNR ZMMT011-ZEILE ZMMT011-MJAHR ZMMT011-BKTXT ZMMT011-MATNR ZMMT011-BWART ZMMT011-CHARG ZMMT011-HSDAT ZMMT011-VFDAT ZMMT011-CHARG_R ZMMT011-CHARG_N ZMMT011-HSDAT_N ZMMT011-WERKS ZMMT011-LGORT

ZMMT011-UMLGO ZMMT011-MENGE_TF_P ZMMT011-MENGE

ZMMT011-TFDOC_NO ZMMT011-TFDOC_IM ZMMT011-TF_DATE

ZMMT011-REMART_SIZE ZMMT011-REMARK ZMMT011-ISSNO

ZMMT011-ISSNO_IM

**Option 5:** **Display Report**

**Display Report**

- แสดงข้อมูลจาก Z-Table ทั้งหมด และดู Stock คงเหลือจาก GR Pending Qty

**Compare with MB52**

- Group by material, plant, sloc และ Batch จาก Z-Table และนำยอดเทียบกับ MB52

- แสดงข้อมูลจาก Z-Table ทั้งหมด และดู Stock คงเหลือจาก GR Pending Qty

**Option 6: Upload Data for Conversion**

- เป็นการแสดงข้อมูล ZMMT010 ในรูปแบบ ALV Grid Display หลังจากนำข้อมูลเข้าระบบก่อนเริ่มใช้งานโปรแกรม โดยผู้ใช้งานจะต้องเตรียมข้อมูลลงใน Excel Template ซึ่งต้องมียอด Stock Balance ใน Sloc คลังนอก เท่ากับ MB52

**Option 7: Transfer Material to Material and Move to Ex.WH**

- กำหนดให้ผู้ใช้งานระบุข้อมูล Require field ได้แก่ Batch, Plant, Source Sloc. และ Dest Sloc.
- แสดงเป็น ALV Grid Display ดึงข้อมูลจาก ZMMT010 ที่ GR Pending Qty = 0 และ ZMMT010-TFDOC_NO <> ค่าว่าง
- เมื่อ Execute Program มาให้ระบบแสดงข้อมูลเป็น Display Field โดยดึงจาก ZMMT010 มาแสดง และเปิดฟิลด์ให้แก้ไขได้ ดังนี้

Dest. Material New Field

Source Sloc. New Field from input screen

Dest. Sloc New Field from input screen โดยจะเป็นค่า Sloc. ของคลังนอกเท่านั้น หาก

กรอกค่าอื่น โปรแกรมแสดง Error “ตรวจสอบ Sloc. ปลายทาง”

Quantity Default ค่าจาก ZMMT010-MENGE แต่แก้ไขได้ แต่ต้องมีค่าน้อยกว่าหรือ

เท่ากับ ค่าเดิม

- หลังจากกดโพสต์รายการ Transfer material to material พร้อมทั้งย้าย Storage location ให้โปรแกรมนำ Record ที่ถูกเลือกและกรอกข้อมูลดังกล่าวมา Update เป็นรายการใหม่ใน ZMMT010 โดยมี Key เป็น Material document ที่เกิดจากการทำรายการ MM Doc MVT 309
- Validate รายการที่ Select โดยต้องมีค่า ใน Dest. Material, Source Sloc., Dest. Sloc และ Quantity เสมอ
- หลังจากทำ Transfer material to material แล้วจะเก็บประวัติ Material document ของ MVT309 ใน Table: ZMMT011

**Option 8: Transfer Material to Material and Move to Ex.WH**

Execute 1

**Execute 1: Create DO, สร้างเลขที่ใบเบิก และสามารถพิมพ์ใบเบิกได้**

### Output Parameter

**Execute 2: PGI MM Doc created**

**Option 1, 2**

| **No** | **Field** | **Description** | **Remark** |
| --- | --- | --- | --- |
| 1   | Selection button | ใช้กรณีต้องการเลือกพิมพ์เอกสาร หรือ Split Batch และ Update ข้อมูลลง Z-Table | CHAR (1) |
| 2   | Status | สถานะกำกับ กิจกรรมล่าสุดที่ทำ (N = New, S = Split, U = Update) | ZMMT010-STATUS |
| 3   | Posting Date | วันที่ทำรายการบันทึกเอกสาร | ZMMT010-BUDAT |
| 4   | Purchasing Document | เลขที่ใบสั่งซื้อ | ZMMT010-EBELN |
| 5   | Purchasing Doc Item | เลขที่ใบสั่งซื้อระดับรายการ | ZMMT010-EBELP |
| 6   | Material Document | เลขที่เอกสารโอนระหว่างพื้นที่จัดเก็บ | ZMMT010-MBLNR |
| 7   | Material Document Item | เลขที่เอกสารโอนระหว่างพื้นที่จัดเก็บระดับรายการ | ZMMT010-ZEILE |
| 8   | Material code | รหัสวัสดุ | ZMMT010-MATNR |
| 9   | Plant | รหัสโรงงานต้นทาง | ZMMT010-WERKS |
| 10  | Source Storage Location | รหัสพื้นที่จัดเก็บ | ZMMT010-LGORT |
| 11  | Batch | รหัสแบทซ์หลักที่ทำรับใน SAP | ZMMT010-CHARG |
| 12  | Valuation Type | ประเภทของวิธีการประเมินมูลค่า | ZMMT010-BWTAR |
| 13  | UoM | หน่วยในการรับสินค้า | ZMMT010-MEINS |
| 14  | GR Qty | จำนวนในการทำรับสินค้า | ZMMT010-MENGE |
| 15  | TF to DEMO Qty | จำนวนในการโอนย้ายจากคลังนอกกลับ DEMO | ZMMT010-MENGE_TF |
| 16  | GR Pending Qty | จำนวนสินค้าที่ยังอยู่ในคลังนอก | ZMMT010-MENGE_PD |
| 17  | MFG main Batch | วันที่ผลิตของแบทซ์หลัก | ZMMT010-HSDAT |
| 18  | SLED main Batch | วันที่หมดอายุของแบทซ์หลัก | ZMMT010-VFDAT |
| 19  | Batch split running | ลำดับที่ของการแต่กแบทซ์หลัก | ZMMT010-CHARG_R |
| 20  | Batch Split | แบทซ์ที่ถูก Split | ZMMT010-CHARG_N |
| 21  | MFG for batch split | วันที่หมดอายุของแบทซ์ที่ถูก Split | ZMMT010-HSDAT_N |
| 22  | Remark – Size | หมายเหตุที่ใช้ระบุไซส์ | ZMMT010-REMARK_SIZE |
| 23  | เลขที่ใบฝาก | เลขที่ใบฝากของคลังนอก | ZMMT010-TFDOC_NO |
| 24  | เลขที่ใบฝากระดับ Item | เลขที่ใบฝากของคลังนอกระดับรายการ | ZMMT010-TFDOC_IM |
| 25  | วันที่ฝาก | วันที่ฝากของที่คลังนอก | ZMMT010-TF_DATE |
| 26  | Header Text | ข้อความระดับ Header | ZMMT010-BKTXT |
| 27  | Delivery Note | ระบุ Invoice | ZMMT010-XBLNR |
| 28  | Item Text | ข้อความระดับ Item | ZMMT010-SGTXT |
| 29  | Remark | หมายเหตุที่นำไปแสดงในฟอร์ม | ZMMT010-REMARK |

**Option 3**

| **No** | **Field** | **Description** | **Remark** |
| --- | --- | --- | --- |
| 1   | Selection button | ใช้กรณีต้องการเลือกพิมพ์เอกสาร หรือ Split Batch และ Update ข้อมูลลง Z-Table | CHAR (1) |
| 2   | Print Date | Print Date | ZMMT012-CPUDT |
| 3   | Print Time | Print Time | ZMMT012-CPUTM |
| 4   | Create By | Create By | ZMMT012-USNAM |
| 5   | Issue Doc no. | Issue Doc no. | ZMMT012-ISSNO |
| 6   | Item Issue Doc no. | Issue Doc no. Item | ZMMT012-ISSNO_IM |
| 7   | Status | สถานะกำกับ กิจกรรมล่าสุดที่ทำ (N = New, S = Split, U = Update) | ZMMT012-STATUS |
| 8   | เลขที่ใบฝาก | เลขที่ใบฝากของคลังนอก | ZMMT012-TFDOC_NO |
| 9   | เลขที่ใบฝากระดับ Item | เลขที่ใบฝากของคลังนอกระดับรายการ | ZMMT012-TFDOC_IM |
| 10  | วันที่ฝาก | วันที่ฝากของที่คลังนอก | ZMMT012-TF_DATE |
| 11  | Posting Date | วันที่ทำรายการบันทึกเอกสาร | ZMMT012-BUDAT |
| 12  | Purchasing Document | เลขที่ใบสั่งซื้อ | ZMMT012-EBELN |
| 13  | Purchasing Doc Item | เลขที่ใบสั่งซื้อระดับรายการ | ZMMT012-EBELP |
| 14  | Material Document | เลขที่เอกสารรับสินค้า | ZMMT012-MBLNR |
| 15  | Material Document Item | เลขที่เอกสารรับสินค้าระดับรายการ | ZMMT012-ZEILE |
| 16  | Material code | รหัสวัสดุ | ZMMT012-MATNR |
| 17  | Plant | รหัสโรงงาน | ZMMT012-WERKS |
| 18  | Source Storage Location | รหัสพื้นที่จัดเก็บต้นทาง | ZMMT012-LGORT |
| 19  | To Storage Location | รหัสพื้นที่จัดเก็บปลายทาง | ZMMT012-UMLGO |
| 20  | Batch | รหัสแบทซ์หลักที่ทำรับใน SAP | ZMMT012-CHARG |
| 21  | Valuation Type | ประเภทของวิธีการประเมินมูลค่า | ZMMT012-BWTAR |
| 22  | UoM | หน่วยในการรับสินค้า | ZMMT012-MEINS |
| 23  | GR Initial Qty | จำนวนในการทำรับสินค้า | ZMMT010-MENGE |
| 24  | TF QTY | จำนวนในการโอนย้ายจากคลังนอกกลับ DEMO ในครั้งนั้น | ZMMT012-MENGE_TF_P |
| 25  | TF to DEMO Qty | จำนวนสะสมในการโอนย้ายจากคลังนอกกลับ DEMO | ZMMT010-MENGE_TF |
| 26  | GR Pending Qty | จำนวนสินค้าที่ยังอยู่ในคลังนอก | ZMMT010-MENGE_PD |
| 27  | MFG main Batch | วันที่ผลิตของแบทซ์หลัก | ZMMT010-HSDAT |
| 28  | SLED main Batch | วันที่หมดอายุของแบทซ์หลัก | ZMMT010-VFDAT |
| 29  | MFG for batch split | วันที่หมดอายุของแบทซ์ที่ถูก Split | ZMMT012-HSDAT_N |
| 30  | Remark – Size | หมายเหตุที่ใช้ระบุไซส์ | ZMMT012-REMARK_SIZE |
| 31  | Header Text | ข้อความระดับ Header | ZMMT012-BKTXT |
| 32  | Delivery Note | ระบุ Invoice | ZMMT012-XBLNR |
| 33  | Item Text | ข้อความระดับ Item | ZMMT012-SGTXT |
| 34  | Remark | หมายเหตุที่นำไปแสดงในฟอร์ม | ZMMT012-REMARK |

**Option 4**

| **No** | **Field** | **Description** | **Remark** |
| --- | --- | --- | --- |
| 1   | Selection button | ใช้กรณีต้องการเลือกพิมพ์เอกสาร หรือ Split Batch และ Update ข้อมูลลง Z-Table | CHAR (1) |
| 2   | Status | สถานะกำกับ กิจกรรมล่าสุดที่ทำ (N = New, S = Split, U = Update) | ZMMT010-STATUS |
| 3   | เลขที่ใบฝาก | เลขที่ใบฝากของคลังนอก | ZMMT010-TFDOC_NO |
| 4   | เลขที่ใบฝากระดับ Item | เลขที่ใบฝากของคลังนอกระดับรายการ | ZMMT010-TFDOC_IM |
| 5   | วันที่ฝาก | วันที่ฝากของที่คลังนอก | ZMMT010-TF_DATE |
| 6   | Posting Date | วันที่ทำรายการบันทึกเอกสาร | ZMMT010-BUDAT |
| 7   | Purchasing Document | เลขที่ใบสั่งซื้อ | ZMMT010-EBELN |
| 8   | Purchasing Doc Item | เลขที่ใบสั่งซื้อระดับรายการ | ZMMT010-EBELP |
| 9   | Material Document | เลขที่เอกสารโอนระหว่างพื้นที่จัดเก็บ | ZMMT010-MBLNR |
| 10  | Material Document Item | เลขที่เอกสารโอนระหว่างพื้นที่จัดเก็บระดับรายการ | ZMMT010-ZEILE |
| 11  | Material code | รหัสวัสดุ | ZMMT010-MATNR |
| 12  | Plant | รหัสโรงงาน | ZMMT010-WERKS |
| 13  | Source Storage Location | รหัสพื้นที่จัดเก็บต้นทาง | ZMMT010-LGORT |
| 14  | To Storage Location | รหัสพื้นที่จัดเก็บปลายทาง | ZMMT012-UMLGO |
| 15  | Batch | รหัสแบทซ์หลักที่ทำรับใน SAP | ZMMT010-CHARG |
| 16  | Valuation Type | ประเภทของวิธีการประเมินมูลค่า | ZMMT010-BWTAR |
| 17  | UoM | หน่วยในการรับสินค้า | ZMMT010-MEINS |
| 18  | GR Initial Qty | จำนวนในการทำรับสินค้า | ZMMT010-MENGE |
| 19  | TF QTY | จำนวนในการโอนย้ายจากคลังนอกกลับ DEMO ในครั้งนั้นไ | QUAN (13,3) |
| 20  | TF to DEMO Qty | จำนวนสะสมในการโอนย้ายจากคลังนอกกลับ DEMO | ZMMT010-MENGE_TF |
| 21  | GR Pending Qty | จำนวนสินค้าที่ยังอยู่ในคลังนอก | ZMMT010-MENGE_PD |
| 22  | MFG main Batch | วันที่ผลิตของแบทซ์หลัก | ZMMT010-HSDAT |
| 23  | SLED main Batch | วันที่หมดอายุของแบทซ์หลัก | ZMMT010-VFDAT |
| 24  | Batch split running | ลำดับที่ของการแต่กแบทซ์หลัก | ZMMT010-CHARG_R |
| 25  | Batch Split | แบทซ์ที่ถูก Split | ZMMT010-CHARG_N |
| 26  | MFG for batch split | วันที่หมดอายุของแบทซ์ที่ถูก Split | ZMMT010-HSDAT_N |
| 27  | Remark – Size | หมายเหตุที่ใช้ระบุไซส์ | ZMMT010-REMARK_SIZE |
| 28  | Header Text | ข้อความระดับ Header | ZMMT010-BKTXT |
| 29  | Delivery Note | ระบุ Invoice | ZMMT010-XBLNR |
| 30  | Item Text | ข้อความระดับ Item | ZMMT010-SGTXT |
| 31  | Remark | หมายเหตุที่นำไปแสดงในฟอร์ม | ZMMT010-REMARK |
| 32  | Issue Doc no. | Issue Doc no. | ZMMT012-ISSNO |
| 33  | Item Issue Doc no. | Issue Doc no. Item | ZMMT012-ISSNO_IM |

**Option 5**

| **No** | **Field** | **Description** | **Remark** |
| --- | --- | --- | --- |
| **No Checkbox: Compare with MB52 \[Display Table\]** |     |     |     |
| 1   | Selection button | ใช้กรณีต้องการเลือกพิมพ์เอกสาร หรือ Split Batch และ Update ข้อมูลลง Z-Table | CHAR (1) |
| 2   | Status | สถานะกำกับ กิจกรรมล่าสุดที่ทำ (N = New, S = Split, U = Update) | ZMMT010-STATUS |
| 3   | Posting Date | วันที่ทำรายการบันทึกเอกสาร | ZMMT010-BUDAT |
| 4   | Purchasing Document | เลขที่ใบสั่งซื้อ | ZMMT010-EBELN |
| 5   | Purchasing Doc Item | เลขที่ใบสั่งซื้อระดับรายการ | ZMMT010-EBELP |
| 6   | Material Document | เลขที่เอกสารโอนระหว่างพื้นที่จัดเก็บ | ZMMT010-MBLNR |
| 7   | Material Document Item | เลขที่เอกสารโอนระหว่างพื้นที่จัดเก็บระดับรายการ | ZMMT010-ZEILE |
| 8   | Material code | รหัสวัสดุ | ZMMT010-MATNR |
| 9   | Plant | รหัสโรงงานต้นทาง | ZMMT010-WERKS |
| 10  | Source Storage Location | รหัสพื้นที่จัดเก็บ | ZMMT010-LGORT |
| 11  | Batch | รหัสแบทซ์หลักที่ทำรับใน SAP | ZMMT010-CHARG |
| 12  | Valuation Type | ประเภทของวิธีการประเมินมูลค่า | ZMMT010-BWTAR |
| 13  | UoM | หน่วยในการรับสินค้า | ZMMT010-MEINS |
| 14  | GR Qty | จำนวนในการทำรับสินค้า | ZMMT010-MENGE |
| 15  | TF to DEMO Qty | จำนวนในการโอนย้ายจากคลังนอกกลับ DEMO | ZMMT010-MENGE_TF |
| 16  | GR Pending Qty | จำนวนสินค้าที่ยังอยู่ในคลังนอก | ZMMT010-MENGE_PD |
| 17  | MFG main Batch | วันที่ผลิตของแบทซ์หลัก | ZMMT010-HSDAT |
| 18  | SLED main Batch | วันที่หมดอายุของแบทซ์หลัก | ZMMT010-VFDAT |
| 19  | Batch split running | ลำดับที่ของการแต่กแบทซ์หลัก | ZMMT010-CHARG_R |
| 20  | Batch Split | แบทซ์ที่ถูก Split | ZMMT010-CHARG_N |
| 21  | MFG for batch split | วันที่หมดอายุของแบทซ์ที่ถูก Split | ZMMT010-HSDAT_N |
| 22  | Remark – Size | หมายเหตุที่ใช้ระบุไซส์ | ZMMT010-REMARK_SIZE |
| 23  | เลขที่ใบฝาก | เลขที่ใบฝากของคลังนอก | ZMMT010-TFDOC_NO |
| 24  | เลขที่ใบฝากระดับ Item | เลขที่ใบฝากของคลังนอกระดับรายการ | ZMMT010-TFDOC_IM |
| 25  | วันที่ฝาก | วันที่ฝากของที่คลังนอก | ZMMT010-TF_DATE |
| 26  | Header Text | ข้อความระดับ Header | ZMMT010-BKTXT |
| 27  | Delivery Note | ระบุ Invoice | ZMMT010-XBLNR |
| 28  | Item Text | ข้อความระดับ Item | ZMMT010-SGTXT |
| 29  | Remark | หมายเหตุที่นำไปแสดงในฟอร์ม | ZMMT010-REMARK |
| **Checkbox: Compare with MB52** |     |     |     |
| 1   | Status | สถานะกำกับ กิจกรรมล่าสุดที่ทำ (N = New, S = Split, U = Update) | ZMMT010-STATUS |
| 2   | Material | รหัสวัสดุ | ZMMT010-MATNR |
| 3   | Plant | รหัสโรงงานต้นทาง | ZMMT010-WERKS |
| 4   | Sloc | รหัสพื้นที่จัดเก็บ | ZMMT010-LGORT |
| 5   | Batch | รหัสแบทซ์หลักที่ทำรับใน SAP | ZMMT010-CHARG |
| 6   | Batch Split Running | ลำดับที่ของการแต่กแบทซ์หลัก | ZMMT010-CHARG_R |
| 7   | Batch Split | แบทซ์ที่ถูก Split | ZMMT010-CHARG_N |
| 8   | เลขที่ใบฝาก | เลขที่ใบฝากของคลังนอก | ZMMT010-TFDOC_NO |
| 9   | Item ใบฝาก | เลขที่ใบฝากของคลังนอกระดับรายการ | ZMMT010-TFDOC_IM |
| 10  | Split MFG | วันที่หมดอายุของแบทซ์ที่ถูก Split | ZMMT010-HSDAT_N |
| 11  | UoM | หน่วยในการรับสินค้า | ZMMT010-MEINS |
| 12  | GR Pending Qty | จำนวนสินค้าที่ยังอยู่ในคลังนอก | ZMMT010-MENGE_PD |
| 13  | LABST | Valuated Unrestricted-Use Stock | MARD-LABST |
| 14  | EINME | Restricted Stock | MARD-EINME |
| 15  | INSME | Stock in Quality Inspection | MARD-INSME |
| 16  | SPEME | Blocked Stock | MARD-SPEME |
| 17  | TOTAL | Total | QUAN (13, 3) |
| 18  | COMPARE | Compare with MB52 | QUAN (13, 3) |

**Option 6**

| **No** | **Field** | **Description** | **Remark** |
| --- | --- | --- | --- |
| 1   | Status | สถานะกำกับ กิจกรรมล่าสุดที่ทำ (N = New, S = Split, U = Update) | ZMMT010-STATUS |
| 2   | Posting Date | วันที่ทำรายการบันทึกเอกสาร | ZMMT010-BUDAT |
| 3   | Purchasing Document | เลขที่ใบสั่งซื้อ | ZMMT010-EBELN |
| 4   | Purchasing Doc Item | เลขที่ใบสั่งซื้อระดับรายการ | ZMMT010-EBELP |
| 5   | Material Document | เลขที่เอกสารโอนระหว่างพื้นที่จัดเก็บ | ZMMT010-MBLNR |
| 6   | Material Document Item | เลขที่เอกสารโอนระหว่างพื้นที่จัดเก็บระดับรายการ | ZMMT010-ZEILE |
| 7   | Material code | รหัสวัสดุ | ZMMT010-MATNR |
| 8   | Plant | รหัสโรงงานต้นทาง | ZMMT010-WERKS |
| 9   | Source Storage Location | รหัสพื้นที่จัดเก็บ | ZMMT010-LGORT |
| 10  | Batch | รหัสแบทซ์หลักที่ทำรับใน SAP | ZMMT010-CHARG |
| 11  | Valuation Type | ประเภทของวิธีการประเมินมูลค่า | ZMMT010-BWTAR |
| 12  | UoM | หน่วยในการรับสินค้า | ZMMT010-MEINS |
| 13  | GR Qty | จำนวนในการทำรับสินค้า | ZMMT010-MENGE |
| 14  | TF to DEMO Qty | จำนวนในการโอนย้ายจากคลังนอกกลับ DEMO | ZMMT010-MENGE_TF |
| 15  | GR Pending Qty | จำนวนสินค้าที่ยังอยู่ในคลังนอก | ZMMT010-MENGE_PD |
| 16  | MFG main Batch | วันที่ผลิตของแบทซ์หลัก | ZMMT010-HSDAT |
| 17  | SLED main Batch | วันที่หมดอายุของแบทซ์หลัก | ZMMT010-VFDAT |
| 18  | Batch split running | ลำดับที่ของการแต่กแบทซ์หลัก | ZMMT010-CHARG_R |
| 19  | Batch Split | แบทซ์ที่ถูก Split | ZMMT010-CHARG_N |
| 20  | MFG for batch split | วันที่หมดอายุของแบทซ์ที่ถูก Split | ZMMT010-HSDAT_N |
| 21  | Remark – Size | หมายเหตุที่ใช้ระบุไซส์ | ZMMT010-REMARK_SIZE |
| 22  | เลขที่ใบฝาก | เลขที่ใบฝากของคลังนอก | ZMMT010-TFDOC_NO |
| 23  | เลขที่ใบฝากระดับ Item | เลขที่ใบฝากของคลังนอกระดับรายการ | ZMMT010-TFDOC_IM |
| 24  | วันที่ฝาก | วันที่ฝากของที่คลังนอก | ZMMT010-TF_DATE |
| 25  | Header Text | ข้อความระดับ Header | ZMMT010-BKTXT |
| 26  | Delivery Note | ระบุ Invoice | ZMMT010-XBLNR |
| 27  | Item Text | ข้อความระดับ Item | ZMMT010-SGTXT |
| 28  | Remark | หมายเหตุที่นำไปแสดงในฟอร์ม | ZMMT010-REMARK |
| 29  | REMART_SIZE | Remark – Size | ZMMT010- REMARK_SIZE |
| 30  | EMLIF | Supplier to be Supplied/Who is to Receive Delivery | ZMMT010-EMLIF |

**Option 7**

| **No** | **Field** | **Description** | **Remark** |
| --- | --- | --- | --- |
| 1   | Selection button | ใช้กรณีต้องการเลือกพิมพ์เอกสาร หรือ Split Batch และ Update ข้อมูลลง Z-Table | CHAR (1) |
| 2   | Status | สถานะกำกับ กิจกรรมล่าสุดที่ทำ (N = New, S = Split, U = Update) | ZMMT010-STATUS |
| 3   | Posting Date | วันที่ทำรายการบันทึกเอกสาร | ZMMT010-BUDAT |
| 4   | Purchasing Document | เลขที่ใบสั่งซื้อ | ZMMT010-EBELN |
| 5   | Purchasing Doc Item | เลขที่ใบสั่งซื้อระดับรายการ | ZMMT010-EBELP |
| 6   | Material Document | เลขที่เอกสารโอนระหว่างพื้นที่จัดเก็บ | ZMMT010-MBLNR |
| 7   | Material Document Item | เลขที่เอกสารโอนระหว่างพื้นที่จัดเก็บระดับรายการ | ZMMT010-ZEILE |
| 8   | Source Material code | รหัสวัสดุต้นทาง | ZMMT010-MATNR |
| 9   | To Material | รหัสวัสดุปลายทาง | ZMMT010-MATNR |
| 10  | Plant | รหัสโรงงานต้นทาง | ZMMT010-WERKS |
| 11  | Source Storage Location | รหัสพื้นที่จัดเก็บต้นทาง | ZMMT010-LGORT |
| 12  | Destination Storage Location | รหัสพื้นที่จัดเก็บปลายทาง | ZMMT010-UMLGO |
| 13  | Batch | รหัสแบทซ์หลักที่ทำรับใน SAP | ZMMT010-CHARG |
| 14  | Valuation Type | ประเภทของวิธีการประเมินมูลค่า | ZMMT010-BWTAR |
| 15  | UoM | หน่วยในการรับสินค้า | ZMMT010-MEINS |
| 17  | GR Qty | จำนวนในการทำรับสินค้า | ZMMT010-MENGE |
| 18  | TF to DEMO Qty | จำนวนในการโอนย้ายจากคลังนอกกลับ DEMO | ZMMT010-MENGE_TF |
| 19  | GR Pending Qty | จำนวนสินค้าที่ยังอยู่ในคลังนอก | ZMMT010-MENGE_PD |
| 20  | MFG main Batch | วันที่ผลิตของแบทซ์หลัก | ZMMT010-HSDAT |
| 21  | SLED main Batch | วันที่หมดอายุของแบทซ์หลัก | ZMMT010-VFDAT |
| 22  | Batch split running | ลำดับที่ของการแต่กแบทซ์หลัก | ZMMT010-CHARG_R |
| 23  | Batch Split | แบทซ์ที่ถูก Split | ZMMT010-CHARG_N |
| 24  | MFG for batch split | วันที่หมดอายุของแบทซ์ที่ถูก Split | ZMMT010-HSDAT_N |
| 25  | Remark – Size | หมายเหตุที่ใช้ระบุไซส์ | ZMMT010-REMARK_SIZE |
| 26  | เลขที่ใบฝาก | เลขที่ใบฝากของคลังนอก | ZMMT010-TFDOC_NO |
| 27  | เลขที่ใบฝากระดับ Item | เลขที่ใบฝากของคลังนอกระดับรายการ | ZMMT010-TFDOC_IM |
| 8   | วันที่ฝาก | วันที่ฝากของที่คลังนอก | ZMMT010-TF_DATE |
| 29  | Header Text | ข้อความระดับ Header | ZMMT010-BKTXT |
| 30  | Delivery Note | ระบุ Invoice | ZMMT010-XBLNR |
| 31  | Item Text | ข้อความระดับ Item | ZMMT010-SGTXT |
| 32  | Remark | หมายเหตุที่นำไปแสดงในฟอร์ม | ZMMT010-REMARK |

**Option 8**

| **No** | **Field** | **Description** | **Remark** |
| --- | --- | --- | --- |
| 1   | Selection button | ใช้กรณีต้องการเลือก Item ไปสร้างเอกสาร DO, DO Item และเลขที่ใบเบิก เพื่อพิมพ์เอกสารใบเบิกสินค้า และ Update ข้อมูลลง Z-Table | CHAR (1) |
| 2   | Sale Order | Sale Order ที่ลูกค้ากรอกมาเพื่อสร้าง DO | ZMMT013-VBELN_SO |
| 3   | Sale Order Item | Sale Order Item ที่ลูกค้ากรอกมาเพื่อสร้าง DO | ZMMT013-POSNR_SO |
| 4   | เลขที่ใบเบิก | เลขที่ใบเบิก | ZMMT013-ISSNO |
| 5   | Delivery Order | Delivery Order ที่เกิดขึ้นหลังจากเลือกรายการ Batch | ZMMT013-VBELN_DO |
| 6   | Delivery Order Item | Deli.Item ที่เกิดขึ้นหลังจากเลือกรายการ Batch | ZMMT013-POSNR_DO |
| 7   | MM Doc. | MM Doc.ที่เกิดขึ้นหลังจากมี Delivery Order | ZMMT013-MBLNR |
| 8   | Status | สถานะกำกับในการสร้างเอกสาร DO หรือ PGI Doc. | ZMMT010-STATUS |
| 9   | Message | ผลลัพธ์ในแต่ละ Step | ZMMT010-BUDAT |
| 10  | ทะเบียนรถ | ทะเบียนรถที่ขนสินค้าออก | ZMMT012-LICENSE_NO |
| 11  | Seal No. | Seal No. | ZMMT012-SEAL_NO |
| 12  | เวลา | เวลารถออก | ZMMT012-DEPART_TIME |
| 13  | Posting Date | วันที่ทำรายการบันทึกเอกสาร | ZMMT010-BUDAT |
| 14  | Material Document | เลขที่เอกสารโอนระหว่างพื้นที่จัดเก็บ | ZMMT010-MBLNR |
| 15  | Material Document Item | เลขที่เอกสารโอนระหว่างพื้นที่จัดเก็บระดับรายการ | ZMMT010-ZEILE |
| 16  | Source Material | รหัสวัสดุ | ZMMT010-MATNR |
| 17  | Plant | รหัสโรงงานต้นทาง | ZMMT010-WERKS |
| 18  | Source Storage Location | รหัสพื้นที่จัดเก็บ | ZMMT010-LGORT |
| 19  | Batch | รหัสแบทซ์หลักที่ทำรับใน SAP | ZMMT010-CHARG |
| 20  | Valuation Type | ประเภทของวิธีการประเมินมูลค่า | ZMMT010-BWTAR |
| 21  | UoM_GR | หน่วยในการรับสินค้า | MATDOC-MEINS |
| 22  | DO Qty | จำนวนในการเบิก | LIPS-LFIMG |
| 23  | UoM_GI | หน่วยในการเบิกสินค้า | LIPS-MEINS |
| 24  | GR Qty | จำนวนในการทำรับสินค้าเข้า Ex.sloc | ZMMT010-MENGE |
| 25  | TF to DEMO Qty | จำนวนในการโอนย้ายจากคลังนอกกลับ DEMO | ZMMT010-MENGE_TF |
| 26  | GR Pending Qty | จำนวนสินค้าที่ยังอยู่ในคลังนอก | ZMMT010-MENGE_PD |
| 27  | MFG main Batch | วันที่ผลิตของแบทซ์หลัก | ZMMT010-HSDAT |
| 28  | Remark – Size | หมายเหตุที่ใช้ระบุไซส์ | ZMMT010-REMARK_SIZE |
| 29  | เลขที่ใบฝาก | เลขที่ใบฝากของคลังนอก | ZMMT010-TFDOC_NO |
| 30  | เลขที่ใบฝากระดับ Item | เลขที่ใบฝากของคลังนอกระดับรายการ | ZMMT010-REMARK |
| 31  | วันที่ฝาก | วันที่ฝากของที่คลังนอก | ZMMT010-TF_DATE |
| 32  | Item Text | ข้อความระดับ Item | ZMMT012-REMARK_SIZE |
| 33  | Remark | หมายเหตุที่นำไปแสดงในฟอร์ม | ZMMT012-REMARK |

### Detail program logic

### 2.3.6.1 แบ่งหน้าจอโปรแกรมเป็น 2 ส่วนหลัก ดังนี้

- - Option

ใช้เพื่อเลือกฟังก์ชั่นงานที่ต้องการทำในโปรแกรม

- - Document Selection

ใช้เพื่อระบุเงื่อนไขต่างๆในการ Execute Program

### 2.3.6.2 เงื่อนไขในการดึงข้อมูลและทำงานของแต่ละ Option มีดังนี้

- - MIGO

หลัง Submit MIGO แล้วเข้าตามเงื่อนไข โปรแกรมจะ Update ข้อมูลจาก Material Document ใน Table MATDOC เข้า ZMMT010 ตาม Structure และ Update ZMMT010-STATUS = N

- - Option 1

เมื่อ Execute โปรแกรมระบบจะแสดงข้อมูล รายการที่ ZMMT010-STATUS = N เท่านั้นจากนั้นให้ Copy Line มาเพื่อทำการ Split Batch และแก้ไขจำนวนในแต่ละ Batch แต่โดยรวมยังต้องเท่ากับจำนวนที่ทำรับใน GR Document ครั้งนั้นๆ

มี Split MFG Date เป็น Require Field ต้องระบุค่าเสมอ หลังจากทำการ SAVE แล้วโปรแกรมจะอัพเดท ZMMT010-STATUS = S และเปลี่ยนทุกฟิลด์เป็น Display

- - Option 2

เมื่อ Execute โปรแกรมระบบจะแสดงข้อมูล รายการที่ ZMMT010-STATUS <> N เท่านั้นเพื่อทำการ Update ข้อมูลต่างๆ หลังจากทำการ Split Batch และแก้ไขจำนวนในแต่ละ Batch ไปแล้ว โดยฟิลด์ที่ทำการ Update ข้อมูลได้ ได้แก่ ZMMT010-MENGE, ZMMT010-HSDAT_N, ZMMT010-REMARK_SIZE, ZMMT010-TFDOC_NO, ZMMT010-TFDOC_IM, ZMMT010-TF_DATE, ZMMT010-REMARKโปรแกรมจะอัพเดท ZMMT010-STATUS = U และเปลี่ยนทุกฟิลด์เป็น Display

- - Option 3

เมื่อ Execute โปรแกรมระบบจะแสดงข้อมูล รายการที่ ZMMT010-STATUS = U และZMMT010-TFDOC_NO <> ค่าว่าง เปิดฟิลด์ให้ระบุ Destination Storage Location และ ยอดที่ต้องการ Transfer กลับไป ยัง DEMO จากนั้นทำการติ๊ก Checkbox ที่ต้องการรวมมาสร้างใบเบิกและสร้างเลขที่เอกสารใบเบิก แล้วบันทึกชุดข้อมูลลง Z-table: ZMMMT012

- - Option 4

เมื่อ Execute โปรแกรมระบบจะแสดงข้อมูล รายการที่ ZMMT010-STATUS = U และ ZMMT012-ISSNO <> ค่าว่าง เปิดฟิลด์ให้ระบุ Destination Storage Location และ ยอดที่ต้องการ Transfer โดยข้อมูลนี้เปิดให้แก้ไขได้แต่จะดึงค่า Default จาก ZMMT012-UMLGO ZMMT012-MENGE_TF_P ZMMT012-REMARKหากกด SAVE จะมีการนำ 3 ฟิลด์นี้กลับไป Update ใน ZMMT012 และ ZMMT010 โดย ใชข้อมูลกรอกข้อมูลใน BAPI ดังนี้

**Call BAPI_GOODSMVT_CREATE**

**GOODSMVT_HEADER**

PSTNG_DATE = SY-DATUM

DOC_DATE = SY-DATUM

HEADER_TXT = “ZDEMO01_4”

~~REF_DOC_NO = ZMMT012-XBLNR~~

PR_UNAME = SY-UNAME

**GOODSMVT_CODE**

GM_CODE = 04

**GOODSMVT_ITEM**

MATERIAL = ZMMT012-MATNR

PLANT = ZMMT012-WERKS

STGE_LOC = ZMMT012-LGORT

ABLAD = ZMMT012-ISSNO

BATCH = ZMMT012-CHARG

MOVE_TYPE = 311

ENTRY_QNT = ZMMT012-MENGE_TF_P

ENTRY_UOM = ZMMT012-MEINS

MOVE_MAT = ZMMT012-MATNR

MOVE_PLANT = ZMMT012-WERKS

MOVE_STLOC = ZMMT012-UMLGO

MOVE_BATCH = ZMMT012-CHARG

**Call BAPI_TRANSACTION_COMMIT**

กรณี Checkbox Transfer back to โรงนอก

โปรแกรมจะดึงข้อมูลจาก Z-Table เฉพาะ STATUS = U และ เลขที่ใบฝาก <> ค่าว่าง

และมีข้อมูล TF to DEMO Qty > 0

**Call BAPI_GOODSMVT_CREATE**

**GOODSMVT_HEADER**

PSTNG_DATE = SY-DATUM

DOC_DATE = SY-DATUM

HEADER_TXT = ZMMT012-ISSNO

REF_DOC_NO = “ZDEMO01_4”

PR_UNAME = SY-UNAME

**GOODSMVT_CODE**

GM_CODE = 04

**GOODSMVT_ITEM**

MATERIAL = ZMMT012-MATNR

PLANT = ZMMT012-WERKS

STGE_LOC = ZMMT012-UMLGO

BATCH = ZMMT012-CHARG

MOVE_TYPE = 311

ENTRY_QNT = ZMMT012-MENGE_TF_P

ENTRY_UOM = ZMMT012-MEINS

MOVE_MAT = ZMMT012-MATNR

MOVE_PLANT = ZMMT012-WERKS

MOVE_STLOC = ZMMT012-LGORT

MOVE_BATCH = ZMMT012-CHARG

**Call BAPI_TRANSACTION_COMMIT**

หลังทำรายการ MVT311 ด้วย Option 4 แล้ว ให้โปรแกรมเก็บข้อมูลใน Z-TABLE: ZMMT011 เพื่อบันทึกประวัติการทำรายการ ดังนี้

ZMMT011-BUDAT_311 = MATDOC-BUDAT

ZMMT011-MBLNR_311 = MATDOC-MBLNR

ZMMT011-ZEILE_311 = MATDOC-ZEILE

ZMMT011-MJAHR_311 = MATDOC-MJAHR

ZMMT011-USNAM = MATDOC-USNAM

ZMMT011-BUDAT = ZMMT010-BUDAT

ZMMT011-MBLNR = ZMMT010-MBLNR

ZMMT011-ZEILE = ZMMT010-ZEILE

ZMMT011-MJAHR = ZMMT010-MJAHR

ZMMT011-BKTXT = ZMMT010-BKTXT

ZMMT011-MATNR = ZMMT010-MATNR

ZMMT011-BWART = ZMMT010-BWART

ZMMT011-CHARG = ZMMT010-CHARG

ZMMT011-HSDAT = ZMMT010-HSDAT

ZMMT011-VFDAT = ZMMT010-VFDAT

ZMMT011-CHARG_R = ZMMT010-CHARG_R

ZMMT011-CHARG_N = ZMMT010-CHARG_N

ZMMT011-HSDAT_N = ZMMT010-HSDAT_N

ZMMT011-WERKS = ZMMT010-WERKS

ZMMT011-LGORT = ZMMT010-LGORT

ZMMT011-UMLGO = ZMMT010-UMLGO

ZMMT011-MEINS = ZMMT010-MEINS

ZMMT011-MENGE = ZMMT010-MENGE_TF_P

ZMMT011-TFDOC_NO = ZMMT010-TFDOC_NO

ZMMT011-TFDOC_IM = ZMMT010-TFDOC_IM

ZMMT011-TF_DATE = ZMMT010-TF_DATE

ZMMT011-REMART_SIZE = ZMMT010-REMART_SIZE

ZMMT011-REMARK = ZMMT010-REMARK

ZMMT011-ISSNO = ZMMT010-ISSNO

ZMMT011-ISSNO_IM = ZMMT010-ISSNO_IM

- - Option 5

แสดงรายงานสต๊อกคงเหลือจากการ Split Batch และยังคงค้างอยู่ที่ External Warehouse

ดึงข้อมูลจาก ZMMT010 มาแสดงโดย แสดงข้อมูลจาก ZMMT010 ทุก Fields แบบ Grid Display และรับข้อมูลจากหน้า Input Screen โดย

ถ้า Compare with MB52 = ค่าว่าง

- - - ถ้า Material ใน Input screen <> ค่าว่าง ให้ Material ใน Input screen = ZMMT010-MATNR
        - ถ้า Batch ใน Input screen <> ค่าว่าง ให้ Material ใน Input screen = ZMMT010-CHARG
        - ถ้า Plant ใน Input screen <> ค่าว่าง ให้ Material ใน Input screen = ZMMT010-WERKS
        - ถ้า Storage Location ใน Input screen <> ค่าว่าง ให้ Material ใน Input screen = ZMMT010-LGORT
        - ดึงข้อมูลจาก ZMMT010 ทั้งหมดมาแสดง และให้ user สามารถจัด Layout ได้เอง โดย Default Layout ไว้ตามฟิลด์ด้านล่าง และสามารถ Sort, Group By, Sub Total และ Summary ZMMT010-MENGE_PD (GR Pending Qty) เพราะแสดงยอดรวมได้

|     |     |     |     |
| --- | --- | --- | --- |
| **Field** | **Type** | **Length** | **Description** |
| STATUS | CHAR | 1   | Status |
| BUDAT | DATS | 8   | Posting Date |
| EBELN | CHAR | 10  | PO  |
| EBELP | NUMC | 5   | PO Item |
| EMLIF | CHAR | 10  | Vendor |
| MBLNR | CHAR | 10  | Material Doc. |
| ZEILE | NUMC | 4   | Item in Material Document |
| MATNR | CHAR | 40  | Material |
| WERKS | CHAR | 4   | Plant |
| LGORT | CHAR | 4   | Sloc |
| CHARG | CHAR | 10  | Batch |
| BWTAR | CHAR | 10  | Valaution Type |
| MEINS | UNIT | 3   | Base Unit of Measure |
| MENGE | QUAN | 13, 3 | Quantity |
| MENGE_TF | QUAN | 13, 3 | TF to DEMO Qty |
| MENGE_PD | QUAN | 13, 3 | GR Pending Qty |
| HSDAT | DATS | 8   | Main MFG |
| VFDAT | DATS | 8   | Main SLED |
| CHARG_R | NUMC | 2   | Batch Split Running |
| CHARG_N | CHAR | 12  | Batch Split |
| HSDAT_N | DATS | 8   | Split MFG |
| REMARK_SIZE | CHAR | 25  | Remark – Size |
| TFDOC_NO | CHAR | 10  | เลขที่ใบฝาก |
| TFDOC_IM | NUMC | 2   | Item ใบฝาก |
| TF_DATE | DATS | 8   | วันที่ฝาก |
| BKTXT | CHAR | 25  | Header Text |
| XBLNR | CHAR | 16  | Delivery Note |
| SGTXT | CHAR | 50  | Item Text |
| REMARK | CHAR | 120 | Remark |

ถ้า Compare with MB52 = “X”

- - - ถ้า Material ใน Input screen <> ค่าว่าง ให้ Material ใน Input screen = ZMMT010-MATNR
        - ถ้า Batch ใน Input screen <> ค่าว่าง ให้ Material ใน Input screen = ZMMT010-CHARG
        - ถ้า Plant ใน Input screen <> ค่าว่าง ให้ Material ใน Input screen = ZMMT010-WERKS
        - ถ้า Storage Location ใน Input screen <> ค่าว่าง ให้ Material ใน Input screen = ZMMT010-LGORT
        - นำข้อมูล Plant และ Storage Location จาก Input Screen มาหา Stock จาก MB52 โดย
            - ถ้า Material ใน Input screen <> ค่าว่าง ให้ Material ใน Input screen = Material ใน MB52

ELSE ZMMT010-MATNR = Material ใน MB52

- - - - ถ้า Batch ใน Input screen <> ค่าว่าง ให้ Material ใน Input screen = Batch ใน MB52

ELSE ZMMT010- CHARG = Batch ใน MB52

- - - - ถ้า Plant ใน Input screen <> ค่าว่าง ให้ Material ใน Input screen = Plant ใน MB52

ELSE ZMMT010- WERKS = Plant ใน MB52

- - - Summary ZMMT010-MENGE_PD (GR Pending Qty) Group by
        - Sum total By MATNR, WERKS, LGORT และ CHARG โดยการ Hide/ Unhide รายงานได้
        - Column Total เป็นผลรวมจาก LABST + EINME + INSME + SPEME
        - Column สุดท้ายนำข้อมูล Total_MB52 ลบกับ Total_MENGE_PD เพื่อแสดงผลต่าง กรณี ค่า > 0 ให้แสดงสี เหลือง และ ค่า < 0 ให้แสดงสีแดง

|     |     |     |     |     |
| --- | --- | --- | --- | --- |
| **Field** | **Type** | **Length** | **Description** | **Source** |
| STATUS | CHAR | 1   | Status | ZMMT010 |
| MATNR | CHAR | 40  | Material |
| WERKS | CHAR | 4   | Plant |
| LGORT | CHAR | 4   | Sloc |
| CHARG | CHAR | 10  | Batch |
| CHARG_R | NUMC | 2   | Batch Split Running |
| CHARG_N | CHAR | 12  | Batch Split |
| TFDOC_NO | CHAR | 10  | เลขที่ใบฝาก |
| TFDOC_IM | NUMC | 2   | Item ใบฝาก |
| HSDAT_N | DATS | 8   | Split MFG |
| MEINS | UNIT | 3   | Base Unit of Measure |
| MENGE_PD | QUAN | 13, 3 | GR Pending Qty |
| LABST | QUAN | 13, 3 | Unrestricted-Use Stock | MB52 |
| EINME | QUAN | 13, 3 | Restricted Stock |
| INSME | QUAN | 13, 3 | Quality Inspection |
| SPEME | QUAN | 13, 3 | Blocked |
| TOTAL | QUAN | 13, 3 | Total |
| COMPARE | QUAN | 13, 3 | Compare with MB52 | Comparison |

- - Option 6

นำข้อมูลที่เตรียมไว้ใน Excel File Upload เข้า Z-Table: ZMMT010 เพื่อใช้สำหรับการทำ Conversion ครั้งแรกตาม Template และสามารถตรวจสอบผลต่างระหว่าง Z-table และ MB52 ได้จาก Option 4

|     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- |
| Field | Type | Length | Description | Example | &nbsp;Remark |
| MBLNR | CHAR | 10  | Number of Material Document | 5000002669 | &nbsp; |
| MJAHR | NUMC | 4   | Material Document Year | 2026 | &nbsp; |
| ZEILE | NUMC | 4   | Item in Material Document | 1   | &nbsp; |
| LINE_ID | NUMC | 6   | Line split | 1   | Running ตามจำนวน Batch ที่แตก |
| BUDAT | DATS | 8   | Posting Date in the Document \* | 18.04.2026 | &nbsp; |
| BKTXT | CHAR | 25  | Document Header Text | &nbsp; | &nbsp; |
| XBLNR | CHAR | 16  | Reference Document Number | 164-Ex/2026 | ใส่หรือไม่ใส่ก็ได้ เนื่องจากไม่ต้องออกฟอร์ม |
| EBELN | CHAR | 10  | Purchase order number | 4100002355 | ใส่หรือไม่ใส่ก็ได้ เนื่องจากไม่ต้องออกฟอร์ม |
| EBELP | NUMC | 5   | Item Number of Purchasing Document | 10  | ใส่หรือไม่ใส่ก็ได้ เนื่องจากไม่ต้องออกฟอร์ม |
| EMLIF | CHAR | 10  | Supplier to be Supplied | 2010078 | ใส่หรือไม่ใส่ก็ได้ เนื่องจากไม่ต้องออกฟอร์ม |
| MATNR | CHAR | 40  | Material Number \* | RI3-N0-XXH-3 | &nbsp; |
| WERKS | CHAR | 4   | Plant \* | 1000 | &nbsp; |
| LGORT | CHAR | 4   | Storage location \* | 0WR0 | &nbsp; |
| CHARG | CHAR | 10  | Batch Number \* | 2508010006 | &nbsp; |
| MEINS | UNIT | 3   | Base Unit of Measure \* | KG  | &nbsp; |
| MENGE | QUAN | 13, 3 | Quantity \* | 24000 | &nbsp; |
| BWTAR | CHAR | 10  | Valuation Type\* | 2508010006 | &nbsp; |
| SGTXT | CHAR | 50  | Item Text | ONEU9187706 | ใส่หรือไม่ใส่ก็ได้ เนื่องจากไม่ต้องออกฟอร์ม |
| HSDAT | DATS | 8   | Date of Manufacture | 06.12.2025 | &nbsp; |
| VFDAT | DATS | 8   | Shelf Life Expiration or Best-Before Date | 06.12.2027 | &nbsp; |
| CHARG_R | NUMC | 2   | Batch split running \* | 01  | **ระบุตามเลขที่ใบฝากระดับ Item ของ DEMOSMART** |
| CHARG_N | CHAR | 12  | Batch Split \* | 250801000601 | **ระบุ Batch no. + เลขที่ใบฝากระดับ Item** |
| HSDAT_N | DATS | 8   | Date of Manufacture \* | 27.02.2026 | MFG for batch split |
| MENGE_TF | QUAN | 13, 3 | TF to DEMO Qty \* | 24000 | &nbsp; |
| MENGE_PD | QUAN | 13, 3 | GR Pending Qty \* | 0   | &nbsp; |
| MENGE_INITIAL | QUAN | 13, 3 | Initial Quantity \* | 24000 | &nbsp; |
| TFDOC_NO | CHAR | 10  | TF Document \* | I69005264 | เลขที่ใบฝาก |
| TFDOC_IM | NUMC | 2   | TF Item \* | 01  | เลขที่ใบฝากระดับ Item |
| TF_DATE | DATS | 8   | TF Date\* | 18.04.2026 | วันที่ฝาก |
| STATUS | CHAR | 1   | Split Status (N, S, U) \* | Update | New, Split, Update |
| REMARK_SIZE | CHAR | 25  | Remark Size | กล่องละ 20 KG | ใส่หรือไม่ใส่ก็ได้ เนื่องจากไม่ต้องออกฟอร์ม |
| REMARK | CHAR | 120 | Remark | Surimi Non MSC PO DEMO 4100002355 | ใส่หรือไม่ใส่ก็ได้ เนื่องจากไม่ต้องออกฟอร์ม |

- - Option 7

เมื่อ Execute โปรแกรมระบบจะแสดงข้อมูล รายการที่ ZMMT010-MENGE_PD = 0 และ ZMMT010-TFDOC_NO <> ค่าว่าง เปิดฟิลด์ให้ระบุ Destination material, Source Storage Location, Destination Storage Location และ ยอดที่ต้องการ Transfer โดยข้อมูลนี้เปิดให้แก้ไขได้แต่จะดึงค่า ใชข้อมูลกรอกข้อมูลใน BAPI ดังนี้

**Call BAPI_GOODSMVT_CREATE**

**GOODSMVT_HEADER**

PSTNG_DATE = SY-DATUM

DOC_DATE = SY-DATUM

HEADER_TXT = “ZDEMO01_7”

PR_UNAME = SY-UNAME

**GOODSMVT_CODE**

GM_CODE = 04

**GOODSMVT_ITEM**

MATERIAL = ZMMT012-MATNR

PLANT = ZMMT010-WERKS

STGE_LOC = Source Sloc. from input screen

ABLAD = ZMMT012-ISSNO

BATCH = ZMMT010-CHARG

MOVE_TYPE = 309

ENTRY_QNT = รับค่าจาก Screen แต่ต้องไม่มากกว่า ZMMT010-MENGE_TF_P

ENTRY_UOM = ZMMT010-MEINS

MOVE_MAT = Destination material from input screen

MOVE_PLANT = ZMMT010-WERKS

MOVE_STLOC = Destination Sloc. from input screen

MOVE_BATCH = ZMMT010-CHARG

**Call BAPI_TRANSACTION_COMMIT**

หลังทำรายการ MVT309 ด้วย Option 7 แล้ว ให้โปรแกรมเก็บข้อมูลใน Z-TABLE: ZMMT011 เพื่อบันทึกประวัติการทำรายการ ดังนี้

ZMMT011-BUDAT_311 = MATDOC-BUDAT

ZMMT011-MBLNR_311 = MATDOC-MBLNR

ZMMT011-ZEILE_311 = MATDOC-ZEILE

ZMMT011-MJAHR_311 = MATDOC-MJAHR

ZMMT011-USNAM = MATDOC-USNAM

ZMMT011-BUDAT = ZMMT010-BUDAT

ZMMT011-MBLNR = ZMMT010-MBLNR

ZMMT011-ZEILE = ZMMT010-ZEILE

ZMMT011-MJAHR = ZMMT010-MJAHR

ZMMT011-BKTXT = ZMMT010-BKTXT

ZMMT011-MATNR = ZMMT010-MATNR

ZMMT011-BWART = ZMMT010-BWART

ZMMT011-CHARG = ZMMT010-CHARG

ZMMT011-HSDAT = ZMMT010-HSDAT

ZMMT011-VFDAT = ZMMT010-VFDAT

ZMMT011-CHARG_R = ZMMT010-CHARG_R

ZMMT011-CHARG_N = ZMMT010-CHARG_N

ZMMT011-HSDAT_N = ZMMT010-HSDAT_N

ZMMT011-WERKS = ZMMT010-WERKS

ZMMT011-LGORT = ZMMT010-LGORT

ZMMT011-UMLGO = ZMMT010-UMLGO

ZMMT011-MEINS = ZMMT010-MEINS

ZMMT011-MENGE = ZMMT010-MENGE_TF_P

ZMMT011-TFDOC_NO = ZMMT010-TFDOC_NO

ZMMT011-TFDOC_IM = ZMMT010-TFDOC_IM

ZMMT011-TF_DATE = ZMMT010-TF_DATE

ZMMT011-REMART_SIZE = ZMMT010-REMART_SIZE

ZMMT011-REMARK = ZMMT010-REMARK

ZMMT011-ISSNO = ZMMT010-ISSNO

ZMMT011-ISSNO_IM = ZMMT010-ISSNO_IM

- - Option 8

เมื่อระบุ Sale Order ที่หน้า Input Screen หลังจาก Execute โปรแกรจะนำข้อมูล material, Plant และ Storage Location ที่อยู้ใน SO (VBAP-MATNR, VBAP-WERKS, VBAP-LGORT) ไปหารายการที่ยังมี stock อยู่ที่ External Storage location โดย

VBAP-MATNR = ZMMT010-MATNR

VBAP-WERKS = ZMMT010-WERKS

VBAP-LGORT = ZMMT010-LGORT

WHERE ZMMT010-MENGE_PD >0

จากนั้นผู้ใช้งานจะเป็นผู้กรอกข้อมูล Sale Order, Sale Order Item และ QTY โดยเลือกกรอกใน Batch ที่ต้องการจะ GI ออกจาก External Storage location และแก้ไขจำนวนให้ตรงกับที่ต้องการ

โปรแกรมรองรับการสร้าง Outbound Delivery อ้างอิง Sales Order และกำหนด Batch Split ให้กับ Delivery Item ตามข้อมูล Batch และปริมาณที่ได้รับจากต้นทาง โดย Sales Order Item หนึ่งรายการสามารถมี Batch Split Sub item ได้หลายรายการ ภายใต้ Delivery Main Item เดียวกัน และผลรวมปริมาณของ Batch Split Sub item ต้องเท่ากับปริมาณที่ต้องการจัดส่งของ Main Item

ก่อนนำข้อมูลไปสร้าง Delivery Order จะ Group Data และ Split Batch ดังนี้

1.  Group by plant, storage location, material และ summary ยอดรวมระบุใน Main Item
2.  กรณีมี Batch แตกต่างกันภายใต้ข้อ 1 ให้ทำ Batch split เป็น Sub Item เช่น 900001, 900002 เป็นต้น

**เมื่อเตรียมข้อมูลครบถ้วนในทำตามขั้นตอนดังนี้**

**เมื่อกด Execute ครั้งที่ 1**

1.  สร้าง Delivery Order

Function Module: BAPI_OUTB_DELIVERY_CREATE_SLS

**Import parameters**

SHIP_POINT = Shipping Point ของ Sales Order Item (VBAP -VSTEL)

DUE_DATE = Current Date (SY-DATUM)

**SALES_ORDER_ITEMS**

REF_DOC = เลข Sales Order ที่ระบุในหน้ารายงาน

REF_ITEM = เลข Sales Order Item ที่ระบุในหน้ารายงาน

DLV_QTY = ปริมาณรวมของ Item หลัก ที่ระบุในหน้ารายงาน Group By Plant, Sloc, Material

SALES_UNIT = หน่วยของปริมาณ โดยใช้จาก Sale Order (VBAP-ZIEME)

เมื่อสร้างสำเร็จจึงรัน Function Module: BAPI_TRANSACTION_COMMIT โดยกรอก WAIT = X ใน sequence เดียวกัน หากพบ Error ให้หยุดและตรวจสอบก่อน Commit

1.  ทำการแก้ไข Delivery Order และ เข้า Batch Split ตามรายการที่เลือกและ Group ไว้

Function Module: BAPI_OUTB_DELIVERY_CHANGE

**HEADER_DATA**

DELIV_NUMB = Delivery Order ในข้อ 1

HEADER_CONTROL

DELIV_NUMB = Delivery Order ในข้อ 1

DELIVERY = Delivery Order ในข้อ 1

**ITEM_DATA**

สมมติว่า Main Item ของ DO ใหม่เป็น 000010, หน่วยขายและ Base UoM เป็น KG ทั้งคู่ และเลข 900001–900007 ยังไม่ถูกใช้และเป็น Sub Item

| **DELIV_ITEM** | **HIERARITEM** | **USEHIERITM** | **BATCH** | **DLV_QTY** | **DLV_QTY_IMUNIT** | **SALES_UNIT** | **BASE_UOM** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 000010 | ว่าง | ว่าง | ว่าง | ว่าง | ว่าง | KG  | KG  |
| 900001 | 000010 | 1   | 1405261810 | 20  | 20  | KG  | KG  |
| 900002 | 000010 | 1   | 1405261910 | 610 | 610 | KG  | KG  |
| 900003 | 000010 | 1   | 1405262010 | 620 | 620 | KG  | KG  |
| 900004 | 000010 | 1   | 1405262110 | 620 | 620 | KG  | KG  |
| 900005 | 000010 | 1   | 1405262210 | 620 | 620 | KG  | KG  |
| 900006 | 000010 | 1   | 1405262310 | 620 | 620 | KG  | KG  |
| 900007 | 000010 | 1   | 1405262410 | 390 | 390 | KG  | KG  |

**ความหมายสำคัญ:**

- - HIERARITEM = 000010 ผูก Sub item กับ Main Item
    - USEHIERITM = 1 ระบุว่าเป็น Batch Split Sub item
    - บรรทัด Main Item ไม่ส่งยอด 3500 ซ้ำใน payload ตัวอย่างนี้ และ ไม่สั่งเปลี่ยนปริมาณ Main Item เป็นศูนย์
    - ถ้า Base UoM ไม่ใช่ KG ต้องแปลง DLV_QTY_IMUNIT ให้ถูกต้องก่อน

**ITEM_CONTROL**

DELIV_NUMB = Delivery Order ในข้อ 1

DELIV_ITEM = Sub Item

CHG_DELQTY = X

| DELIV_NUMB | DELIV_ITEM | CHG_DELQTY |
| --- | --- | --- |
| &lt;DO_TEST&gt; | 900001 | X   |
| &lt;DO_TEST&gt; | 900002 | X   |
| &lt;DO_TEST&gt; | 900003 | X   |
| &lt;DO_TEST&gt; | 900004 | X   |
| &lt;DO_TEST&gt; | 900005 | X   |
| &lt;DO_TEST&gt; | 900006 | X   |
| &lt;DO_TEST&gt; | 900007 | X   |

BAPI_TRANSACTION_COMMIT

เมื่อสร้างสำเร็จจึงรัน Function Module: BAPI_TRANSACTION_COMMIT โดยกรอก WAIT = X ใน sequence เดียวกัน หากมีข้อความประเภท E หรือ A ให้หยุด ไม่ Commit เมื่อผ่านจึงเรียก Commit โดย WAIT = X

1.  สร้างเอกสารใบเบิก

สร้างใบเบิกและสร้างเลขที่เอกสารใบเบิก แล้วบันทึกชุดข้อมูลลง Z-table: ZMMMT012

1.  โปรแกรมแสดงผล Delivery Order และ เลขที่ใบเบิก ดังตัวอย่าง

**เมื่อกด Execute ครั้งที่ 2**

1.  ตรวจสอบรายการ Picking Status

| สถานะปัจจุบัน | วิธีดำเนินการ |
| --- | --- |
| Picking = C — Completely Processed หรือ Item ไม่ต้อง Picking | ทำ PGI ด้วยตามค่าด้านล่าง |
| Picking = A / B และ<br><br>Item ต้อง Picking | ต้องอัปเดต Picking ที่ Batch Split Sub items ให้ครบก่อน แล้วจึง PGI |

1.  ทำรายการ Goods Issue อ้างอิง Delivery Order ที่แสดงผลในข้อ 4

Function Module: WS_DELIVERY_UPDATE_2

กรณี Picking ครบแล้ว กรอก WS_DELIVERY_UPDATE_2 ดังนี้

| **ส่วน** | **Field** | **ค่า** |
| --- | --- | --- |
| VBKOK_WA | VBELN_VL | เลข DO |
| VBKOK_WA | WABUC | X   |
| VBKOK_WA | WADAT_IST | วันที่ต้องการ Post GI |
| หน้าหลัก | DELIVERY | เลข DO เดียวกัน |
| หน้าหลัก | SYNCHRON | X   |
| หน้าหลัก | COMMIT | X — Execute แล้วบันทึกจริง |
| หน้าหลัก | UPDATE_PICKING | เว้นว่าง |
| หน้าหลัก | NICHT_SPERREN_1 | เว้นว่าง |
| ตาราง | VBPOK_TAB | เว้นว่าง |

หลังจาก Goods issue สำเร็จให้โปรแกรมกลับไป Update ข้อมูล QTY ต่างๆใน ZMMT010 โดย

นำจำนวนใน MATDOC-MENGE (MM Doc MVT601) ลบออกจาก ZMMT010-MENGE_PD

นำจำนวนใน MATDOC-MENGE (MM Doc MVT601) บวกเพิ่มไปใน MENGE_GI

และ Update ข้อมูลรายการ Material Doc ที่เกิดจากการ Goods Issue ใน Z-Table: ZMMT014 ดังนี้

## Report / Form

### Sample output

ทะเบียนรถ: 70-1123

Seal No: 26000210

เวลาออกรถ: 13.30 น.

### Column Specification

**ใบแจ้งฝากสินค้า**

| **Item** | **Field** | **Details** | **Technical Field** |
| --- | --- | --- | --- |
| **Document Title:** |     |     |     |
| 1.  | &lt;Company Logo&gt; | โลโก้บริษัท | JPG File |
| 2.  | &lt;Company Name&gt; | พิมพ์ชื่อบริษัท ทั้งภาษาไทย และอังกฤษ<br><br>Select company code (T001K-BUKRS) from T001K where T001K-BWKEY = MATDOC-WERKS<br><br>Select T001-ADRNR where T001-BUKRS = T001K-BUKRS<br><br>Select ADRC-NAME1 WHERE T001-ADRNR = ADRC-ADRNR AND ADRC-NATION = Blank, “T” | T880-NAME1 |
| 3.  | &lt;Company Address&gt; | พิมพ์ที่อยู่บริษัท ทั้งภาษาไทย และอังกฤษ<br><br>Select ADRC-STREET ADRC-STR_SUPPL3 ADRC-LOCATION ADRC-CITY2 ADRC-CITY1 ADRC-POST_CODE1 WHERE T001-ADRNR = ADRC-ADRNR AND ADRC-NATION = Blank, “T”<br><br>Select T005T-LANDX WHERE T001-LAND1 = T005T-LAND1 T005T-SPRAS = EN<br><br>Select T001-STCEG By remove (“TH”) WHERE T001-BUKRS = T001K-BUKRS<br><br>ระบุเบอร์โทรศัพท์และอีเมลล์ ใน Std Text: ZMMF004_TEL_EMAIL |     |
| 4.  | &lt;DOCUMENT TITLE&gt; | พิมพ์ชื่อฟอร์ม<br><br>“ใบแจ้งขอฝากสินค้า” |     |
| **Header – Section Top-Right:** |     |     |     |
| 5.  | PAGE: | พิมพ์ Page No. / Total Pages |     |
| **Header – Document Info-Left:** |     |     |     |
| 6.  | เรียน: | ถ้า MARA-MTART <> ZFIN<br><br>ดึงข้อมูลจาก Standard Text มาแสดง โดย STD Text ชื่อ ZMMF004_RECEIVER_ตามด้วย MATDOC-LGORT ในเอกสาร GR Document<br><br>ถ้า MARA-MTART = ZFIN<br><br>ดึงข้อมูลจาก Standard Text มาแสดง โดย STD Text ชื่อ ZMMF005_RECEIVER_ตามด้วย MATDOC-LGORT ในเอกสาร GR Document |     |
| 7.  | จาก: | ถ้า MARA-MTART <> ZFIN<br><br>ดึงข้อมูลจาก Standard Text มาแสดง โดย STD Text ชื่อ ZMMF004_SENDER ตามด้วย MATDOC-LGORT ในเอกสาร GR Document<br><br>ถ้า MARA-MTART = ZFIN<br><br>ดึงข้อมูลจาก Standard Text มาแสดง โดย STD Text ชื่อ ZMMF005_SENDER ตามด้วย MATDOC-LGORT ในเอกสาร GR Document |     |
| 8.  | วันที่: | Execution Date |     |
| **Item Detail** |     |     |     |
| 9.  | ลำดับ | Running No. ที่ใช้ในการออกฟอร์ม โดยขึ้นตารางและ Running ใหม่ทุกครั้งตามข้อมูล material code และ Lot No. | NUM (3) |
| 10. | รายละเอียดสินค้า | พิมพ์ Material No. จาก MATDOC-MATNR | ZMMT010-MATNR |
| 11. | จำนวน | ปริมาณในการฝาก (KG) | ZMMT010-MENGE |
| 12. | หน่วย | จำนวนชิ้นที่ฝาก | NUM (3) |
| 13. | Lot No. | เลขที่แบทซ์ที่ฝาก | ZMMT010-CHARG |
| 14. | MFG Date | วันที่ผลิต | ZMMT010-HSDAT_N |
| 15. | Size | Remark - Size | ZMMT010-REMARK_SIZE |
| **Item Detail - Total** |     |     |     |
| 16. | Total | แสดงใต้บรรทัดสุดท้ายที่ออกฟอร์ม โดย Group By material code และ Lot No. | CHAR |
| 17. | Total Weight | คำนวณยอดน้ำหนักทั้งหมด โดย Group By material code และ Lot No. | DEC (13,3) |
| **Item Footer - Signature** |     |     |     |
| 18. | หมายเหตุ: | ข้อความที่แสดงใน Item Text รายการแรกที่เลือกมาพิมพ์ฟอร์ม โดย Group By material code และ Lot No. | Char (120) |
| 19. | คำลงท้าย | ถ้า MARA-MTART <> ZFIN<br><br>ดึงข้อมูลจาก Standard Text มาแสดง โดย STD Text ชื่อ ZMMF004_FOOTER_ตามด้วย MATDOC-LGORT ในเอกสาร GR Document<br><br>ถ้า MARA-MTART = ZFIN<br><br>ดึงข้อมูลจาก Standard Text มาแสดง โดย STD Text ชื่อ ZMMF005_FOOTER_ตามด้วย MATDOC-LGORT ในเอกสาร GR Document | Char (255) |
| 20. | ชื่อผู้ออกฟอร์ม | แสดง ชื่อ-นามสกุล ของ User Logon โดย<br><br>ถ้า SY-UNAME = USER_ADDR-BNAME ให้นำข้อมูล USER_ADDR-NAME_TEXTC มาแสดง | USER_ADDR-NAME_TEXTC |
| 21. | ตำแหน่งผู้ออกฟอร์ม | ถ้า MARA-MTART <> ZFIN<br><br>ดึงข้อมูลจาก Standard Text มาแสดง โดย STD Text ชื่อ ZMMF004_SENDER ตามด้วย MATDOC-LGORT ในเอกสาร GR Document<br><br>ถ้า MARA-MTART = ZFIN<br><br>ดึงข้อมูลจาก Standard Text มาแสดง โดย STD Text ชื่อ ZMMF005_SENDER ตามด้วย MATDOC-LGORT ในเอกสาร GR Document | Char (255) |

**ใบแจ้งขอเบิกสินค้า**

| **Item** | **Field** | **Details** | **Technical Field** |
| --- | --- | --- | --- |
| **Document Title:** |     |     |     |
| 1.  | &lt;Company Logo&gt; | โลโก้บริษัท | JPG File |
| 2.  | &lt;Company Name&gt; | พิมพ์ชื่อบริษัท ทั้งภาษาไทย และอังกฤษ<br><br>Select company code (T001K-BUKRS) from T001K where T001K-BWKEY = MATDOC-WERKS<br><br>Select T001-ADRNR where T001-BUKRS = T001K-BUKRS<br><br>Select ADRC-NAME1 WHERE T001-ADRNR = ADRC-ADRNR AND ADRC-NATION = Blank, “T” | T880-NAME1 |
| 3.  | &lt;Company Address&gt; | พิมพ์ที่อยู่บริษัท ทั้งภาษาไทย และอังกฤษ<br><br>Select ADRC-STREET ADRC-STR_SUPPL3 ADRC-LOCATION ADRC-CITY2 ADRC-CITY1 ADRC-POST_CODE1 WHERE T001-ADRNR = ADRC-ADRNR AND ADRC-NATION = Blank, “T”<br><br>Select T005T-LANDX WHERE T001-LAND1 = T005T-LAND1 T005T-SPRAS = EN<br><br>Select T001-STCEG By remove (“TH”) WHERE T001-BUKRS = T001K-BUKRS<br><br>ระบุเบอร์โทรศัพท์และอีเมลล์ ใน Std Text: ZMMF004_TEL_EMAIL |     |
| 4.  | &lt;DOCUMENT TITLE&gt; | พิมพ์ชื่อฟอร์ม<br><br>“ใบแจ้งขอเบิกสินค้า” |     |
| **Header – Section Top-Right:** |     |     |     |
| 5.  | Document No. | ถ้า MARA-MTART <> ZFIN<br><br>ขิ้นต้นด้วยคำว่า “ใบเบิกเลขที่”<br><br>IF MATDOC-LGORT = 0WR0 ให้ขึ้นต้นด้วย RC NO.<br><br>IF MATDOC-LGORT = 0WP0 ให้ขึ้นต้นด้วย PCS NO.<br><br>ตามด้วย Running no. 3 หลักเริ่มต้นที่ 001<br><br>Re-Running By Date + ”/” + Current Date<br><br>ถ้า MARA-MTART = ZFIN<br><br>ขิ้นต้นด้วยคำว่า “ใบเบิกเลขที่”<br><br>IF MATDOC-LGORT = 0WR0 ให้ขึ้นต้นด้วย RC2 NO.<br><br>IF MATDOC-LGORT = 0WPC ให้ขึ้นต้นด้วย PCC NO.<br><br>IF MATDOC-LGORT = 0WIS ให้ขึ้นต้นด้วย IS NO.<br><br>ตามด้วย Running no. 3 หลักเริ่มต้นที่ 001<br><br>Re-Running By Date + ”/” + Current Date | ZMMT012-ISSNO |
| 6.  | PAGE: | พิมพ์ Page No. / Total Pages |     |
| **Header – Document Info-Left:** |     |     |     |
| 7.  | เรียน: | ถ้า MARA-MTART <> ZFIN<br><br>ดึงข้อมูลจาก Standard Text มาแสดง โดย STD Text ชื่อ ZMMF004_RECEIVER_ตามด้วย MATDOC-LGORT ในเอกสาร GR Document<br><br>ถ้า MARA-MTART = ZFIN<br><br>ดึงข้อมูลจาก Standard Text มาแสดง โดย STD Text ชื่อ ZMMF005_RECEIVER_ตามด้วย MATDOC-LGORT ในเอกสาร GR Document |     |
| 8.  | จาก: | ถ้า MARA-MTART <> ZFIN<br><br>ดึงข้อมูลจาก Standard Text มาแสดง โดย STD Text ชื่อ ZMMF004_FOOTER_ ตามด้วย MATDOC-LGORT ในเอกสาร GR Document<br><br>ถ้า MARA-MTART = ZFIN<br><br>ดึงข้อมูลจาก Standard Text มาแสดง โดย STD Text ชื่อ ZMMF005_FOOTER_ ตามด้วย MATDOC-LGORT ในเอกสาร GR Document |     |
| 9.  | วันที่: | Execution Date |     |
| **Header – Document Info-Left:** |     |     |     |
|     | ทะเบียนรถ | ทะเบียนรถ | ZMMT012- LICENSE_NO |
|     | Seal No. | Seal No. | ZMMT012- SEAL_NO |
|     | เวลาออกรถ | เวลาออกรถ | ZMMT012- DEPART_TIME |
| **Item Detail** |     |     |     |
| 10. | ลำดับ | Running No. ที่ใช้ในการออกฟอร์ม | NUM (3) |
| 11 – 12 | เลขที่ใบฝาก/<br><br>วันที่ฝาก | เลขที่ใบฝาก<br><br>พิมพ์ จาก ZMMT010-TFDOC_NO<br><br>วันที่ฝาก<br><br>พิมพ์ จาก ZMMT010-TF_DATE |     |
| 13. | Item | พิมพ์ จาก ZMMT010-TFDOC_IM |     |
| 14. | รายละเอียดสินค้า | พิมพ์ Material No. จาก MATDOC-MATNR | ZMMT010-MATNR |
| 15. | จำนวน | ปริมาณในการโอน (KG) | ZMMT012-MENGE_TF_P |
| 16. | หน่วย | จำนวนชิ้นที่ฝาก | NUM (3) |
| 17. | Lot No. | เลขที่แบทซ์ที่ฝาก | ZMMT010-CHARG |
| 18. | MFG Date | MFG Date<br><br>พิมพ์ จาก ZMMT010- HSDAT_N |     |
| 19. | Size | Remark - Size | ZMMT010-REMARK_SIZE |
| **Item Detail - Total** |     |     |     |
| 20. | Total | แสดงใต้บรรทัดสุดท้ายที่ออกฟอร์ม | CHAR |
| 21. | Total Weight | คำนวณยอดน้ำหนักทั้งหมด | DEC (13,3) |
| **Item Footer - Signature** |     |     |     |
| 22. | หมายเหตุ: | ข้อความที่แสดงใน Item Text รายการแรกที่เลือกมาพิมพ์ฟอร์ม | CHAR (120) |
| 23. | คำลงท้าย | ถ้า MARA-MTART <> ZFIN<br><br>ดึงข้อมูลจาก Standard Text มาแสดง โดย STD Text ชื่อ ZMMF004_FOOTER_ตามด้วย MATDOC-LGORT ในเอกสาร GR Document<br><br>ถ้า MARA-MTART = ZFIN<br><br>ดึงข้อมูลจาก Standard Text มาแสดง โดย STD Text ชื่อ ZMMF005_FOOTER_ตามด้วย MATDOC-LGORT ในเอกสาร GR Document | CHAR (255) |
| 24. | ชื่อผู้ออกฟอร์ม | แสดง ชื่อ-นามสกุล ของ User Logon โดย<br><br>ถ้า SY-UNAME = USER_ADDR-BNAME ให้นำข้อมูล USER_ADDR-NAME_TEXTC มาแสดง | USER_ADDR-NAME_TEXTC |
| 25. | ตำแหน่งผู้ออกฟอร์ม | ถ้า MARA-MTART <> ZFIN<br><br>ดึงข้อมูลจาก Standard Text มาแสดง โดย STD Text ชื่อ ZMMF004_SENDER ตามด้วย MATDOC-LGORT ในเอกสาร GR Document<br><br>ถ้า MARA-MTART = ZFIN<br><br>ดึงข้อมูลจาก Standard Text มาแสดง โดย STD Text ชื่อ ZMMF004_SENDER ตามด้วย MATDOC-LGORT ในเอกสาร GR Document | Char (255) |

### Other

## N/A

# Error Handling

## N/A

# Testing

|     |     |     |
| --- | --- | --- |
| Scenario | Test Description | Expect Result |
| 4.1 | ทำรายการ Goods Receipt ด้วย MIGO และมีการ Update ZMMT010 | Update ข้อมูลเข้า ZMMT010 ถูกต้องด้วย Status N |
| 4.2 | เรียกดูรายการที่ทำรับมาแล้วยังไม่มีการ Split Batch ด้วย Option 1 และทำการ Split Batch พร้อมทั้งอัพเดท Status S | Update ข้อมูลเข้า ZMMT010 ถูกต้องด้วย Status S |
| 4.3 | สั่งพิมพ์เลขที่เอกสารใบฝากสินค้า | แสดงข้อมูลในรายงานและฟอร์มถูกต้อง |
| 4.4 | เรียกดูรายการที่ Split Batch แล้วด้วย Option 2 และทำการ Update ข้อมูลเพิ่มเติมจากคลังนอก พร้อมทั้งอัพเดท Status U | Update ข้อมูลเข้า ZMMT010 ถูกต้องด้วย Status U |
| 4.5 | โปรแกรมแสดงข้อมูล จาก ZMMT010 เพื่อให้ Select เพื่อ Goods Transfer MVT311 | โปรแกรมโพสต์รายการโอนย้ายๆด้ถูกต้อง |
| 4.6 | สั่งพิมพ์เลขที่เอกสารใบเบิกสินค้า | แสดงข้อมูลในรายงานและฟอร์มถูกต้อง |
| 4.7 | เรียกดูรายงานจาก Option 4 แบบไม่เปรียบเทียบ MB52 เพื่อดูความถูกต้องของข้อมูล | ข้อมูล Upload ถูกต้องและมีข้อมูล Stock ใน ZMMT010 |
| 4.8 | เรียกดูรายงานจาก Option 4 แบบเปรียบเทียบ MB52 | ข้อมูล Upload ถูกต้องและมีข้อมูล Stock ใน ZMMT010 โดยรวมเท่ากับ MB52 |
| 4.9 | Upload ข้อมูล Excel สำหรับการ Conversion ด้วย Option 5 และเรียกดูรายงานแบบเปรียบเทียบ MB52 ด้วย Option 4 | ข้อมูล Upload ถูกต้องและมีข้อมูล Stock ใน ZMMT010 โดยรวมเท่ากับ MB52 |
| 4.10 | สั่งพิมพ์เลขที่เอกสารใบฝากสินค้าสำหรับ FG | แสดงข้อมูลในรายงานและฟอร์มถูกต้อง |
| 4.11 | โปรแกรมแสดงข้อมูล จาก ZMMT010 เพื่อให้ Select เพื่อ Goods Transfer MVT311 สำหรับ FG | โปรแกรมโพสต์รายการโอนย้ายๆด้ถูกต้อง |
| 4.12 | สั่งพิมพ์เลขที่เอกสารใบเบิกสินค้าสำหรับ FG | แสดงข้อมูลในรายงานและฟอร์มถูกต้อง |
| 4.13 | เรียกดูรายงานจาก Option 4 แบบไม่เปรียบเทียบ MB52 เพื่อดูความถูกต้องของข้อมูลสำหรับ FG | ข้อมูล Upload ถูกต้องและมีข้อมูล Stock ใน ZMMT010 |
| 4.14 | โปรแกรมแสดงข้อมูล จาก ZMMT010 เพื่อให้ Select เพื่อสร้าง Delivery Order และ GIสำหรับ FG | โปรแกรมโพสต์รายการ Goods issue ถูกต้อง |

# Appendix

## N/A