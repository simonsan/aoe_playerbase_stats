from common import leaderboard_settings, DATASET_FILE, FRANCHISE_GAMES
from util.leaderboard_entry import LeaderboardEntry
from util.dataset import DataSet
import datetime
import json


class DataProcessor(object):
    def __init__(self):
        self.date = None
        self.data = {}
        self.dataset = DataSet()
        self.unique_profiles = {}

    def new_with_data(data):
        d = DataProcessor()
        d.date = datetime.date.fromisoformat(data["date"])
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
            collector = []
            for entry in data[game][leaderboard]:
                collector.append(
                    LeaderboardEntry(
                        steam_id=entry["steam_id"],
                        profile_id=entry["profile_id"],
                        rank=entry["rank"],
                        rating=entry["rating"],
                        highest_rating=entry["highest_rating"],
                        previous_rating=entry["previous_rating"],
                        country_code=entry["country_code"],
                        name=entry["name"],
                        known_name=entry["known_name"],
                        avatar=entry["avatar"],
                        avatarfull=entry["avatarfull"],
                        avatarmedium=entry["avatarmedium"],
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

    def export_dataset(self, file=DATASET_FILE):
        with open(file, "w") as handle:
            json.dump(self.dataset.export, handle, indent=4)

    def create_unique_player_profiles(self):
        for (
            game,
            leaderboard,
            _,
            _,
        ) in leaderboard_settings:
            for entry in self.data[game][leaderboard]:
                try:
                    self.unique_profiles[entry.profile_id][game][
                        leaderboard
                    ] = entry.last_match
                except (KeyError):
                    try:
                        if isinstance(
                            self.unique_profiles[entry.profile_id],
                            dict,
                        ):
                            self.unique_profiles[entry.profile_id].update(
                                {game: {leaderboard: entry.last_match}}
                            )
                    except (KeyError):
                        self.unique_profiles[entry.profile_id] = {}
                        self.unique_profiles[entry.profile_id][game] = {
                            leaderboard: entry.last_match
                        }

    def count_unique_profiles_in_franchise(self):
        self.dataset.export["unique_players"]["franchise"] = len(
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

            self.dataset.export["unique_players"][game] = unique_players[game]

    def calculate_activity_profiles_per_leaderboard(self):
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

            self.dataset.export["activity"]["30d"][game][
                leaderboard
            ] = activity_30d
            self.dataset.export["activity"]["14d"][game][
                leaderboard
            ] = activity_14d
            self.dataset.export["activity"]["7d"][game][
                leaderboard
            ] = activity_7d
            self.dataset.export["activity"]["3d"][game][
                leaderboard
            ] = activity_3d
            self.dataset.export["activity"]["1d"][game][
                leaderboard
            ] = activity_1d

    def calculate_activity_profiles_per_game(self):
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

            self.dataset.export["activity"]["30d"][game][
                leaderboard
            ] = activity_30d
            self.dataset.export["activity"]["14d"][game][
                leaderboard
            ] = activity_14d
            self.dataset.export["activity"]["7d"][game][
                leaderboard
            ] = activity_7d
            self.dataset.export["activity"]["3d"][game][
                leaderboard
            ] = activity_3d
            self.dataset.export["activity"]["1d"][game][
                leaderboard
            ] = activity_1d

    def calculate_activity_profiles_in_franchise(self):
        activity_30d = 0
        activity_14d = 0
        activity_7d = 0
        activity_3d = 0
        activity_1d = 0

        for (
            game,
            leaderboard,
            _,
            _,
        ) in leaderboard_settings:

            for entry in self.data[game][leaderboard]:
                if entry.last_activity(self.date, 30):
                    activity_30d += 1
                if entry.last_activity(self.date, 14):
                    activity_14d += 1
                if entry.last_activity(self.date, 7):
                    activity_7d += 1
                if entry.last_activity(self.date, 3):
                    activity_3d += 1
                if entry.last_activity(self.date, 1):
                    activity_1d += 1

        self.dataset.export["activity"]["30d"]["franchise"] = activity_30d
        self.dataset.export["activity"]["14d"]["franchise"] = activity_14d
        self.dataset.export["activity"]["7d"]["franchise"] = activity_7d
        self.dataset.export["activity"]["3d"]["franchise"] = activity_3d
        self.dataset.export["activity"]["1d"]["franchise"] = activity_1d

    def countries_per_leaderboard(self):
        # languages = {}

        # for (
        #     game,
        #     leaderboard,
        #     _,
        #     _,
        # ) in leaderboard_settings:

        #     for entry in self.data[game][leaderboard]:
        #         unique_players[game][entry.profile_id] = True

        #     self.dataset.export["unique_players"][game] = len(
        #         unique_players[game]
        #     )
        pass
