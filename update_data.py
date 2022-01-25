import logging
import datetime
import json

# Intern
from common import DATA_FILE, leaderboard_settings

# Extern
import requests

LOGGER = logging.getLogger(__name__)

# Main
LOGGER.info("Opening data file ...")
with open(DATA_FILE, "r") as handle:
    leaderboard_data = json.load(handle)
LOGGER.info("Data file loaded.")

now = datetime.datetime.now()

# Setup basic data layout for Yaml file
data_entry = {
    "date": f"{now.strftime('%d')}/{now.strftime('%m')}/{now.strftime('%Y')}",
    "aoe2": {},
    "aoe4": {},
}

# Get data from the server
for leaderboard in leaderboard_settings:
    req = requests.get(f"{leaderboard.url}")
    req = req.json()

    data_entry[f"{leaderboard.game}"][f"{leaderboard.leaderboard}"] = req[
        "recordsFiltered"
    ]

# Append the new data
leaderboard_data.append(data_entry)

# Write data back to yaml
with open(DATA_FILE, "w") as handle:
    json.dump(leaderboard_data, handle)
