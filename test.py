import json

with open("./data/ew-1v1.json", encoding="utf8", mode="r") as handle:
    leaderboard_data = json.load(handle)

print(len(leaderboard_data["data"]))
