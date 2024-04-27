import cv2
import numpy as np
import matplotlib.pyplot as plt

#Edge Detection Function
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


