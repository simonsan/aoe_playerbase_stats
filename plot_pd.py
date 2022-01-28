import pandas as pd
import json
from collections import namedtuple


from scripts.common import DATASET_FILE, leaderboard_settings

with open(DATASET_FILE, "r") as handle:
    dataset = json.load(handle)


periods = ["30d", "14d", "7d", "3d", "1d"]
platforms = ["steam", "relic", "n/a"]
games = ["aoe2", "aoe3", "aoe4", "franchise"]

# Index
index_activity = []
for game, leaderboard, _, _ in leaderboard_settings:
    index_activity.append((dataset[0]["date"], game, leaderboard))

index = pd.MultiIndex.from_tuples(
    index_activity,
    names=[
        "datetime",
        "games",
        "leaderboards",
    ],
)
df = pd.DataFrame(
    index=index,
)

# Only for game_activity
# index_activity.append(("franchise",))
for period in periods:
    data = []
    for game, leaderboard, _, _ in leaderboard_settings:
        data.append(
            dataset[0]["leaderboard_activity"][period][game][leaderboard]
        )

    df[period] = data


print(df)


# data_full = []
# columns = []


#     columns.append(period)
#     data_full.append(data)

# df = pd.Series(index=index, data=dataset[0]["leaderboard_activity"]["30d"])


"""



leaderboards = []


game activity
                30d   14d   7d    3d    1d
aoe2
aoe3
aoe4
franchise



"""
