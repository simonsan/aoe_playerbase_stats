import datetime
import hashlib
import operator
import os
from collections import Counter, defaultdict

import pandas as pd
import pycountry
from .common import (
    GLOBAL_SETTINGS,
    PARQUET_FILE,
)

from .dataset import DataSet
from .decorators import timing
from .leaderboard_entry import LeaderboardEntry

# TODO: Set default value, meaning this will only be
# able to be used for ones own datasets
PEPPER = os.getenv("PEPPER_LEADERBOARD_DATA").encode()


class DataProcessor(object):

    date: datetime.datetime
    data: dict
    dataset: DataSet
    profile_stats: dict
    dataframe: pd.DataFrame
    dataframe_update: pd.DataFrame

    def __init__(self):
        self.date = None
        self.data = {}
        self.dataset = DataSet()
        self.profile_stats = {
            "aoe2": 0,
            "aoe3": 0,
            "aoe4": 0,
            "franchise": 0,
        }

        def unique_profiles_defaultdict():
            return defaultdict(unique_profiles_defaultdict)

        self.unique_profiles = unique_profiles_defaultdict()

    @timing
    def new_with_collected_data(data):
        d = DataProcessor()
        d.date = datetime.datetime.fromisoformat(data["date"])
        d.dataset.set_date(d.date)
        d.data = {
            "aoe2": {},
            "aoe3": {},
            "aoe4": {},
        }

        for (
            game,
            leaderboard,
            _,
            _,
            _,
        ) in GLOBAL_SETTINGS["LEADERBOARD_SETTINGS"]:
            collector = []

            for entry in data[game][leaderboard]:
                collector.append(
                    LeaderboardEntry(
                        timestamp=d.date,
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
                    )
                )

            d.data[game][leaderboard] = collector

        return d

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
    def update_parquet_file(self, file=PARQUET_FILE):
        self.import_dataframe_from_parquet(file)
        self.create_dataframe_from_newly_collected_data()
        self.append_to_dataframe_in_parquet()
        self.export_dataframe_to_parquet(file)

    def import_dataframe_from_parquet(self, file=PARQUET_FILE):
        self.dataframe = pd.read_parquet(file, engine="pyarrow")

    def append_to_dataframe_in_parquet(self):
        concat_df = pd.concat(
            [self.dataframe, self.dataframe_update], ignore_index=True
        )
        self.dataframe = concat_df

    @timing
    def export_dataframe_to_parquet(
        self,
        file=PARQUET_FILE,
        engine="pyarrow",
        compression="brotli",
        index=True,
    ):
        self.dataframe.to_parquet(
            file,
            engine=engine,
            compression=compression,
            index=index,
        )

    @timing
    def create_dataframe_from_newly_collected_data(
        self, mode="update_existing"
    ):
        collection = []
        for game in GLOBAL_SETTINGS["FRANCHISE_GAMES"]:
            for leaderboard in self.data[game].keys():
                for row in self.data[game][leaderboard]:
                    collection.append(row.__dict__)
        if mode == "update_existing":
            self.dataframe_update = pd.DataFrame(collection)
        elif mode == "create_new":
            self.dataframe = pd.DataFrame(collection)

    def create_player_profiles(self):
        for (
            game,
            leaderboard,
            _,
            _,
            bit_mask,
        ) in GLOBAL_SETTINGS["LEADERBOARD_SETTINGS"]:
            for entry in self.data[game][leaderboard]:

                def _helper_set_value_if(
                    self, mut_val, set_val, cmp_type, cmp_act="<"
                ):
                    """Helper function to replace a mutable value with a new value

                    Args:
                        mut_val: Tuple of data path within self
                        set_val: Value that will replace mutable value
                        cmp_type: Type to compare with if initial mutable
                                  value is empty
                        cmp_act: Type of comparison, Default: "<",
                                 possible values: ["<", ">", "<=", ">="]

                    """

                    if not isinstance(
                        self.unique_profiles[mut_val[0]][mut_val[1]][
                            mut_val[2]
                        ][mut_val[3]][mut_val[4]],
                        cmp_type,
                    ):
                        if (
                            len(
                                self.unique_profiles[mut_val[0]][mut_val[1]][
                                    mut_val[2]
                                ][mut_val[3]][mut_val[4]]
                            )
                            == 0
                        ):
                            self.unique_profiles[mut_val[0]][mut_val[1]][
                                mut_val[2]
                            ][mut_val[3]][mut_val[4]] = set_val
                    elif (
                        cmp_act == "<"
                        and self.unique_profiles[mut_val[0]][mut_val[1]][
                            mut_val[2]
                        ][mut_val[3]][mut_val[4]]
                        < set_val
                    ):
                        self.unique_profiles[mut_val[0]][mut_val[1]][
                            mut_val[2]
                        ][mut_val[3]][mut_val[4]] = set_val
                    elif (
                        cmp_act == ">"
                        and self.unique_profiles[mut_val[0]][mut_val[1]][
                            mut_val[2]
                        ][mut_val[3]][mut_val[4]]
                        > set_val
                    ):
                        self.unique_profiles[mut_val[0]][mut_val[1]][
                            mut_val[2]
                        ][mut_val[3]][mut_val[4]] = set_val
                    elif (
                        cmp_act == "<="
                        and self.unique_profiles[mut_val[0]][mut_val[1]][
                            mut_val[2]
                        ][mut_val[3]][mut_val[4]]
                        <= set_val
                    ):
                        self.unique_profiles[mut_val[0]][mut_val[1]][
                            mut_val[2]
                        ][mut_val[3]][mut_val[4]] = set_val
                    elif (
                        cmp_act == ">="
                        and self.unique_profiles[mut_val[0]][mut_val[1]][
                            mut_val[2]
                        ][mut_val[3]][mut_val[4]]
                        >= set_val
                    ):
                        self.unique_profiles[mut_val[0]][mut_val[1]][
                            mut_val[2]
                        ][mut_val[3]][mut_val[4]] = set_val

                # TODO: Debug
                # if entry.profile_id == 199325:
                #     pass

                self.unique_profiles[entry.profile_id]["country"] = (
                    pycountry.countries.get(alpha_2=entry.country_code)
                    if entry.country_code is not None
                    else None
                )

                self.unique_profiles[entry.profile_id]["hasSteamID"] = (
                    True if entry.steam_id is not None else False
                )

                self.unique_profiles[entry.profile_id]["hasRelicLinkID"] = (
                    True if entry.profile_id is not None else False
                )

                # TODO: what are the general ratios are of new players vs
                # leaving players vs long term players

                # Note: if someone is active on a leaderboard that person is
                # active in a game, if someone is inactive on a leaderboard
                # that person is not necessarily inactive for a game (as there
                # are other leaderboards) only being inactive on all
                # leaderboards, means inactive in a game

                # [ ] long-term players need some kind of `activity_streak`

                # First seen for each leaderboard
                _helper_set_value_if(
                    self,
                    (
                        entry.profile_id,
                        "activities",
                        game,
                        leaderboard,
                        "first_seen",
                    ),
                    entry.last_match,
                    datetime.datetime,
                    ">",
                )

                # Determine new leaderboard player
                self.unique_profiles[entry.profile_id]["activities"][game][
                    leaderboard
                ]["isNew"] = (
                    True
                    if (
                        datetime.datetime.now()
                        - self.unique_profiles[entry.profile_id]["activities"][
                            game
                        ][leaderboard]["first_seen"]
                    ).days
                    <= GLOBAL_SETTINGS["NEW_PLAYER_ACTIVITY_THRESHOLD"]
                    else False
                )

                # Last seen
                _helper_set_value_if(
                    self,
                    (
                        entry.profile_id,
                        "activities",
                        game,
                        leaderboard,
                        "last_seen",
                    ),
                    entry.last_match,
                    datetime.datetime,
                    "<",
                )

                # Determine (in-)active leaderboard player
                self.unique_profiles[entry.profile_id]["activities"][game][
                    leaderboard
                ]["isActive"] = (
                    True
                    if (
                        datetime.datetime.now()
                        - self.unique_profiles[entry.profile_id]["activities"][
                            game
                        ][leaderboard]["last_seen"]
                    ).days
                    <= GLOBAL_SETTINGS["LEAVING_PLAYER_ACTIVITY_THRESHOLD"]
                    else False
                )

                # Create activity bits
                if isinstance(
                    self.unique_profiles[entry.profile_id]["activities"][
                        "bits"
                    ],
                    defaultdict,
                ):
                    self.unique_profiles[entry.profile_id]["activities"][
                        "bits"
                    ] = 0b0

                base = self.unique_profiles[entry.profile_id]["activities"][
                    "bits"
                ]

                if (
                    self.unique_profiles[entry.profile_id]["activities"][game][
                        leaderboard
                    ]["isActive"]
                    is True
                ):
                    base = base | bit_mask
                else:
                    base = base & bit_mask

                self.unique_profiles[entry.profile_id]["activities"][
                    "bits"
                ] = base

                # Other properties
                # Highest Rank
                _helper_set_value_if(
                    self,
                    (
                        entry.profile_id,
                        "leaderboards",
                        game,
                        leaderboard,
                        "highest_rank",
                    ),
                    entry.rank,
                    int,
                )

                # Highest Rating
                _helper_set_value_if(
                    self,
                    (
                        entry.profile_id,
                        "leaderboards",
                        game,
                        leaderboard,
                        "highest_rating",
                    ),
                    entry.highest_rating,
                    int,
                )

                # Highest streak
                _helper_set_value_if(
                    self,
                    (
                        entry.profile_id,
                        "leaderboards",
                        game,
                        leaderboard,
                        "highest_streak",
                    ),
                    entry.streak,
                    int,
                )

                # Num games
                _helper_set_value_if(
                    self,
                    (
                        entry.profile_id,
                        "leaderboards",
                        game,
                        leaderboard,
                        "num_games",
                    ),
                    entry.num_games,
                    int,
                )

                # Num wins
                _helper_set_value_if(
                    self,
                    (
                        entry.profile_id,
                        "leaderboards",
                        game,
                        leaderboard,
                        "num_wins",
                    ),
                    entry.num_wins,
                    int,
                )

                # TODO: DEBUG
                # if entry.profile_id == 199325:
                #     print(self.unique_profiles[199325])

    def count_profiles_in_franchise(self):
        self.profile_stats["franchise"] = len(self.unique_profiles)
        self.dataset.export["analysed_profiles"]["franchise"] = len(
            self.unique_profiles
        )

    def count_profiles_per_game(self):
        unique_players = {
            "aoe2": 0,
            "aoe3": 0,
            "aoe4": 0,
        }

        for game in GLOBAL_SETTINGS["FRANCHISE_GAMES"]:
            for profile in self.unique_profiles.values():
                if game in profile:
                    if len(profile[game]) > 0:
                        unique_players[game] += 1

            self.profile_stats[game] = unique_players[game]
            self.dataset.export["analysed_profiles"][game] = unique_players[
                game
            ]

    def save_profile_stats(self):
        self.count_profiles_per_game()
        self.count_profiles_in_franchise()

    # def set_new_profile(self):
    #     profile["activities"][game][leaderboard]["isNew"]
    #     profile["activities"][game][leaderboard]["isActive"]

    # def set_activity_profile(self):

    #     profile["activities"][game][leaderboard]["isNew"]
    #     profile["activities"][game][leaderboard]["isActive"]

    def calculate_leaderboard_activity(self):
        for (
            game,
            leaderboard,
            _,
            _,
            _,
        ) in GLOBAL_SETTINGS["LEADERBOARD_SETTINGS"]:
            activity = defaultdict(dict)

            for profile in self.unique_profiles.values():
                if game in profile:
                    if leaderboard in profile[game]:
                        for activity_period in GLOBAL_SETTINGS[
                            "ACTIVITY_PERIODS"
                        ]:
                            if LeaderboardEntry.last_activity_from_date(
                                self.date,
                                profile[game][leaderboard],
                                activity_period,
                            ):
                                activity[activity_period] += 1

            for activity_period in GLOBAL_SETTINGS["ACTIVITY_PERIODS"]:
                self.dataset.export["leaderboard_activity"][
                    f"{activity_period}d"
                ][game][leaderboard] = activity[activity_period]

    def calculate_game_activity(self):

        for game in GLOBAL_SETTINGS["FRANCHISE_GAMES"]:

            activity_30d = 0
            activity_14d = 0
            activity_7d = 0
            activity_3d = 0
            activity_1d = 0

            for profile in self.unique_profiles.values():
                if game in profile:
                    max_date = max(
                        profile[game].items(), key=operator.itemgetter(1)
                    )[1]

                    if LeaderboardEntry.last_activity_from_date(
                        self.date, max_date, 30
                    ):
                        activity_30d += 1
                    if LeaderboardEntry.last_activity_from_date(
                        self.date, max_date, 14
                    ):
                        activity_14d += 1
                    if LeaderboardEntry.last_activity_from_date(
                        self.date, max_date, 7
                    ):
                        activity_7d += 1
                    if LeaderboardEntry.last_activity_from_date(
                        self.date, max_date, 3
                    ):
                        activity_3d += 1
                    if LeaderboardEntry.last_activity_from_date(
                        self.date, max_date, 1
                    ):
                        activity_1d += 1

            self.dataset.export["game_activity"]["30d"][game] = activity_30d
            self.dataset.export["game_activity"]["14d"][game] = activity_14d
            self.dataset.export["game_activity"]["7d"][game] = activity_7d
            self.dataset.export["game_activity"]["3d"][game] = activity_3d
            self.dataset.export["game_activity"]["1d"][game] = activity_1d

    def calculate_franchise_activity(self):
        activity_30d = 0
        activity_14d = 0
        activity_7d = 0
        activity_3d = 0
        activity_1d = 0

        for game in GLOBAL_SETTINGS["FRANCHISE_GAMES"]:
            for profile in self.unique_profiles.values():
                if game in profile:
                    max_date = max(
                        profile[game].items(), key=operator.itemgetter(1)
                    )[1]

                    if LeaderboardEntry.last_activity_from_date(
                        self.date, max_date, 30
                    ):
                        activity_30d += 1
                    if LeaderboardEntry.last_activity_from_date(
                        self.date, max_date, 14
                    ):
                        activity_14d += 1
                    if LeaderboardEntry.last_activity_from_date(
                        self.date, max_date, 7
                    ):
                        activity_7d += 1
                    if LeaderboardEntry.last_activity_from_date(
                        self.date, max_date, 3
                    ):
                        activity_3d += 1
                    if LeaderboardEntry.last_activity_from_date(
                        self.date, max_date, 1
                    ):
                        activity_1d += 1

        self.dataset.export["game_activity"]["30d"]["franchise"] = activity_30d
        self.dataset.export["game_activity"]["14d"]["franchise"] = activity_14d
        self.dataset.export["game_activity"]["7d"]["franchise"] = activity_7d
        self.dataset.export["game_activity"]["3d"]["franchise"] = activity_3d
        self.dataset.export["game_activity"]["1d"]["franchise"] = activity_1d

    def countries_per_game(self):

        for game in GLOBAL_SETTINGS["FRANCHISE_GAMES"]:

            countries = {}
            percentages = {}
            no_country = 0

            for profile in self.unique_profiles.values():
                if game in profile:
                    if profile["country"] is not None:
                        if profile["country"].alpha_2 in countries:
                            countries[profile["country"].alpha_2] += 1
                        else:
                            countries.update({profile["country"].alpha_2: 1})
                    else:
                        no_country += 1

            for country in countries.keys():
                percentages[country] = round(
                    countries[country] / self.profile_stats[game] * 100, 2
                )

            no_country = round(no_country / self.profile_stats[game] * 100, 2)

            top25 = dict(Counter(percentages).most_common(25))
            top25.update({"no_country_set": no_country})

            self.dataset.export["country"][game] = top25

    def countries_for_franchise(self):

        countries = {}
        percentages = {}
        no_country = 0

        for profile in self.unique_profiles.values():
            if profile["country"] is not None:
                if profile["country"].alpha_2 in countries:
                    countries[profile["country"].alpha_2] += 1
                else:
                    countries.update({profile["country"].alpha_2: 1})
            else:
                no_country += 1

        for country in countries.keys():
            percentages[country] = round(
                countries[country] / self.profile_stats["franchise"] * 100, 2
            )

        no_country = round(
            no_country / self.profile_stats["franchise"] * 100, 2
        )

        top25 = dict(Counter(percentages).most_common(25))
        top25.update({"no_country_set": no_country})

        self.dataset.export["country"]["franchise"] = top25

    def platforms_per_game(self):
        for game in GLOBAL_SETTINGS["FRANCHISE_GAMES"]:

            steam = 0
            relic = 0
            nothing = 0

            for profile in self.unique_profiles.values():
                if game in profile:
                    if (
                        profile["hasSteamID"] is True
                        and profile["hasRelicLinkID"] is False
                    ):
                        steam += 1
                    elif (
                        profile["hasSteamID"] is False
                        and profile["hasRelicLinkID"] is True
                    ):
                        relic += 1
                    elif (
                        profile["hasSteamID"] is True
                        and profile["hasRelicLinkID"] is True
                    ):
                        steam += 1
                    elif (
                        profile["hasSteamID"] is False
                        and profile["hasRelicLinkID"] is False
                    ):
                        nothing += 1

            steam = round(steam / self.profile_stats[game] * 100, 2)
            relic = round(relic / self.profile_stats[game] * 100, 2)
            nothing = round(nothing / self.profile_stats[game] * 100, 2)

            self.dataset.export["platforms"][game]["steam"] = steam
            self.dataset.export["platforms"][game]["relic"] = relic
            self.dataset.export["platforms"][game]["n/a"] = nothing

    def platforms_for_franchise(self):

        steam = 0
        relic = 0
        nothing = 0

        for profile in self.unique_profiles.values():
            if (
                profile["hasSteamID"] is True
                and profile["hasRelicLinkID"] is False
            ):
                steam += 1
            elif (
                profile["hasSteamID"] is False
                and profile["hasRelicLinkID"] is True
            ):
                relic += 1
            elif (
                profile["hasSteamID"] is True
                and profile["hasRelicLinkID"] is True
            ):
                steam += 1
            elif (
                profile["hasSteamID"] is False
                and profile["hasRelicLinkID"] is False
            ):
                nothing += 1

        steam = round(steam / self.profile_stats["franchise"] * 100, 2)
        relic = round(relic / self.profile_stats["franchise"] * 100, 2)
        nothing = round(nothing / self.profile_stats["franchise"] * 100, 2)

        self.dataset.export["platforms"]["franchise"]["steam"] = steam
        self.dataset.export["platforms"]["franchise"]["relic"] = relic
        self.dataset.export["platforms"]["franchise"]["n/a"] = nothing
