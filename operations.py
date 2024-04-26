import cv2
import numpy as np
import matplotlib.pyplot as plt

#blurring function
def blur(img):
 blurred = cv2.GaussianBlur(img, (3, 3), 0)
 return blurred

#removing image color function
def gray(img):
 gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 return gray

def rotate(img):
 rot = cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE)
 return rot

#removing the salt and pepper noise function
def apply_median_filter(image, kernel_size=7):
# Apply median filter to the image
 return cv2.medianBlur(image, kernel_size)

#invertion function
def invert_photo(image):
 inverted_image = cv2.bitwise_not(image)
 return inverted_image

def incerase_brightness(image):
    img_float = image.astype(float)
    
    brightened_img = cv2.multiply(img_float, 1.3)
    
    brightened_img = brightened_img.astype('uint8')
    
    return brightened_img

#check and adjust contrast function
def check_and_adjust_contrast(image):
    # Convert the image to grayscale if it's a color image
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Compute the histogram
    hist, bins = np.histogram(image.flatten(), 256, [0, 256])
    # Calculate the cumulative distribution function (CDF)
    cdf = hist.cumsum()

    # Normalize the CDF
    cdf_normalized = cdf * hist.max() / cdf.max()

    # Find the midpoint where the histogram is split into two halves
    midpoint = np.argmax(cdf_normalized >= 0.5 * cdf_normalized.max())

    # Check if the midpoint is below the target contrast
    if midpoint == 125:
        # Adjust the image contrast using histogram equalization
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        equalized_image = clahe.apply(image)
        thresh_img = cv2.adaptiveThreshold(
        src=equalized_image,
        maxValue=255,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv2.THRESH_BINARY_INV,
        blockSize=251,
        C=5
        )
        print("Contrast adjusted")
        thresh_img = cv2.cvtColor(thresh_img, cv2.COLOR_GRAY2BGR)
        plt.imshow(thresh_img, cmap="gray")
        plt.title("C corrected")
        plt.show()
        return thresh_img
    else:
        print("Contrast is good. No further processing needed.")
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        return image
