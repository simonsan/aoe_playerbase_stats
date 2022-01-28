from common import leaderboard_settings, DATASET_FILE, FRANCHISE_GAMES
from util.leaderboard_entry import LeaderboardEntry
from util.dataset import DataSet
import datetime
import json
import operator
import pycountry
from collections import Counter


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

                # TODO: Debug
                # if entry.profile_id == 199325:
                #     pass

                if entry.profile_id not in self.unique_profiles:
                    self.unique_profiles.update(
                        {
                            entry.profile_id: {
                                game: {leaderboard: entry.last_match},
                            }
                        }
                    )
                elif game not in self.unique_profiles[entry.profile_id]:
                    self.unique_profiles[entry.profile_id].update(
                        {game: {leaderboard: entry.last_match}}
                    )
                elif (
                    leaderboard
                    not in self.unique_profiles[entry.profile_id][game]
                ):
                    self.unique_profiles[entry.profile_id][game].update(
                        {leaderboard: entry.last_match}
                    )

                if "country" not in self.unique_profiles[entry.profile_id]:
                    self.unique_profiles[entry.profile_id].update(
                        {
                            "country": pycountry.countries.get(
                                alpha_2=entry.country_code
                            )
                            if entry.country_code is not None
                            else None,
                        }
                    )

                if "hasSteamID" not in self.unique_profiles[entry.profile_id]:
                    self.unique_profiles[entry.profile_id].update(
                        {
                            "hasSteamID": True
                            if entry.steam_id is not None
                            else False,
                        }
                    )

                if (
                    "hasRelicLinkID"
                    not in self.unique_profiles[entry.profile_id]
                ):
                    self.unique_profiles[entry.profile_id].update(
                        {
                            "hasRelicLinkID": True
                            if entry.profile_id is not None
                            else False,
                        }
                    )

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

            top10 = dict(Counter(percentages).most_common(10))
            top10.update({"no_country_set": no_country})

            self.dataset.export["country"][game] = top10

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

        top10 = dict(Counter(percentages).most_common(10))
        top10.update({"no_country_set": no_country})

        self.dataset.export["country"]["franchise"] = top10

    def platforms_per_games(self):
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
