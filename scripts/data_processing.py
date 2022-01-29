# Intern
import logging
import lzma
import os
import pickle
import sys

from common import CACHE_FILE
from util.data_processor import DataProcessor

LOGGER = logging.getLogger(__name__)

DEBUG = True
WRITE = False


# TODO: We might also want to be able to pass more than one file
# e.g. wrapping all the following into a function and call that within a loop
# or better(?) add an array of cache files
# or add a folder containing the files and open them all (probably worse)

# Import data
try:
    if os.path.exists(CACHE_FILE):
        with lzma.open(CACHE_FILE, mode="rb") as handle:
            # We are aware of Pickle security implications
            main_data = pickle.load(handle)  # nosec
except FileNotFoundError:
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
