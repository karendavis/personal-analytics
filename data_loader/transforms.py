import cv2
import numpy as np


def grayscale_to_black_text_transform(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.threshold(image, 200, 200, 200)[1]


def grayscale_to_white_text_black_background_transform(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Get brightness channel
    brightness_channel = image[:, :, 2]
    # Threshold all the very bright pixels
    image = 255 * np.uint8(brightness_channel < 200)
    # converting grayscale to black
    return cv2.threshold(image, 200, 200, 200)[1]
