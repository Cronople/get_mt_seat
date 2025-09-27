call conda create -n mt_seat_gpu python=3.8 -y
call conda activate mt_seat_gpu

call python -m pip install --upgrade pip

call pip install torch==1.8.0 torchvision==0.9.0 torchaudio==0.8.0
call pip install -r requirements.txt

call pip install -U openmim
call mim install mmengine
call mim install mmcv==2.0.0rc4
call mim install mmdet==3.1.0
call mim install mmocr

call conda deactivate

pause