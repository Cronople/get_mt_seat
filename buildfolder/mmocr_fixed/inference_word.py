from mmocr.apis import TextRecInferencer
import cv2 as cv
import time
from mmengine.logging import MMLogger


def local_img2square(path):
    image = cv.imread(path, cv.IMREAD_UNCHANGED)

    background_color = (255,255,255)
    trans_mask = image[:,:,3] == 0
    image[trans_mask] = [255, 255, 255, 255]
    new_img = cv.cvtColor(image, cv.COLOR_BGRA2BGR)
    height, width,channel = new_img.shape
    dif = width - height
    square_img = cv.copyMakeBorder(new_img, dif//2, dif//2, 0, 0, cv.BORDER_REPLICATE, background_color)

    return square_img


def preload_inferencer(device_name, logLevel):
    model_path = 'buildfolder/mmocr_fixed/configs/textrecog/sar/sar_resnet31_parallel-decoder_custom.py'
    weights_path = 'buildfolder/mmocr_fixed/save/rec_word03/epoch_100.pth'
        
    inferencer = TextRecInferencer(model=model_path, weights=weights_path, device=device_name)

    if device_name != 'cpu':
        inferencer(local_img2square('buildfolder/mmocr_fixed/test_img/none.png'))

    return inferencer


def inferencing(img, inferencer, logLevel):
    start_time = time.time()
    word = inferencer(img)
    
    # print(word['predictions'][0]['rec_texts'][0])
    if logLevel <= 3:
        print('보안문자 추론 소요 시간 ', time.time() - start_time)

    return word['predictions'][0]['text']