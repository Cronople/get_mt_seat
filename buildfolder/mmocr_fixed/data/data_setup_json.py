import os
import json
import random
import cv2

# 경로 설정
RAW_DATA_DIR = "data/raw_data/"
IMAGE_DIR = "data/image/"
ANNOTATION_DIR = "data/annotation/"
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(ANNOTATION_DIR, exist_ok=True)

# 파일 리스트 가져오기
png_files = [f for f in os.listdir(RAW_DATA_DIR) if f.endswith(".png")]
random.shuffle(png_files)  # 데이터 랜덤 셔플

# Train / Validation 비율
split_ratio = 0.9
split_idx = int(len(png_files) * split_ratio)
train_files, val_files = png_files[:split_idx], png_files[split_idx:]

def convert_and_save(files, json_path):
    annotations = {"metainfo": {"dataset_type": "OCRDataset"}, "data_list": []}
    background_color = (255,255,255)
    
    for file in files:
        img_path = os.path.join(RAW_DATA_DIR, file)
        text_label = os.path.splitext(file)[0]  # 파일명에서 정답 추출
        new_img_name = file.replace(".png", ".jpg")
        new_img_path = os.path.join(IMAGE_DIR, new_img_name)
        
        # PNG -> JPG 변환 및 저장
        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        trans_mask = img[:,:,3] == 0
        img[trans_mask] = [255, 255, 255, 255]
        new_img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        height, width,channel = new_img.shape
        dif = width - height
        square_img = cv2.copyMakeBorder(new_img, dif//2, dif//2, 0, 0, cv2.BORDER_REPLICATE, background_color )
        cv2.imwrite(new_img_path, square_img)
        
        # Annotation 저장
        annotations["data_list"].append({
            "img_path": new_img_path,
            "instances": [{"text": text_label}]
        })
    
    # JSON 파일 저장
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(annotations, f, ensure_ascii=False, indent=4)

# 변환 및 JSON 저장
convert_and_save(train_files, os.path.join(ANNOTATION_DIR, "train.json"))
convert_and_save(val_files, os.path.join(ANNOTATION_DIR, "val.json"))

print("✅ 데이터 변환 및 분할 완료!")
