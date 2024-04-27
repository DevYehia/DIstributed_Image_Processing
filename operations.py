import cv2
import numpy as np
import matplotlib.pyplot as plt

#blurring function
def edges(img):
 edgeImage = cv2.Canny(img, 100, 200)
 return edgeImage

#removing image color function
def gray(img):
 gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 return gray

def rotate(img):
 rot = cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE)
 return rot


#invertion function
def invert_photo(image):
 inverted_image = cv2.bitwise_not(image)
 return inverted_image

def incerase_brightness(image):
    img_float = image.astype(float)
    
    brightened_img = cv2.multiply(img_float, 1.3)
    
    brightened_img = brightened_img.astype('uint8')
    
    return brightened_img

