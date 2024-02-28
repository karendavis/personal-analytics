import cv2
import numpy as np
from config import config

TOP_MASK_PERCENTAGE_START = config.TOP_MASK_PERCENTAGE_START
TOP_MASK_PERCENTAGE_END = config.TOP_MASK_PERCENTAGE_END
BOTTOM_MASK_PERCENTAGE_START = config.BOTTOM_MASK_PERCENTAGE_START


def grayscale_to_black_text_transform(image):
    # Convert image to greyscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Convert grayscale image to black and white
    image = cv2.threshold(image, 200, 200, 200)[1]
    return image


def grayscale_to_black_text_transform_with_masking(image):
    # Masking the image, the middle content is largely graphs and is the same colour as the
    # application time text that we want to capture

    # create a mask that will include the top section
    mask = np.zeros(image.shape[:2], np.uint8)
    image_len = image.shape[0]
    top_mask_start = int(image_len * TOP_MASK_PERCENTAGE_START)
    mask_len = int(image_len * TOP_MASK_PERCENTAGE_END)
    mask[top_mask_start:mask_len] = 255

    # create a mask that will include the bottom section (last 20% or so of screen)
    bottom_mask = int(image_len * BOTTOM_MASK_PERCENTAGE_START)
    mask[bottom_mask:image_len] = 255
    masked_image = cv2.bitwise_and(image, image, mask=mask)
    return masked_image


def light_grey_text_to_black_text_transform(image):
    # The bottom light grey text is very light and difficult to read. If we manually convert
    # it to black before converting the entire image to grayscale it will hopefully make it
    # easier to read.

    # iterating over the bottom section of the image only (got to be a better/faster way to do
    # this)
    image_len = image.shape[0]
    image_width = image.shape[1]
    black_bgr = [0, 0, 0]
    for i in range(int(image_len * BOTTOM_MASK_PERCENTAGE_START), image_len - 1):
        for j in range(0, image_width - 1):
            bgr_array = image[i, j]
            if all(250 >= pixel >= 180 for pixel in bgr_array):
                image[i, j] = black_bgr
            j += 1
        i += 1
    return image


def grayscale_to_white_text_black_background_transform(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Get brightness channel
    brightness_channel = image[:, :, 2]
    # Threshold all the very bright pixels
    image = 255 * np.uint8(brightness_channel < 200)
    # converting grayscale to black
    return cv2.threshold(image, 200, 200, 200)[1]


image_transforms = [
    grayscale_to_black_text_transform_with_masking,
    grayscale_to_black_text_transform,
]
