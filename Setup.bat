python -m pip install --upgrade pip

pip install torch==1.8.0+cpu torchvision==0.9.0+cpu torchaudio==0.8.0 -f https://download.pytorch.org/whl/torch_stable.html

pip install -r buildfolder\requirements.txt

pip install -U openmim
mim install mmengine
pip install buildfolder/mmcv-2.0.0rc4-cp38-cp38-win_amd64.whl
mim install mmdet==3.1.0
mim install mmocr
