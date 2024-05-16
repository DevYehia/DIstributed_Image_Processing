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


def increase_contrast(image):
    contrasted_image = cv2.convertScaleAbs(image,alpha = 2.0, beta = 0.0)
    return contrasted_image

def binary(image):
    grayImg = gray(image)
    return cv2.threshold(grayImg,127,255,cv2.THRESH_BINARY)

def brighten(image):
    brighted = cv2.convertScaleAbs(image,alpha = 1.0,beta = 50)
    return brighted

def darken(image):
    darkened = cv2.convertScaleAbs(image,alpha = 1.0,beta = -50)
    return darkened    

def reflect(image):
    reflected = cv2.flip(image,1)
    return reflected

def corners(image):
    operatedImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
  
    # modify the data type 
    # setting to 32-bit floating point 
    operatedImage = np.float32(operatedImage) 
  
    # apply the cv2.cornerHarris method 
    # to detect the corners with appropriate 
    # values as input parameters 
    dest = cv2.cornerHarris(operatedImage, 2, 5, 0.07) 
  
    # Results are marked through the dilated corners 
    dest = cv2.dilate(dest, None) 
  
    # Reverting back to the original image, 
    # with optimal threshold value 
    image[dest > 0.01 * dest.max()]=[0, 0, 255]  
    return image