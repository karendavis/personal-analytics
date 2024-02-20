import cv2
import pandas as pd
import pytesseract
import re
from dataclasses import dataclass, asdict
import glob
import os


@dataclass
class ApplicationItem:
    application_name: str
    application_time: str

    def dict(self, index):
        return {f'application_name_{index}': self.application_name, f'application_time_{index}': self.application_time}


@dataclass
class ScreenTimeItem:
    date: str
    total_time: str
    applications: [ApplicationItem]

    def dict(self):
        dictionary = {k: str(v) for k, v in asdict(self).items()}
        dictionary.pop('applications')
        for row in [application.dict(index) for index, application in enumerate(self.applications)]:
            dictionary.update(row)
        return dictionary


class FolderDoesNotExistError(Exception):
    pass


application_names = ["Safari", "Messages", "DuckDuckGo", "MyFitnessPal", "Connect", "Gmail"]


def load_screen_time_data(folder: str) -> pd.DataFrame:
    if not os.path.isdir(folder):
        raise FolderDoesNotExistError(f"Folder `{folder}` does not exist")

    image_files = glob.glob(f"{folder}/*.png")
    screen_time_data = []
    for image_file in image_files:
        screen_time_data.append(load_screen_time_item(image_file))

    flattened_screen_data = [x.dict() for x in screen_time_data]
    df = pd.DataFrame.from_dict(flattened_screen_data)
    return df


def load_screen_time_item(img_file: str) -> ScreenTimeItem:
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
    # This Safari is not the one we want to use for getting the time spent on the application
    safari_regex = re.compile(r'<.*Safari')
    text_items = [x for x in text_items if not safari_regex.match(x)]
    return text_items


def create_screen_time_item_from_text(text_items: list) -> ScreenTimeItem:
    screen_time_date_idx = [i for i, item in enumerate(text_items) if 'Today,' in item][0]
    application_indexes = [i for i, item in enumerate(text_items) if (any(name in item for name in application_names))]
    applications = []
    for index in application_indexes:
        applications.append(ApplicationItem(application_name=text_items[index], application_time=text_items[index+1]))

    return ScreenTimeItem(date=text_items[screen_time_date_idx], total_time=text_items[screen_time_date_idx + 1],
                          applications=applications)
