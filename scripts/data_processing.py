# Intern
from common import CACHE_FILE
from util.data_processor import DataProcessor

import logging

# import datetime
import os
import sys
import json

# import sys

LOGGER = logging.getLogger(__name__)

DEBUG = True

# Check for cache hit
if os.path.exists(CACHE_FILE):
    CACHE_HIT = True
    with open(CACHE_FILE, encoding="utf8", mode="r") as handle:
        main_data = json.load(handle)
else:
    CACHE_HIT = False

# Set Debug logging if necessary
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
elif not DEBUG:
    logging.basicConfig(level=logging.INFO)

# Parsing
data_processor = DataProcessor.new_with_data(main_data)

# Does that work.
data_processor.create_unique_player_profiles()
data_processor.calculate_leaderboard_activity()
data_processor.calculate_game_activity()
data_processor.calculate_franchise_activity()
data_processor.count_unique_profiles_per_game()
data_processor.count_unique_profiles_in_franchise()

# Export
data_processor.export_dataset()

sys.exit(0)
