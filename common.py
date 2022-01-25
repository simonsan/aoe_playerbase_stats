from collections import namedtuple

DATA_FILE = "./data/leaderboard_data.json"

# Settings and descriptions for plotting
LeaderboardSetting = namedtuple(
    "LeaderboardSetting", "game leaderboard legend url"
)
leaderboard_settings = [
    LeaderboardSetting(
        "aoe2", "rm", "AoE2 RM", "https://aoe2.net/leaderboard/aoe2de/rm-1v1"
    ),
    LeaderboardSetting(
        "aoe2",
        "team_rm",
        "AoE2 Team-RM",
        "https://aoe2.net/leaderboard/aoe2de/rm-team",
    ),
    LeaderboardSetting(
        "aoe2", "ew", "AoE2 EW", "https://aoe2.net/leaderboard/aoe2de/ew-1v1"
    ),
    LeaderboardSetting(
        "aoe2",
        "team_ew",
        "AoE2 Team-EW",
        "https://aoe2.net/leaderboard/aoe2de/ew-team",
    ),
    LeaderboardSetting(
        "aoe2",
        "unranked",
        "AoE2 Unranked",
        "https://aoe2.net/leaderboard/aoe2de/unranked",
    ),
    LeaderboardSetting(
        "aoe4",
        "custom",
        "AoE4 Custom",
        "https://aoeiv.net/leaderboard/aoe4/custom",
    ),
    LeaderboardSetting(
        "aoe4",
        "qm_1v1",
        "AoE4 QM-1v1",
        "https://aoeiv.net/leaderboard/aoe4/qm-1v1",
    ),
    LeaderboardSetting(
        "aoe4",
        "qm_2v2",
        "AoE4 QM-2v2",
        "https://aoeiv.net/leaderboard/aoe4/qm-2v2",
    ),
    LeaderboardSetting(
        "aoe4",
        "qm_3v3",
        "AoE4 QM-3v3",
        "https://aoeiv.net/leaderboard/aoe4/qm-3v3",
    ),
    LeaderboardSetting(
        "aoe4",
        "qm_4v4",
        "AoE4 QM-4v4",
        "https://aoeiv.net/leaderboard/aoe4/qm-4v4",
    ),
]
