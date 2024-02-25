import cv2
import pandas as pd
import pytesseract
import re
from dataclasses import dataclass, asdict
import glob
import os
import logging

from pytesseract import Output

from data_loader.transforms import image_transforms


@dataclass
class ApplicationItem:
    application_name: str
    application_hour: str
    application_min: str

    def dict(self, index):
        return {f'application_name_{index}': self.application_name, f'application_hour_{index}': self.application_hour,
                f'application_min_{index}': self.application_min}


@dataclass
class ScreenTimeItem:
    day: str
    month: str
    year: str
    total_hour: str
    total_min: str
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
    if not text or len(text) == 0:
        # get the date from the file name
        screen_time_date = os.path.basename(img_file).split('at')[0]
        screen_time_day = screen_time_date.split(' ')[0]
        screen_time_month = screen_time_date.split(' ')[1]
        screen_time_year = screen_time_date.split(' ')[2]
        return ScreenTimeItem(day=screen_time_day,
                              month=screen_time_month,
                              year=screen_time_year,
                              total_hour='0',
                              total_min='0',
                              applications=[])
    else:
        return create_screen_time_item_from_text(text)


def convert_image_to_text(image) -> list[str]:
    for transform in image_transforms:
        image = transform(image)
    text = pytesseract.image_to_data(image, output_type=Output.DICT)['text']
    return text


def filter_empty_text_items(text_items: list) -> list:
    text_items = list(filter(None, text_items))
    text_items = [item.replace('<', '') for item in text_items]
    text_items = [item.replace('.', '') for item in text_items]
    text_items = [item.replace('>', '') for item in text_items]
    text_items = [item.replace('!', '') for item in text_items]
    text_items = [item.replace(':', '') for item in text_items]
    text_items = [item.replace('-', '') for item in text_items]
    text_items = [item.replace('_', '') for item in text_items]
    text_items = [item.replace('—', '') for item in text_items]
    text_items = [item.replace('©', '') for item in text_items]
    text_items = [item.replace('#', '') for item in text_items]
    text_items = [item.replace('Smin', '8min') for item in text_items]
    text_items = [item.replace('Ah', '4h') for item in text_items]
    text_items = [item.replace('Th', '1h') for item in text_items]
    text_items = [item for item in text_items if item != '1']
    text_items = [item for item in text_items if item != "\'"]
    text_items = [item for item in text_items if item != "i"]
    text_items = [item for item in text_items if item != "\\"]
    text_items = [item for item in text_items if item != ","]
    text_items = list(filter(lambda item: item.strip(), text_items))
    # If there are more than two instances of 'safari' in the image, the first is in the top left of the screen
    # and not part of the applications with time section. If there are more than 1 remove the first instance
    remove_indexes = [i for i, item in enumerate(text_items) if 'Safari' in item]
    if len(remove_indexes) > 1:
        text_items.pop(remove_indexes[0])
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
        applications.append(create_application_item_from_text(text_items, index))
    # Drop any None applications
    applications = [application for application in applications if application is not None]
    return ScreenTimeItem(day=text_items[screen_time_date_idx + 1],
                          month=text_items[screen_time_date_idx + 2],
                          year=2024,
                          total_hour=text_items[screen_time_date_idx + 3],
                          total_min=text_items[screen_time_date_idx + 4],
                          applications=applications)


def create_application_item_from_text(text, application_index) -> ApplicationItem:
    application_name = text[application_index]
    time = text[application_index + 1]
    if 'h' in time:
        hour = time
        minutes = text[application_index + 2]
    elif 'min' in time:
        hour = 0
        minutes = time
    else:
        print(f"plus one{time}")
        hour = 0
        minutes = 0

    return ApplicationItem(application_name=application_name,
                           application_hour=hour,
                           application_min=minutes)


