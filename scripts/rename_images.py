# rename_images.py
import os
import json
import shutil
import logging

# ตั้งค่า path สำหรับไฟล์ report และโฟลเดอร์รูปภาพ
report_file = 'logs/reportGender.json'
img_dir = 'data/img'
output_img_dir = 'data/img_renamed'

# สร้างโฟลเดอร์ output_img_dir หากยังไม่มี
os.makedirs(output_img_dir, exist_ok=True)

# ตั้งค่า logging
logging.basicConfig(
    filename='logs/rename_images.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# ฟังก์ชันเพื่อกรองเฉพาะไฟล์รูปภาพที่ต้องการ
def get_image_files(directory):
    supported_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')
    return [f for f in sorted(os.listdir(directory)) if f.lower().endswith(supported_extensions)]

def rename_images_from_report():
    try:
        # โหลดข้อมูลจาก reportGender.json
        with open(report_file, 'r', encoding='utf-8') as f:
            report_data = json.load(f)
    except FileNotFoundError:
        logging.error(f"Report file {report_file} not found.")
        print(f"Error: Report file {report_file} not found.")
        return
    except json.JSONDecodeError:
        logging.error(f"Report file {report_file} contains invalid JSON.")
        print(f"Error: Report file {report_file} contains invalid JSON.")
        return

    # จัดกลุ่มข้อมูลรูปภาพตาม gender
    gender_map = {'male': [], 'female': []}
    for entry in report_data:
        gender = entry.get('gender', '').lower()
        image_name = entry.get('image', '')
        if gender in gender_map and image_name:
            gender_map[gender].append(image_name)

    # แยกไฟล์ในโฟลเดอร์ male และ female โดยกรองเฉพาะรูปภาพ
    male_dir = os.path.join(img_dir, 'male')
    female_dir = os.path.join(img_dir, 'female')
    male_images = get_image_files(male_dir)
    female_images = get_image_files(female_dir)

    # ฟังก์ชันสำหรับการเปลี่ยนชื่อรูปภาพโดยใช้การวนซ้ำเมื่อไม่พอ
    def rename_gender_images(gender, new_names, source_images):
        num_source = len(source_images)
        if num_source == 0:
            logging.error(f"No image files found in '{gender}' folder.")
            print(f"Error: No image files found in '{gender}' folder.")
            return

        for idx, new_name in enumerate(new_names):
            # ใช้การวนซ้ำเมื่อไม่พอจำนวนรูปภาพ
            source_idx = idx % num_source
            old_path = os.path.join(img_dir, gender, source_images[source_idx])
            new_path = os.path.join(output_img_dir, f"{new_name}.jpg")
            try:
                shutil.copy(old_path, new_path)
                logging.info(f"Renamed: {old_path} -> {new_path}")
                print(f"Renamed: {old_path} -> {new_path}")
            except Exception as e:
                logging.error(f"Failed to copy {old_path} to {new_path}: {e}")
                print(f"Error: Failed to copy {old_path} to {new_path}: {e}")

    # เปลี่ยนชื่อรูปภาพสำหรับเพศชายและหญิง โดยใช้การวนซ้ำเมื่อไม่พอจำนวนรูปภาพ
    rename_gender_images('male', gender_map['male'], male_images)
    rename_gender_images('female', gender_map['female'], female_images)

if __name__ == "__main__":
    rename_images_from_report()
