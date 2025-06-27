import re
import json
import os

def load_text(filepath):
    with open(filepath, 'r', encoding='gb2312') as f:
        text = f.read()
    return text

def extract_blocks(text):
    # 拆分：病虫害区块 和 杂草防除区块
    parts = re.split(r'# 玉米田杂草防除技术', text)
    pest_part = parts[0]
    weed_part = parts[1] if len(parts) > 1 else ""

    # 病虫害块：以 ### 开头划分
    pest_sections = re.split(r'###\s+', pest_part)[1:]

    pest_data = []
    for section in pest_sections:
        lines = section.split('\n')
        title = lines[0].strip()
        content = '\n'.join(lines[1:])

        # # 每个字段用 **字段名** 抽取
        # # 症状/形态特征字段
        # symptoms = re.search(r'\*\*(症状|形态|形态特征)\*\*：(.*?)(\*\*|$)', content, re.S)
        # if symptoms:
        #     symptom_field = symptoms.group(1).strip()
        #     symptom_content = symptoms.group(2).strip()
        # else:
        #     symptom_field = ""
        #     symptom_content = ""

        # # 发病规律字段
        # rules = re.search(r'\*\*(发病规律|发生规律|生活习性)\*\*：(.*?)(\*\*|$)', content, re.S)
        # if rules:
        #     rule_field = rules.group(1).strip()
        #     rule_content = rules.group(2).strip()
        # else:
        #     rule_field = ""
        #     rule_content = ""

        # # 防治措施字段
        # controls = re.search(r'\*\*(药剂防治|防治措施|防治方法)\*\*：(.*?)(\*\*|$)', content, re.S)
        # if controls:
        #     control_field = controls.group(1).strip()
        #     control_content = controls.group(2).strip()
        # else:
        #     control_field = ""
        #     control_content = ""

        # record = {
        #     "title": title,
        #     "type": "病虫害",
        #     "symptom_field": symptom_field,
        #     "symptom_content": symptom_content,
        #     "rule_field": rule_field,
        #     "rule_content": rule_content,
        #     "control_field": control_field,
        #     "control_content": control_content
        #     # "image": None
        # }

        record = {
            "title": title,
            "content":f"标题：{title}\n 关键字：{section}",
            # "images": [],
            # "image_path":[]
        }
        pest_data.append(record)

    # 杂草防除整体处理
    weed_record = {
        "title": "玉米田杂草防除技术",
        # "type": "杂草防除",
        "content": weed_part.strip()
        # "images": [],
        # "image_path":[]
    }

    return pest_data, weed_record

def match_images(pest_data, weed_record, image_dir):
    image_files = os.listdir(image_dir)
    image_files = [f for f in image_files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    used_images = set()

    # 病虫害图像配对
    for record in pest_data:
        matched_imgs = [img for img in image_files if record['title'] in img]
        record['images'] = matched_imgs
        record['image_path'] = [f"uploaded_images/{img}" for img in matched_imgs]
        used_images.update(matched_imgs)
        
        del record['title']  # 删除 title 字段


    # 杂草防除分配剩余图像
    remaining_images = [img for img in image_files if img not in used_images]
    weed_record['images'] = remaining_images
    weed_record['image_path'] = [f"uploaded_images/{img}" for img in remaining_images]

    return pest_data, weed_record

if __name__ == "__main__":
    text = load_text('data/corn_diseases_pests_weeds.txt')
    pest_data, weed_record = extract_blocks(text)
    # pest_data, weed_record = match_images(pest_data, weed_record, 'data/images/')

    with open("data/structured_data2.json", "w", encoding="utf-8") as f:
        json.dump({"pests": pest_data, "weed": weed_record}, f, ensure_ascii=False, indent=2)

    print("✅ 数据抽取 & 图片配对 完成！")