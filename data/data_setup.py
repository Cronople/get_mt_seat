import os
import shutil

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

# 파일 번호
file_num = 0

# 정답 파일 내용
annotation_content = ""

for image_file in image_files:
    # 원본 이미지 파일 경로
    raw_image_path = os.path.join(raw_data_dir, image_file)
    # 대상 이미지 파일 경로
    image_path = os.path.join(image_dir, f"{file_num}.png")  # 파일명 번호 순서로 변경

    # 이미지 파일 복사
    shutil.copy2(raw_image_path, image_path) # copy2는 메타데이터까지 복사
    
    # 파일명에서 정답 추출
    answer = image_file.split(".")[0]  # 확장자 제거

    # 정답 파일 내용 추가
    annotation_content += f"{file_num}.png {answer}\n"

    # 파일 번호 증가
    file_num += 1

# 정답 파일 저장
annotation_file_path = os.path.join(annotation_dir, "file.txt")
with open(annotation_file_path, "w") as f:
    f.write(annotation_content)

print("이미지 파일 이동 및 정답 파일 생성 완료")