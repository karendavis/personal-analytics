import logging
import sys
from screentime.data_loader import load_screen_time_data
from config import config

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def run():
    read_folder = config.icloud_folder + config.screentime_folder
    write_folder = config.data_folder
    df = load_screen_time_data(read_folder)

    df.to_csv(f"{write_folder}/screen_time_data.csv", index=False)


if __name__ == "__main__":
    run()
