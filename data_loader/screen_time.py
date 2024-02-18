import cv2
import pytesseract
import re
from dataclasses import dataclass


@dataclass
class ScreenTimeItem:
    date: str
    total_time: str
    applications: []


application_names = ["Safari", "Messages", "DuckDuckGo", "MyFitnessPal", "Connect", "The Lott", "Gmail"]


def load_screen_time_data(img_file: str) -> ScreenTimeItem:
    img = cv2.imread(img_file)
    ref = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ref = cv2.threshold(ref, 200, 200, 200)[1]

    text = pytesseract.image_to_string(ref).split('\n')
    text = filter_empty_text_items(text)
    screen_time_data = create_screen_time_item_from_text(text)
    return screen_time_data


def filter_empty_text_items(text_items: list) -> list:
    text_items = list(filter(None, text_items))
    text_items = list(filter(lambda item: item.strip(), text_items))
    # This Safari is not the one we want to use for application time
    # text_items.remove('< Safari')
    safari_regex = re.compile(r'<.*Safari')
    text_items = [x for x in text_items if not safari_regex.match(x)]
    return text_items


def create_screen_time_item_from_text(text_items: list) -> list:
    screen_time_date_idx = [i for i, item in enumerate(text_items) if 'Today,' in item][0]

    application_indexes = [i for i, item in enumerate(text_items) if (any(name in item for name in application_names))]

    applications = {}
    for index in application_indexes:
        applications[text_items[index]] = text_items[index+1]

    return ScreenTimeItem(date=text_items[screen_time_date_idx], total_time=text_items[screen_time_date_idx + 1],
                          applications=applications)
