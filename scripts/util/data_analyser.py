import datetime
import hashlib
import json
import operator
import os
from collections import Counter, defaultdict
from dataclasses import dataclass

import pandas as pd
import pycountry
from common import (
    ACTIVITY_PERIODS,
    DATASET_FILE,
    FRANCHISE_GAMES,
    LEAVING_PLAYER_ACTIVITY_THRESHOLD,
    NEW_PLAYER_ACTIVITY_THRESHOLD,
    PARQUET_FILE,
    PROFILE_FILE,
    leaderboard_settings,
)

from util.dataset import DataSet
from util.decorators import debug, timer
from util.leaderboard_entry import LeaderboardEntry


@dataclass
class DataAnalyser(object):

    dataset: DataSet

    def append_to_dataset(self, file=DATASET_FILE):
        with open(file, "r") as handle:
            data = json.load(handle)

        data.append(self.dataset.export)

        with open(file, "w") as handle:
            json.dump(data, handle, indent=4)
