import datetime
import json
from dataclasses import dataclass

import pandas as pd

# import pycountry
from util.common import (
    # ACTIVITY_PERIODS,
    DATASET_FILE,
    # FRANCHISE_GAMES,
    # LEAVING_PLAYER_ACTIVITY_THRESHOLD,
    # NEW_PLAYER_ACTIVITY_THRESHOLD,
    PARQUET_FILE,
    # leaderboard_settings,
)

from util.dataset import DataSet

# from util.decorators import debug, timer
# from util.leaderboard_entry import LeaderboardEntry


@dataclass
class DataAnalyser(object):

    dataset: DataSet
    date: datetime.datetime
    dataframe: pd.DataFrame

    def append_to_dataset(self, file=DATASET_FILE):
        with open(file, "r") as handle:
            data = json.load(handle)

        data.append(self.dataset.export)

        with open(file, "w") as handle:
            json.dump(data, handle, indent=4)

    def new_with_parquet_file():
        d = DataAnalyser(None, datetime.datetime.now(), None)
        d.import_dataframe_from_parquet()
        d.dataset = DataSet()
        return d

    def import_dataframe_from_parquet(self, file=PARQUET_FILE):
        self.dataframe = pd.read_parquet(file, engine="pyarrow")

    def create_leaderboard_player_count(self):
        new = self.dataframe.groupby(
            ["timestamp", "game", "leaderboard"]
        ).size()
        new.tail(1)
        new.to_json("data/test.json", indent=4)
