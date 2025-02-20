import cv2 as cv
import numpy as np
import urllib.request


def recognizing(link):
    img = url_to_image(link)
    #cv.imshow('captcha',img)
    #cv.waitKey(0)
    
    return ''


def url_to_image(url):
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype='uint8')
    image = cv.imdecode(image, cv.IMREAD_UNCHANGED)
    trans_mask = image[:,:,3] == 0
    image[trans_mask] = [255, 255, 255, 255]
    new_img = cv.cvtColor(image, cv.COLOR_BGRA2BGR)

    return new_img