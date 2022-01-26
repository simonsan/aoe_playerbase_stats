import logging
import datetime
import os
import json

# Intern
from common import leaderboard_settings

LOGGER = logging.getLogger(__name__)

DEBUG = True


def unpack_list(_list):
    if len(_list) == 0:
        return _list
    if isinstance(_list[0], list):
        return unpack_list(_list[0]) + unpack_list(_list[1:])
    return _list[:1] + unpack_list(_list[1:])


# Check for cache hit
if os.path.exists("./data_temp/cache.json"):
    CACHE_HIT = True
    with open("./data_temp/cache.json", encoding="utf8", mode="r") as handle:
        main_data = json.load(handle)
else:
    CACHE_HIT = False

# Set Debug logging if necessary
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
elif not DEBUG:
    logging.basicConfig(level=logging.INFO)

for leaderboard_setting in leaderboard_settings:
    # TODO: Temporary Flatten
    print(len(unpacked))

# What can be derived:
# - we can make the players unique on each leaderboard
#   and count them -> same as now, but unique
# - we can count players within a certain amount of activity,
#   e.g. within last day, last 3 days, last 7 days, last 14 days
# - we can join all the unique players across the leaderboards
#   and create overall game activity
# - we can join all the unique players across the games and create
#   overall franchise (AoE2DE, AoE3DE, AoE4) multiplayer activity
