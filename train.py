from mmocr.apis import init_detector, inference_detector
from mmocr.datasets import build_dataset
from mmengine.runner import load_checkpoint, save_checkpoint
from albumentations import (
    Compose, RandomCrop, RandomBrightnessContrast,
    RandomRotate, ShiftScaleRotate, HorizontalFlip,
    RandomSizedBBoxSafeCrop, HueSaturationValue, RGBShift,
    RandomResizedCrop
)
import numpy as np
import os

# 설정 파일 경로
config_file = 'configs/textrecog/svtr/svtr_small_freeze.py'
# 체크포인트 파일 경로
checkpoint_file = 'checkpoints/svtr_small_pretrain.pth'

# 모델 초기화
model = init_detector(config_file, checkpoint=checkpoint_file, device='cuda')

# Albumentations augmentation 정의
transform = Compose([
    ShiftScaleRotate(shift_limit=5, scale_limit=0, rotate_limit=5, p=0.5, border_mode = 0) # x, y 좌표를 +-5 이내로 움직이는 augmentation
])

# 데이터셋 설정
data_cfg = dict(
    type='OCRDataset',
    img_prefix='path/to/your/image/folder',
    ann_file='path/to/your/annotation/file.txt',
    test_mode=False,
    pipeline=[
        dict(type='LoadImageFromFile'),
        dict(type='Resize', img_scale=(100, 32)),
        dict(type='Normalize', mean=[127.5, 127.5, 127.5], std=[127.5, 127.5, 127.5]),
        dict(type='ToTensor'),
        dict(type='Collect', keys=['img'], meta_keys=['gt_label'])
    ])

# 데이터셋 빌드
dataset = build_dataset(data_cfg)

# 데이터셋 split
train_size = int(len(dataset) * 0.9)
val_size = len(dataset) - train_size
train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

# 모델 가중치 동결
for name, param in model.named_parameters():
    if 'module.backbone' in name:
        param.requires_grad = False

# 훈련
num_epochs = 100
best_loss = np.inf
patience = 3
counter = 0

# 모델 저장 경로 설정
save_dir = '/saved_model/stvr_small_modified/'
os.makedirs(save_dir, exist_ok=True)

for epoch in range(num_epochs):
    # 매 epoch 마다 데이터 섞기
    train_dataset.shuffle()
    val_dataset.shuffle()

    # 훈련 시작
    model.train_step(data_loader=train_dataset.data_loader, optimizer=model.optimizer)

    # 검증
    result = model.evaluate(val_dataset)
    val_loss = result['loss']

    # Early stopping
    if val_loss < best_loss:
        best_loss = val_loss
        counter = 0

        # best model 저장
        save_path = os.path.join(save_dir, 'best_model.pth')
        save_checkpoint(model, save_path)
        print(f"Best model saved at {save_path}")
    else:
        counter += 1
        if counter >= patience:
            print(f"Early stopping at epoch {epoch+1}")
            break

    print(f"Epoch: {epoch+1}, Validation Loss: {val_loss}")

# 추론
img = 'path/to/your/image.jpg'
result = inference_detector(model, img)
print(result)