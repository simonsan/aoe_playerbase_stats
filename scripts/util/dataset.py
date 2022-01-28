class DataSet(object):
    def __init__(self):
        self.export = {
            "date": None,
            "leaderboard_activity": {
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
            "language": {
                "aoe2": {},
                "aoe3": {},
                "aoe4": {},
                "franchise": {},
            },
        }

    def set_date(self, date):
        self.export["date"] = date.isoformat()
