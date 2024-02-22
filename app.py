from data_loader.screen_time import load_screen_time_data
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

FOLDER = "/Users/karendavis/Library/Mobile Documents/iCloud~is~workflow~my~workflows/Documents/ScreenTime/Karen"


def run():
    df = load_screen_time_data(FOLDER)
    df.to_csv("~/Development/personal-data-analysis/screen_time_data.csv")


if __name__ == '__main__':
    run()
