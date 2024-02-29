import logging
import sys
from screentime.data_loader import load_screen_time_data
from config import config

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def run():
    df = load_screen_time_data(config.folder)
    df.to_csv("~/Development/personal-data-analysis/screen_time_data.csv", index=False)


if __name__ == "__main__":
    run()
