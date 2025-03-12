import cv2 as cv
import numpy as np
import urllib.request
from mmocr_fixed.inference_word import inferencing


def recognizing(link):
    img = url_to_image(link)
    text = inferencing(img)
    
    return text


def url_to_image(url):
    background_color = (255,255,255)

    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype='uint8')
    image = cv.imdecode(image, cv.IMREAD_UNCHANGED)
    trans_mask = image[:,:,3] == 0
    image[trans_mask] = [255, 255, 255, 255]
    new_img = cv.cvtColor(image, cv.COLOR_BGRA2BGR)
    height, width,channel = new_img.shape
    dif = width - height
    square_img = cv.copyMakeBorder(new_img, dif//2, dif//2, 0, 0, cv.BORDER_REPLICATE, background_color)

    return square_img