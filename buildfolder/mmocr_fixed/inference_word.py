from mmocr.apis import MMOCRInferencer
import cv2
import time

def inferencing(img):
    model_path = 'buildfolder/mmocr_fixed/configs/textrecog/sar/sar_resnet31_parallel-decoder_custom.py'
    weights_path = 'buildfolder/mmocr_fixed/save/rec_word03/epoch_100.pth'
    start_time = time.time()
    inferencer = MMOCRInferencer(rec=model_path, rec_weights=weights_path, device='cpu')
    word = inferencer(img)
    
    # print('*'*20)
    # print(word['predictions'][0]['rec_texts'][0])
    print('보안문자 추론 소요 시간 ', time.time() - start_time)

    return word['predictions'][0]['rec_texts'][0]