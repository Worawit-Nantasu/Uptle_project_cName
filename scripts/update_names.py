#update_names.py
import os
import json
import random
import datetime

# ตั้งค่า path สำหรับไฟล์ชื่อและไฟล์ input/output
names_file = 'data/ja_names.json'
input_dir = 'data/input'
output_dir = 'data/output'
logs_dir = 'logs'

# สร้างโฟลเดอร์ logs หากยังไม่มี
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# สร้าง/เปิดไฟล์ script_run.log ในโหมด append
script_log_path = os.path.join(logs_dir, 'script_run.log')
script_log_file = open(script_log_path, 'a', encoding='utf-8')

def log_message(message):
    # ใส่ timestamp ลงไปใน log
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"{timestamp} - {message}\n"
    # แสดงผลบน console
    print(log_line.strip())
    # บันทึกลงไฟล์ log
    script_log_file.write(log_line)
    script_log_file.flush()

# โหลดรายชื่อจากไฟล์ ja_names.json
with open(names_file, 'r', encoding='utf-8') as f:
    names_data = json.load(f)

# สร้าง map สำหรับค้นหาเพศจากชื่อ
name_gender_map = {}
for entry in names_data:
    if 'name' in entry and 'gender' in entry:
        name_gender_map[entry['name']] = entry['gender']

# สร้าง list ของชื่อทั้งหมด (ตาม key "name")
all_names = [entry['name'] for entry in names_data if 'name' in entry]

if not all_names:
    raise ValueError("No names found in ja_names.json")

# สร้างโฟลเดอร์ output หากยังไม่มี
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# ขั้นตอนที่ 1: สแกนไฟล์ทั้งหมดเพื่อรวบรวมจำนวนฟิลด์ที่ต้องเปลี่ยนชื่อ
files_to_process = []
total_keys_to_replace = 0

for filename in os.listdir(input_dir):
    if not filename.endswith('.json'):
        continue
    input_path = os.path.join(input_dir, filename)

    with open(input_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            log_message(f"Skipping {filename}: Invalid JSON")
            continue
    
    if 'rating_schema' in data and isinstance(data['rating_schema'], list):
        keys_to_replace = []
        for item in data['rating_schema']:
            if 'clientName' in item:
                keys_to_replace.append(('clientName', item))
            clevel_keys = [k for k in item.keys() if k.startswith('clevel')]
            for ck in clevel_keys:
                keys_to_replace.append((ck, item))
        
        files_to_process.append((filename, data, keys_to_replace))
        total_keys_to_replace += len(keys_to_replace)
    else:
        # ไม่มี rating_schema หรือไม่ใช่ list ก็เก็บข้อมูลเดิมไว้
        files_to_process.append((filename, data, []))

# ไม่ต้องตรวจสอบว่าชื่อพอหรือไม่ เพราะเราจะอนุญาตให้ซ้ำได้

# ขั้นตอนที่ 2: สุ่มเรียงลำดับชื่อทั้งหมดครั้งเดียว
random.shuffle(all_names)

# ใช้ตัวแปร current_name_index ในการวนชื่อ
current_name_index = 0

# สร้าง list เพื่อเก็บข้อมูล reportGender
report_list = []

# ขั้นตอนที่ 3: แทนค่าชื่อในไฟล์ทั้งหมด
for (filename, data, keys_to_replace) in files_to_process:
    if keys_to_replace:
        for (key, obj) in keys_to_replace:
            new_name = all_names[current_name_index % len(all_names)]
            obj[key] = new_name
            current_name_index += 1
    
    # บันทึกไฟล์ JSON ที่แก้ไขแล้วลงใน output_dir
    output_path = os.path.join(output_dir, filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    log_message(f"Processed and saved: {output_path}")

    # หลังจากเปลี่ยนชื่อเสร็จ ตรวจสอบข้อมูลใน rating_schema เพื่อนำไปลง reportGender
    if 'rating_schema' in data and isinstance(data['rating_schema'], list):
        for item in data['rating_schema']:
            if 'image' in item and 'clientName' in item:
                client_name = item['clientName']
                gender = name_gender_map.get(client_name, "unknown")
                report_list.append({
                    "image": item["image"],
                    "clientName": client_name,
                    "gender": gender
                })

# ขั้นตอนที่ 4: บันทึกข้อมูล reportGender.json ในโฟลเดอร์ logs
report_path = os.path.join(logs_dir, 'reportGender.json')
with open(report_path, 'w', encoding='utf-8') as f:
    json.dump(report_list, f, ensure_ascii=False, indent=2)
log_message(f"Report saved: {report_path}")

# ปิดไฟล์ log เมื่อเสร็จสิ้นงาน
script_log_file.close()
