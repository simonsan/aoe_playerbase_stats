import datetime
import hashlib

import os
from typing import List

import pandas as pd


from ..commons.settings import GLOBAL_SETTINGS
from .decorators import timing
from .leaderboard_entry import LeaderboardEntry

# TODO: Set default value, meaning this will only be
# able to be used for ones own datasets
PEPPER = os.getenv("PEPPER_LEADERBOARD_DATA").encode()


class DataProcessor(object):

    dataframe: pd.DataFrame
    dataframe_update: pd.DataFrame
    with_parquet: bool = False
    collector: List

    def __init__(self):
        self.set_parquet(False)
        self.collector = []

    @timing
    def new_with_parquet_file(
        path: os.path = GLOBAL_SETTINGS["FILESYSTEM"]["PARQUET_FILE_PATH"],
    ):
        d = DataProcessor()
        d.import_dataframe_from_parquet(path)
        return d

    @timing
    def new_without_parquet_file():
        d = DataProcessor()
        d.set_parquet(False)
        return d

    def is_from_parquet(self):
        return self.with_parquet

    def set_parquet(self, _bool: bool = False):
        self.with_parquet = _bool

    @timing
    def process_new_data_from(self, data):
        date = datetime.datetime.fromisoformat(data["date"])

        for (game, leaderboard, _, _, _,) in GLOBAL_SETTINGS[
            "VARIABLES"
        ]["LEADERBOARD_SETTINGS"]:

            for entry in data[game][leaderboard]:
                self.collector.append(
                    LeaderboardEntry(
                        timestamp=date,
                        game=game,
                        leaderboard=leaderboard,
                        steam_id=DataProcessor.pseudonymise(entry["steam_id"])
                        if entry["steam_id"] is not None
                        else None,
                        profile_id=DataProcessor.pseudonymise(
                            entry["profile_id"]
                        ),
                        rank=entry["rank"],
                        rating=entry["rating"],
                        highest_rating=entry["highest_rating"],
                        previous_rating=entry["previous_rating"],
                        country_code=entry["country_code"],
                        name=DataProcessor.pseudonymise(entry["name"])
                        if entry["name"] is not None
                        else None,
                        known_name=DataProcessor.pseudonymise(
                            entry["known_name"]
                        )
                        if entry["known_name"] is not None
                        else None,
                        # avatar=entry["avatar"],
                        # avatarfull=entry["avatarfull"],
                        # avatarmedium=entry["avatarmedium"],
                        num_games=entry["num_games"],
                        streak=entry["streak"],
                        num_wins=entry["num_wins"],
                        win_percent=entry["win_percent"],
                        rating24h=entry["rating24h"],
                        games24h=entry["games24h"],
                        wins24h=entry["wins24h"],
                        last_match=entry["last_match"],
                    ).__dict__
                )

    def pseudonymise(plaintext):
        ###
        # DON'T USE FOR PASSWORDS, NOT SECURE
        ###
        plaintext = f"{plaintext}".encode()
        # Let's keep this simple, more privacy is already given with just
        # '1' iteration. We just don't want to work with plaintext.
        digest = hashlib.pbkdf2_hmac("sha224", plaintext, PEPPER, 1)
        return digest

    @timing
    def produce_dataframe(self):
        self.create_dataframe_from_collector()
        if self.is_from_parquet():
            self.append_to_dataframe_in_parquet()

    @timing
    def import_dataframe_from_parquet(
        self, path=GLOBAL_SETTINGS["FILESYSTEM"]["PARQUET_FILE_PATH"]
    ):
        self.dataframe = pd.read_parquet(path, engine="pyarrow")
        self.set_parquet(True)

    @timing
    def append_to_dataframe_in_parquet(self):
        if self.is_from_parquet():
            concat_df = pd.concat(
                [self.dataframe, self.dataframe_update], ignore_index=True
            )
            self.dataframe = concat_df

    @timing
    def export_dataframe_to_parquet(
        self,
        path=GLOBAL_SETTINGS["FILESYSTEM"]["PARQUET_FILE_PATH"],
        engine="pyarrow",
        compression="brotli",
        index=True,
    ):
        self.dataframe.to_parquet(
            path=path,
            engine=engine,
            compression=compression,
            index=index,
        )

    @timing
    def create_dataframe_from_collector(self):
        if self.is_from_parquet():
            self.dataframe_update = pd.DataFrame(self.collector)
        else:
            self.dataframe = pd.DataFrame(self.collector)
