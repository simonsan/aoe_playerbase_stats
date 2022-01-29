# Intern
from util.data_processor import DataProcessor
from common import DATA_FILE_NAME, TEMP_DATA_FOLDER

import logging

# import datetime
import os
import sys
import json

# import sys

LOGGER = logging.getLogger(__name__)

DEBUG = True
WRITE = True

# TODO: We might also want to be able to pass more than one file


# Import data
try:
    if os.path.exists(f"{TEMP_DATA_FOLDER}{DATA_FILE_NAME}"):
        with open(
            f"{TEMP_DATA_FOLDER}{DATA_FILE_NAME}", encoding="utf8", mode="r"
        ) as handle:
            main_data = json.load(handle)
except:
    LOGGER.error("DataFile not found.")

# Set Debug logging if necessary
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
elif not DEBUG:
    logging.basicConfig(level=logging.INFO)

# Parsing
data_processor = DataProcessor.new_with_data(main_data)

# Does all that juicy work.
data_processor.create_unique_player_profiles()

# Utility
data_processor.save_profile_stats()

# Statistics
data_processor.calculate_leaderboard_activity()
data_processor.calculate_game_activity()
data_processor.calculate_franchise_activity()
data_processor.countries_per_game()
data_processor.countries_for_franchise()
data_processor.platforms_per_game()
data_processor.platforms_for_franchise()

# DEBUG: Export new dataset
# if WRITE:
# data_processor.export_dataset()

# Append to old dataset
if WRITE:
    data_processor.append_to_dataset()

sys.exit(0)
