class DataSet(object):
    def __init__(self):
        self.export = {
            "date": None,
            "activity": {
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
            "unique_players": {
                "aoe2": None,
                "aoe3": None,
                "aoe4": None,
                "franchise": None,
            },
        }

    def set_date(self, date):
        self.export["date"] = date.isoformat()
