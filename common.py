from collections import namedtuple

DATA_FILE = "./data/aoe-leaderboards.yaml"

# Settings and descriptions for plotting
LeaderboardSetting = namedtuple(
    "LeaderboardSetting", "game leaderboard legend url"
)
leaderboard_settings = [
    LeaderboardSetting(
        "aoe2", "rm", "AoE2 RM", "https://aoe2.net/#aoe2de-leaderboard-rm-1v1"
    ),
    LeaderboardSetting(
        "aoe2",
        "trm",
        "AoE2 Team-RM",
        "https://aoe2.net/#aoe2de-leaderboard-rm-team",
    ),
    LeaderboardSetting(
        "aoe2", "ew", "AoE2 EW", "https://aoe2.net/#aoe2de-leaderboard-ew-1v1"
    ),
    LeaderboardSetting(
        "aoe2",
        "tew",
        "AoE2 Team-EW",
        "https://aoe2.net/#aoe2de-leaderboard-ew-team",
    ),
    LeaderboardSetting(
        "aoe2",
        "ur",
        "AoE2 Unranked",
        "https://aoe2.net/#aoe2de-leaderboard-unranked",
    ),
    LeaderboardSetting(
        "aoe4",
        "cst",
        "AoE4 Custom",
        "https://aoeiv.net/#aoe4-leaderboard-custom",
    ),
    LeaderboardSetting(
        "aoe4",
        "1v1",
        "AoE4 QM-1v1",
        "https://aoeiv.net/#aoe4-leaderboard-qm-1v1",
    ),
    LeaderboardSetting(
        "aoe4",
        "2v2",
        "AoE4 QM-2v2",
        "https://aoeiv.net/#aoe4-leaderboard-qm-2v2",
    ),
    LeaderboardSetting(
        "aoe4",
        "3v3",
        "AoE4 QM-3v3",
        "https://aoeiv.net/#aoe4-leaderboard-qm-3v3",
    ),
    LeaderboardSetting(
        "aoe4",
        "4v4",
        "AoE4 QM-4v4",
        "https://aoeiv.net/#aoe4-leaderboard-qm-4v4",
    ),
]
