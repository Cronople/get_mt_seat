call conda create -n mt_seat_cpu python=3.8 -y
call conda activate mt_seat_cpu

call python -m pip install --upgrade pip

call pip install torch==1.8.0+cpu torchvision==0.9.0+cpu torchaudio==0.8.0 -f https://download.pytorch.org/whl/torch_stable.html

call pip install -r requirements.txt

call pip install -U openmim
call mim install mmengine
call pip install mmcv-2.0.0rc4-cp38-cp38-win_amd64.whl
call mim install mmdet==3.1.0
call mim install mmocr

call conda deactivate

pause