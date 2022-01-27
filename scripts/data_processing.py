# Intern
from common import leaderboard_settings, CACHE_FILE
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


data_processor = DataProcessor.new_with_data(main_data)


sys.exit(0)
# for game, leaderboard, _, _ in leaderboard_settings:
#     main_data[game][leaderboard]


# What can be derived:
# - we can make the players unique on each leaderboard
#   and count them -> same as now, but unique
# - we can count players within a certain amount of activity,
#   e.g. within last day, last 3 days, last 7 days, last 14 days
# - we can join all the unique players across the leaderboards
#   and create overall game activity
# - we can join all the unique players across the games and create
#   overall franchise (AoE2DE, AoE3DE, AoE4) multiplayer activity
