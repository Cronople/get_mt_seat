call conda create -n mt_seat_hand python=3.8 -y
call conda activate mt_seat_hand

call python -m pip install --upgrade pip

call pip install -r requirements.txt

call conda deactivate

pause