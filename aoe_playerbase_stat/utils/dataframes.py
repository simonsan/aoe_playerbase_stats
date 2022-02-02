# import datetime
# import json

# import pandas as pd

# from ..settings import GLOBAL_SETTINGS


# def prepare_dataframes():
#     with open(DATASET_FILE, "r") as handle:
#         datasets = json.load(handle)

#     df_activity = pd.DataFrame()
#     df_playerbase = pd.DataFrame()
#     df_platforms = pd.DataFrame()
#     df_country = pd.DataFrame()

#     for dataset in datasets:

#         data_activity = {}
#         data_playerbase = {}
#         data_platforms = {}
#         data_country = {}

#         timestamp = datetime.datetime.fromisoformat(dataset["date"])

#         data_activity["timestamp"] = pd.Timestamp(timestamp)
#         data_playerbase["timestamp"] = pd.Timestamp(timestamp)
#         data_platforms["timestamp"] = pd.Timestamp(timestamp)
#         data_country["timestamp"] = pd.Timestamp(timestamp)

#         for period in ACTIVITY_PERIODS:
#             for game, leaderboard, _, _ in leaderboard_settings:
#                 data_activity[
#                     f"leaderboard_activity_{period}_{game}_{leaderboard}"
#                 ] = dataset["leaderboard_activity"][period][game][leaderboard]
#                 data_activity[f"game_activity_{period}_{game}"] = dataset[
#                     "game_activity"
#                 ][period][game]

#         for game in dataset["playerbase"]:
#             data_playerbase[f"playerbase_{game}"] = dataset["playerbase"][game]

#         for game in dataset["platforms"]:
#             for platform in dataset["platforms"][game]:
#                 data_platforms[f"playerbase_{game}_{platform}"] = dataset[
#                     "platforms"
#                 ][game][platform]

#         for game in dataset["country"]:
#             for lang in dataset["country"][game]:
#                 data_country[f"country_{game}_{lang}"] = dataset["country"][
#                     game
#                 ][lang]

#         new_activity = pd.DataFrame([data_activity])
#         new_playerbase = pd.DataFrame([data_playerbase])
#         new_platforms = pd.DataFrame([data_platforms])
#         new_country = pd.DataFrame([data_country])

#         df_activity = pd.concat([df_activity, new_activity])
#         df_playerbase = pd.concat([df_playerbase, new_playerbase])
#         df_platforms = pd.concat([df_platforms, new_platforms])
#         df_country = pd.concat([df_country, new_country])

#     # DEBUG
#     # print(df_activity)
#     # print(df_playerbase)
#     # print(df_platforms)
#     # print(df_country)

#     return (df_activity, df_playerbase, df_platforms, df_country)


# (
#     _,
#     _,
#     _,
#     _,
# ) = prepare_dataframes()
