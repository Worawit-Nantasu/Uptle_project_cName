# README

## ภาพรวมของโปรเจ็ค
โปรเจ็คนี้ใช้สำหรับประมวลผลไฟล์ JSON และไฟล์รูปภาพ โดยการเปลี่ยนชื่อคีย์ในไฟล์ JSON และจัดระเบียบรูปภาพให้เป็นโฟลเดอร์ที่เปลี่ยนชื่อใหม่ตามเพศ การทำงานหลักอยู่ในสองสคริปต์ Python ดังนี้:

1. **`update_names.py`**: อัพเดตชื่อในไฟล์ JSON และสร้างรายงานที่เชื่อมโยงชื่อและเพศ
2. **`rename_images.py`**: เปลี่ยนชื่อไฟล์รูปภาพตามรายงานที่สร้างไว้

---

## โครงสร้างของโฟลเดอร์

```
Uptle_project_cName
├── data
│   ├── img
│   │   ├── female         # รูปภาพต้นฉบับ (หญิง)
│   │   └── male           # รูปภาพต้นฉบับ (ชาย)
│   ├── img_renamed        # รูปภาพที่เปลี่ยนชื่อแล้ว
│   ├── input              # ไฟล์ JSON ต้นฉบับ
│   ├── lang_names.json    # ไฟล์ชื่อ (ประกอบด้วยชื่อและเพศ)
│   └── output             # ไฟล์ JSON ที่เปลี่ยนชื่อแล้ว
├── logs
│   ├── reportGender.json  # รายงานที่แมปชื่อกับเพศ
│   └── script_run.log     # ไฟล์ log สำหรับการทำงานของสคริปต์
├── scripts
│   ├── rename_images.py   # สคริปต์สำหรับเปลี่ยนชื่อรูปภาพ
│   └── update_names.py    # สคริปต์สำหรับอัพเดตชื่อใน JSON
└── README.md              # เอกสารประกอบโปรเจ็ค
```

---

## ข้อกำหนดเบื้องต้น

- Python 3.7+
- ไลบรารี Python ที่ต้องใช้:
  - `os`
  - `json`
  - `random`
  - `datetime`
  - `shutil`
  - `logging`

ติดตั้งไลบรารีเพิ่มเติมถ้าจำเป็นด้วยคำสั่ง:

```bash
pip install -r requirements.txt
```

---

## วิธีการใช้งาน

### ขั้นตอนที่ 1: เตรียมไฟล์
- วางไฟล์ JSON ที่ต้องการเปลี่ยนชื่อในโฟลเดอร์ `data/input`
- วางไฟล์รูปภาพในโฟลเดอร์ `data/img/male` และ `data/img/female`
- สร้างไฟล์ `lang_names.json` ในโฟลเดอร์ `data/` โดยมีโครงสร้างดังนี้:

  ```json
  [
    {"name": "ชื่อ1", "gender": "male"},
    {"name": "ชื่อ2", "gender": "female"}
  ]
  ```

### ขั้นตอนที่ 2: รันสคริปต์

1. **รัน `update_names.py`**:
   ```bash
   python scripts/update_names.py
   ```
   - เปลี่ยนชื่อในไฟล์ JSON
   - บันทึกไฟล์ JSON ที่เปลี่ยนชื่อแล้วใน `data/output`
   - สร้างไฟล์รายงาน `logs/reportGender.json`

2. **รัน `rename_images.py`**:
   ```bash
   python scripts/rename_images.py
   ```
   - เปลี่ยนชื่อไฟล์รูปภาพตามรายงาน
   - บันทึกไฟล์รูปภาพที่เปลี่ยนชื่อแล้วใน `data/img_renamed`

---

## ผลลัพธ์

1. **ไฟล์ JSON ที่เปลี่ยนชื่อแล้ว**: อยู่ใน `data/output`
2. **รูปภาพที่เปลี่ยนชื่อแล้ว**: อยู่ใน `data/img_renamed`
3. **Logs**:
   - `logs/script_run.log`: บันทึกการทำงานของ `update_names.py`
   - `logs/rename_images.log`: บันทึกการทำงานของ `rename_images.py`
4. **รายงาน**: `logs/reportGender.json` ที่แสดงการแมปชื่อกับเพศและรูปภาพ


# Uptle_project_cName
