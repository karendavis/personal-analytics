import cv2
import pandas as pd
import pytesseract
import re
from dataclasses import dataclass, asdict
import glob
import os
import logging
from data_loader.transforms import grayscale_to_white_text_black_background_transform, grayscale_to_black_text_transform


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
    logging.info(f"Loading screen time data from this file: {img_file}")
    img = cv2.imread(img_file)
    text = convert_image_to_text(img)
    text = filter_empty_text_items(text)
    # Allow for the case where there is no screen time data
    if "As this device is used, screen time will be" in text:
        # get the date from the file name
        screen_time_date = os.path.basename(img_file).split('at')[0]
        return ScreenTimeItem(date=screen_time_date, total_time=0,
                              applications=[])
    else:
        return create_screen_time_item_from_text(text)


def convert_image_to_text(image) -> list[str]:
    image = grayscale_to_black_text_transform(image)
    text = pytesseract.image_to_string(image).split('\n')
    return text


def filter_empty_text_items(text_items: list) -> list:
    text_items = list(filter(None, text_items))
    text_items = list(filter(lambda item: item.strip(), text_items))
    # This Safari is not the one we want to use for getting the time spent on the application
    safari_regex = re.compile(r'<.*Safari')
    text_items = [x for x in text_items if not safari_regex.match(x)]
    return text_items


def create_screen_time_item_from_text(text_items: list) -> ScreenTimeItem:
    screen_time_date_indexes = [i for i, item in enumerate(text_items) if 'Today,' in item or "Yesterday," in item]
    if len(screen_time_date_indexes) == 0:
        # Some files don't have 'Today, {date}' but a '{day_of_week}, {date}' pattern
        day_of_week_pattern = re.compile("^((?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)),.*")
        screen_time_date_idx = [i for i, item in enumerate(text_items) if re.search(day_of_week_pattern, item)][0]
    else:
        screen_time_date_idx = screen_time_date_indexes[0]

    application_indexes = [i for i, item in enumerate(text_items) if (any(name in item for name in application_names))]
    applications = []
    for index in application_indexes:
        applications.append(ApplicationItem(application_name=text_items[index], application_time=text_items[index+1]))

    return ScreenTimeItem(date=text_items[screen_time_date_idx], total_time=text_items[screen_time_date_idx + 1],
                          applications=applications)
