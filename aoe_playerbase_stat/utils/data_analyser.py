import datetime
import json
from dataclasses import dataclass

import pandas as pd
# import pycountry
from aoe_playerbase_stat.settings import GLOBAL_SETTINGS
from aoe_playerbase_stat.utils.dataset import DataSet

# from util.decorators import debug, timer
# from util.leaderboard_entry import LeaderboardEntry


@dataclass
class DataAnalyser(object):

    dataset: DataSet
    date: datetime.datetime
    dataframe: pd.DataFrame

    def append_to_dataset(
        self, file=GLOBAL_SETTINGS["VARIABLES"]["DATASET_FILE_PATH"]
    ):
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

    def import_dataframe_from_parquet(
        self, file=GLOBAL_SETTINGS["VARIABLES"]["PARQUET_FILE_PATH"]
    ):
        self.dataframe = pd.read_parquet(file, engine="pyarrow")

    def create_leaderboard_player_count(self):
        new = self.dataframe.groupby(
            ["timestamp", "game", "leaderboard"]
        ).size()
        new.tail(1)
        new.to_json("data/test.json", indent=4)
