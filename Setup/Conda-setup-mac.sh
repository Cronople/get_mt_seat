#!/bin/bash

# 콘다 환경 생성 및 활성화
conda create -n mt_seat_cpu python=3.8 -y
conda activate mt_seat_cpu

python -m pip install --upgrade pip

pip install torch==1.8.0 torchvision==0.9.0 torchaudio==0.8.0

pip install -r requirements.txt

pip install -U openmim
mim install mmengine
pip install mmcv==2.0.0rc4 -f https://download.openmmlab.com/mmcv/dist/cpu/torch1.8/index.html
mim install mmdet==3.1.0
mim install mmocr

conda deactivate

read -p "Installation done. Press any key."