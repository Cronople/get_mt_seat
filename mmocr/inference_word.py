from mmocr.apis import MMOCRInferencer
import cv2
import time

def image_convert(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    trans_mask = img[:,:,3] == 0
    img[trans_mask] = [255, 255, 255, 255]
    new_img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    height, width,channel = new_img.shape
    dif = width - height
    square_img = cv2.copyMakeBorder(new_img, dif//2, dif//2, 0, 0, cv2.BORDER_REPLICATE, background_color)
    return square_img

start_time = time.time()

img_path = 'test_img/test4.png'
img_path2 = 'test_img/test2.png'
model_path = 'configs/textrecog/sar/sar_resnet31_parallel-decoder_custom.py'
weights_path = 'save/rec_word03/epoch_100.pth'
background_color = (255,255,255)

inferencer = MMOCRInferencer(rec=model_path, rec_weights=weights_path, device='cpu')

square_img = image_convert(img_path)
word = inferencer(square_img)
print('*'*20)
print(word['predictions'][0]['rec_texts'][0])
print(time.time() - start_time)