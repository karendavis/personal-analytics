import cv2
import pytesseract
from dataclasses import dataclass


@dataclass
class ScreenTimeItem:
    date: str
    total_time: str
    applications: []


def load_screen_time_data(img_file: str) -> ScreenTimeItem:
    img = cv2.imread(img_file)
    ref = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ref = cv2.threshold(ref, 200, 200, 200)[1]
    text = pytesseract.image_to_string(ref).split('\n')
    screen_time_data = ScreenTimeItem(date=text[10], total_time=text[12],
                                      applications={text[26]: text[27],
                                                    text[29]: text[30],
                                                    text[32]: text[34]})
    return screen_time_data


