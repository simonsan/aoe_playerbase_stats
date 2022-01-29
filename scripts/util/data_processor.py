import datetime
import hashlib
import json
import operator
import os
from collections import Counter, defaultdict

import pycountry
from common import (
    PROFILE_FILE,
    DATASET_FILE,
    FRANCHISE_GAMES,
    leaderboard_settings,
)

from util.dataset import DataSet
from util.leaderboard_entry import LeaderboardEntry

PEPPER = os.getenv("PEPPER_LEADERBOARD_DATA").encode()


class DataProcessor(object):
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
        self.unique_profiles = defaultdict(dict)

    def new_with_data(data):
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
        ) in leaderboard_settings:
            collector = defaultdict(list)
            for entry in data[game][leaderboard]:
                collector.append(
                    LeaderboardEntry(
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

    def append_to_dataset(self, file=DATASET_FILE):
        with open(file, "r") as handle:
            data = json.load(handle)

        data.append(self.dataset.export)

        with open(file, "w") as handle:
            json.dump(data, handle, indent=4)

    def export_dataset(self, file=DATASET_FILE):
        with open(file, "w") as handle:
            json.dump(self.dataset.export, handle, indent=4)

    def export_profiles(self, file=PROFILE_FILE):
        import pickle
        import lzma

        with lzma.open(file, mode="wb") as handle:
            pickle.dump(self.unique_profiles, handle)

    def import_profiles(self, file=PROFILE_FILE):
        import pickle
        import lzma

        with lzma.open(file, mode="rb") as handle:
            # We are aware of Pickle security implications
            self.unique_profiles = pickle.load(handle)  # nosec

    def create_unique_player_profiles(self):
        for (
            game,
            leaderboard,
            _,
            _,
        ) in leaderboard_settings:
            for entry in self.data[game][leaderboard]:

                # TODO: Debug
                # if entry.profile_id == 199325:
                #     pass

                self.unique_profiles[entry.profile_id][game][
                    leaderboard
                ] = entry.last_match

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
                # We can derive new players from first_seen
                # we can derive leaving players from last_seen
                # long-term players need some kind of `activity_streak`
                # something like

                if (
                    self.unique_profiles[entry.profile_id]["activity"][
                        "first_seen"
                    ]
                    is None
                ):
                    self.unique_profiles[entry.profile_id]["activity"][
                        "first_seen"
                    ] = self.date

                if (
                    self.unique_profiles[entry.profile_id]["activity"][
                        "last_seen"
                    ]
                    < entry.last_match
                ):
                    self.unique_profiles[entry.profile_id]["activity"][
                        "last_seen"
                    ] = entry.last_match

                if (
                    self.unique_profiles[entry.profile_id]["highest_rank"]
                    < entry.rank
                ):
                    self.unique_profiles[entry.profile_id][
                        "highest_rank"
                    ] = entry.rank

                if (
                    self.unique_profiles[entry.profile_id]["highest_rating"]
                    < entry.highest_rating
                ):
                    self.unique_profiles[entry.profile_id][
                        "highest_rating"
                    ] = entry.highest_rating

                if (
                    self.unique_profiles[entry.profile_id]["highest_streak"]
                    < entry.streak
                ):
                    self.unique_profiles[entry.profile_id][
                        "highest_streak"
                    ] = entry.streak

                if (
                    self.unique_profiles[entry.profile_id]["num_games"]
                    < entry.num_games
                ):
                    self.unique_profiles[entry.profile_id][
                        "num_games"
                    ] = entry.num_games

                if (
                    self.unique_profiles[entry.profile_id]["num_wins"]
                    < entry.num_wins
                ):
                    self.unique_profiles[entry.profile_id][
                        "num_wins"
                    ] = entry.num_wins

                # TODO: DEBUG
                # if entry.profile_id == 199325:
                #     print(self.unique_profiles[199325])

    def count_unique_profiles_in_franchise(self):
        self.profile_stats["franchise"] = len(self.unique_profiles)
        self.dataset.export["playerbase"]["franchise"] = len(
            self.unique_profiles
        )

    def count_unique_profiles_per_game(self):
        unique_players = {
            "aoe2": 0,
            "aoe3": 0,
            "aoe4": 0,
        }

        for game in FRANCHISE_GAMES:
            for profile in self.unique_profiles.values():
                if game in profile:
                    if len(profile[game]) > 0:
                        unique_players[game] += 1

            self.profile_stats[game] = unique_players[game]
            self.dataset.export["playerbase"][game] = unique_players[game]

    def save_profile_stats(self):
        self.count_unique_profiles_per_game()
        self.count_unique_profiles_in_franchise()

    def calculate_leaderboard_activity(self):
        for (
            game,
            leaderboard,
            _,
            _,
        ) in leaderboard_settings:
            activity_30d = 0
            activity_14d = 0
            activity_7d = 0
            activity_3d = 0
            activity_1d = 0

            for profile in self.unique_profiles.values():
                if game in profile:
                    if leaderboard in profile[game]:
                        if LeaderboardEntry.last_activity_from_date(
                            self.date, profile[game][leaderboard], 30
                        ):
                            activity_30d += 1
                        if LeaderboardEntry.last_activity_from_date(
                            self.date, profile[game][leaderboard], 14
                        ):
                            activity_14d += 1
                        if LeaderboardEntry.last_activity_from_date(
                            self.date, profile[game][leaderboard], 7
                        ):
                            activity_7d += 1
                        if LeaderboardEntry.last_activity_from_date(
                            self.date, profile[game][leaderboard], 3
                        ):
                            activity_3d += 1
                        if LeaderboardEntry.last_activity_from_date(
                            self.date, profile[game][leaderboard], 1
                        ):
                            activity_1d += 1

            self.dataset.export["leaderboard_activity"]["30d"][game][
                leaderboard
            ] = activity_30d
            self.dataset.export["leaderboard_activity"]["14d"][game][
                leaderboard
            ] = activity_14d
            self.dataset.export["leaderboard_activity"]["7d"][game][
                leaderboard
            ] = activity_7d
            self.dataset.export["leaderboard_activity"]["3d"][game][
                leaderboard
            ] = activity_3d
            self.dataset.export["leaderboard_activity"]["1d"][game][
                leaderboard
            ] = activity_1d

    def calculate_game_activity(self):

        for game in FRANCHISE_GAMES:

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

        for game in FRANCHISE_GAMES:
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

        for game in FRANCHISE_GAMES:

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
        for game in FRANCHISE_GAMES:

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
