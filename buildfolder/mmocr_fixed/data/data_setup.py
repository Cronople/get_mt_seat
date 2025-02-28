import os
import shutil
import cv2
import random

# 원본 이미지 파일 경로
raw_data_dir = "data/raw_data"
# 대상 이미지 파일 경로
image_dir = "data/image"
# 정답 파일 경로
annotation_dir = "data/annotation"

# 대상 디렉토리 생성
os.makedirs(image_dir, exist_ok=True)
os.makedirs(annotation_dir, exist_ok=True)

# 파일 목록 얻기
image_files = os.listdir(raw_data_dir)
random.shuffle(image_files)

# train/test 데이터 분리
train_size = int(len(image_files) * 0.8)  # 80% train
train_files = image_files[:train_size]
test_files = image_files[train_size:]

# 파일 번호
file_num = 0

# 정답 파일 내용
train_annotation_content = ""
test_annotation_content = ""

for image_file in image_files:
    # 원본 이미지 파일 경로
    raw_image_path = os.path.join(raw_data_dir, image_file)
    # 대상 이미지 파일 경로
    image_path = os.path.join(image_dir, f"{file_num}.jpg")  # 파일명 번호 순서로 변경

    # 이미지 파일 확장자 확인 및 jpg로 변환
    if image_file.lower().endswith(".png"):
        img = cv2.imread(raw_image_path, cv2.IMREAD_UNCHANGED)
        trans_mask = img[:,:,3] == 0
        img[trans_mask] = [255, 255, 255, 255]
        new_img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        cv2.imwrite(image_path, new_img)
    else: # png 파일이 아닌 경우 복사
        shutil.copy2(raw_image_path, image_path)
    
    # 파일명에서 정답 추출
    answer = image_file.split(".")[0]  # 확장자 제거

    # 정답 파일 내용 추가
    if image_file in train_files:
        train_annotation_content += f"{file_num}.jpg {answer}\n"
    else:
        test_annotation_content += f"{file_num}.jpg {answer}\n"

    # 파일 번호 증가
    file_num += 1

# 정답 파일 저장
train_annotation_file_path = os.path.join(annotation_dir, "train_file.txt")
test_annotation_file_path = os.path.join(annotation_dir, "test_file.txt")
with open(train_annotation_file_path, "w") as f:
    f.write(train_annotation_content)
    f.close()
with open(test_annotation_file_path, "w") as f:
    f.write(test_annotation_content)
    f.close()

print("이미지 파일 이동 및 정답 파일 생성 완료")