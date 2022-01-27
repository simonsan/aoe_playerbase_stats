from common import leaderboard_settings
from util.leaderboard_entry import LeaderboardEntry
import datetime


class DataProcessor(object):
    def __init__(self):
        self.date = None
        self.data = {}

    def new_with_data(data):
        d = DataProcessor()
        d.date = datetime.date.fromisoformat(data["date"])
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
