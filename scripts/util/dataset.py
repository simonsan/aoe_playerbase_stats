class DataSet(object):
    def __init__(self):
        self.export = {
            "date": None,
            "leaderboard_activity": {
                "30d": {
                    "aoe2": {},
                    "aoe3": {},
                    "aoe4": {},
                },
                "14d": {
                    "aoe2": {},
                    "aoe3": {},
                    "aoe4": {},
                },
                "7d": {
                    "aoe2": {},
                    "aoe3": {},
                    "aoe4": {},
                },
                "3d": {
                    "aoe2": {},
                    "aoe3": {},
                    "aoe4": {},
                },
                "1d": {
                    "aoe2": {},
                    "aoe3": {},
                    "aoe4": {},
                },
            },
            "game_activity": {
                "30d": {
                    "aoe2": {},
                    "aoe3": {},
                    "aoe4": {},
                    "franchise": {},
                },
                "14d": {
                    "aoe2": {},
                    "aoe3": {},
                    "aoe4": {},
                    "franchise": {},
                },
                "7d": {
                    "aoe2": {},
                    "aoe3": {},
                    "aoe4": {},
                    "franchise": {},
                },
                "3d": {
                    "aoe2": {},
                    "aoe3": {},
                    "aoe4": {},
                    "franchise": {},
                },
                "1d": {
                    "aoe2": {},
                    "aoe3": {},
                    "aoe4": {},
                    "franchise": {},
                },
            },
            "playerbase": {
                "aoe2": None,
                "aoe3": None,
                "aoe4": None,
                "franchise": None,
            },
            "platforms": {
                "aoe2": {
                    "steam": None,
                    "relic": None,
                },
                "aoe3": {
                    "steam": None,
                    "relic": None,
                },
                "aoe4": {
                    "steam": None,
                    "relic": None,
                },
                "franchise": {
                    "steam": None,
                    "relic": None,
                },
            },
            "country": {
                "aoe2": {},
                "aoe3": {},
                "aoe4": {},
                "franchise": {},
            },
        }

    def set_date(self, date):
        self.export["date"] = date.isoformat()
