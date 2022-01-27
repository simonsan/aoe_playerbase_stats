import datetime


class LeaderboardEntry(object):
    def __init__(
        self,
        steam_id,
        profile_id,
        rank,
        rating,
        highest_rating,
        previous_rating,
        country_code,
        name,
        known_name,
        avatar,
        avatarfull,
        avatarmedium,
        num_games,
        streak,
        num_wins,
        win_percent,
        rating24h,
        games24h,
        wins24h,
        last_match,
    ):
        self.steam_id = steam_id
        self.profile_id = profile_id
        self.rank = rank
        self.rating = rating
        self.highest_rating = highest_rating
        self.previous_rating = previous_rating
        self.country_code = country_code
        self.name = name
        self.known_name = known_name
        self.avatar = avatar
        self.avatarfull = avatarfull
        self.avatarmedium = avatarmedium
        self.num_games = num_games
        self.streak = streak
        self.num_wins = num_wins
        self.win_percent = win_percent
        self.rating24h = rating24h
        self.games24h = games24h
        self.wins24h = wins24h
        self.last_match = datetime.datetime.fromtimestamp(last_match)

    def last_activity(self, data_date, max_days):
        pass

    def parse_leaderboard_entry(entry):
        pass
