import pytesseract
from pytesseract import Output
import cv2

from screentime.transforms import image_transforms


def view_ocr_accuracy(image_file, transform_functions):
    image = cv2.imread(image_file)
    for transform_function in transform_functions:
        image = transform_function(image)
    data = pytesseract.image_to_data(image, output_type=Output.DICT)
    highlight_colour = (171, 32, 253)
    for i in range(0, len(data["text"])):
        # extract the bounding box surrounding the text
        left = data["left"][i]
        top = data["top"][i]
        width = data["width"][i]
        height = data["height"][i]

        # extract the text
        text = data["text"][i]
        # strip out non-ASCII text
        text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
        # draw the bounding box
        cv2.rectangle(
            image, (left, top), (left + width, top + height), highlight_colour, 2
        )
        # write the text identified/recognised by OCR
        cv2.putText(
            image,
            text,
            (left, top - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            highlight_colour,
            3,
        )
        # show the output image
        cv2.imshow("Image", image)
        cv2.waitKey(0)
    print(data["text"])


if __name__ == "__main__":
    IMAGE_FILE_PATH = "tests/test_data/zero_seconds_of_screentime.png"
    view_ocr_accuracy(IMAGE_FILE_PATH, image_transforms)
