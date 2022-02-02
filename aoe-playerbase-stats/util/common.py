# flake8: noqa: E501

import datetime
import glob
import logging
from collections import namedtuple

LOGGER = logging.getLogger(__name__)

CURRENT_DATE = datetime.date.isoformat(datetime.date.today())
DATA_SET_TIMESTAMP = None
DF_OUT = None

__DATA_FOLDER = f"{__package__}/data/"
__WEB_FOLDER = "./web/"
__TEMPORARY_DATA_FOLDER = f"{__package__}/data_temp/"

LeaderboardSetting = namedtuple(
    "LeaderboardSetting", "game leaderboard legend url bit_mask"
)

# Template: GLOBAL_SETTINGS['FILESYSTEM']['TEMPORARY_CACHE_FOLDER']
GLOBAL_SETTINGS = {
    "ARGUMENTS": {None},
    "FILESYSTEM": {
        "DATA_FOLDER": __DATA_FOLDER,
        "WEB_FOLDER": __WEB_FOLDER,
        "TEMPORARY_DATA_FOLDER": __TEMPORARY_DATA_FOLDER,
        "TEMPORARY_CACHE_FOLDER": f"{__TEMPORARY_DATA_FOLDER}cache/",  # previously: CACHE_PATH, CACHE_FOLDER
        "ARCHIVED_CACHE_FOLDER": f"{__TEMPORARY_DATA_FOLDER}cache/archive/",
        "DATASET_FILE_PATH": f"{__DATA_FOLDER}dataset.json",
        "AOC_REF_DATA_FILE_PATH": f"{__TEMPORARY_DATA_FOLDER}aoc_ref_data.json",
        "PARQUET_FILE_PATH": f"{__DATA_FOLDER}dataframe.br.parq",
        "PLOT_OUTPUT_FILE_PATH": f"{__WEB_FOLDER}index.html",  # previously: PLOT_OUTPUT
    },
    "VARIABLES": {
        "KNOWN_STAGES": ["collect", "process", "analyse", "plot"],
        "ACTIVITY_PERIODS": [30, 14, 7, 3, 1],
        "GAMES": ["aoe2", "aoe3", "aoe4"],
        # 26 because we don't drop None in values_count(), so it's Top25 + Amount of not set
        "TOP_COUNTRIES": 26,
        "NEW_PLAYER_ACTIVITY_THRESHOLD": 30,
        "LEAVING_PLAYER_ACTIVITY_THRESHOLD": 90,
        "AOC_REF_DATA_URL": (
            "https://raw.githubusercontent.com/SiegeEngineers/"
            "aoc-reference-data/master/data/auto_generated/players.json"
        ),
        "LEADERBOARD_SETTINGS": [
            LeaderboardSetting(
                "aoe2",
                "rm",
                "AoE2:DE RM",
                "https://aoe2.net/leaderboard/aoe2de/rm-1v1?draw=1&columns[0][data]=&columns[0][name]=&columns[0][searchable]=false&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=&columns[1][name]=&columns[1][searchable]=false&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=&columns[3][name]=&columns[3][searchable]=false&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=&columns[4][name]=&columns[4][searchable]=false&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=&columns[5][name]=&columns[5][searchable]=false&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=&columns[6][name]=&columns[6][searchable]=false&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=&columns[7][name]=&columns[7][searchable]=false&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&order[0][column]=0&order[0][dir]=asc&search[value]=&search[regex]=false",
                0b1,
            ),
            LeaderboardSetting(
                "aoe2",
                "team_rm",
                "AoE2:DE Team-RM",
                "https://aoe2.net/leaderboard/aoe2de/rm-team?draw=2&columns[0][data]=&columns[0][name]=&columns[0][searchable]=false&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=&columns[1][name]=&columns[1][searchable]=false&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=&columns[3][name]=&columns[3][searchable]=false&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=&columns[4][name]=&columns[4][searchable]=false&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=&columns[5][name]=&columns[5][searchable]=false&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=&columns[6][name]=&columns[6][searchable]=false&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=&columns[7][name]=&columns[7][searchable]=false&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&order[0][column]=0&order[0][dir]=asc&search[value]=&search[regex]=false",
                0b10,
            ),
            LeaderboardSetting(
                "aoe2",
                "ew",
                "AoE2:DE EW",
                "https://aoe2.net/leaderboard/aoe2de/ew-1v1?draw=4&columns[0][data]=&columns[0][name]=&columns[0][searchable]=false&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=&columns[1][name]=&columns[1][searchable]=false&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=&columns[3][name]=&columns[3][searchable]=false&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=&columns[4][name]=&columns[4][searchable]=false&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=&columns[5][name]=&columns[5][searchable]=false&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=&columns[6][name]=&columns[6][searchable]=false&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=&columns[7][name]=&columns[7][searchable]=false&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&order[0][column]=0&order[0][dir]=asc&search[value]=&search[regex]=false",
                0b100,
            ),
            LeaderboardSetting(
                "aoe2",
                "team_ew",
                "AoE2:DE Team-EW",
                "https://aoe2.net/leaderboard/aoe2de/ew-team?draw=3&columns[0][data]=&columns[0][name]=&columns[0][searchable]=false&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=&columns[1][name]=&columns[1][searchable]=false&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=&columns[3][name]=&columns[3][searchable]=false&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=&columns[4][name]=&columns[4][searchable]=false&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=&columns[5][name]=&columns[5][searchable]=false&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=&columns[6][name]=&columns[6][searchable]=false&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=&columns[7][name]=&columns[7][searchable]=false&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&order[0][column]=0&order[0][dir]=asc&search[value]=&search[regex]=false",
                0b1000,
            ),
            LeaderboardSetting(
                "aoe2",
                "unranked",
                "AoE2:DE Unranked",
                "https://aoe2.net/leaderboard/aoe2de/unranked?draw=5&columns[0][data]=&columns[0][name]=&columns[0][searchable]=false&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=&columns[1][name]=&columns[1][searchable]=false&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=&columns[3][name]=&columns[3][searchable]=false&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=&columns[4][name]=&columns[4][searchable]=false&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=&columns[5][name]=&columns[5][searchable]=false&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=&columns[6][name]=&columns[6][searchable]=false&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=&columns[7][name]=&columns[7][searchable]=false&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&order[0][column]=0&order[0][dir]=asc&search[value]=&search[regex]=false",
                0b10000,
            ),
            LeaderboardSetting(
                "aoe3",
                "supremacy_1v1",
                "AoE3:DE Supremacy 1v1",
                "https://aoe3.net/leaderboard/aoe3de/supremacy-1v1?draw=1&columns[0][data]=&columns[0][name]=&columns[0][searchable]=false&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=&columns[1][name]=&columns[1][searchable]=false&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=&columns[3][name]=&columns[3][searchable]=false&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=&columns[4][name]=&columns[4][searchable]=false&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=&columns[5][name]=&columns[5][searchable]=false&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=&columns[6][name]=&columns[6][searchable]=false&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=&columns[7][name]=&columns[7][searchable]=false&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&order[0][column]=0&order[0][dir]=asc&search[value]=&search[regex]=false",
                0b100000,
            ),
            LeaderboardSetting(
                "aoe3",
                "supremacy_team",
                "AoE3:DE Supremacy Team",
                "https://aoe3.net/leaderboard/aoe3de/supremacy-team?draw=2&columns[0][data]=&columns[0][name]=&columns[0][searchable]=false&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=&columns[1][name]=&columns[1][searchable]=false&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=&columns[3][name]=&columns[3][searchable]=false&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=&columns[4][name]=&columns[4][searchable]=false&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=&columns[5][name]=&columns[5][searchable]=false&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=&columns[6][name]=&columns[6][searchable]=false&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=&columns[7][name]=&columns[7][searchable]=false&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&order[0][column]=0&order[0][dir]=asc&search[value]=&search[regex]=false",
                0b1000000,
            ),
            LeaderboardSetting(
                "aoe3",
                "treaty",
                "AoE3:DE Treaty",
                "https://aoe3.net/leaderboard/aoe3de/treaty?draw=3&columns[0][data]=&columns[0][name]=&columns[0][searchable]=false&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=&columns[1][name]=&columns[1][searchable]=false&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=&columns[3][name]=&columns[3][searchable]=false&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=&columns[4][name]=&columns[4][searchable]=false&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=&columns[5][name]=&columns[5][searchable]=false&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=&columns[6][name]=&columns[6][searchable]=false&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=&columns[7][name]=&columns[7][searchable]=false&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&order[0][column]=0&order[0][dir]=asc&search[value]=&search[regex]=false",
                0b10000000,
            ),
            LeaderboardSetting(
                "aoe3",
                "deathmatch",
                "AoE3:DE Deathmatch",
                "https://aoe3.net/leaderboard/aoe3de/deathmatch?draw=4&columns[0][data]=&columns[0][name]=&columns[0][searchable]=false&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=&columns[1][name]=&columns[1][searchable]=false&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=&columns[3][name]=&columns[3][searchable]=false&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=&columns[4][name]=&columns[4][searchable]=false&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=&columns[5][name]=&columns[5][searchable]=false&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=&columns[6][name]=&columns[6][searchable]=false&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=&columns[7][name]=&columns[7][searchable]=false&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&order[0][column]=0&order[0][dir]=asc&search[value]=&search[regex]=false",
                0b100000000,
            ),
            LeaderboardSetting(
                "aoe4",
                "custom",
                "AoE4 Custom",
                "https://aoeiv.net/leaderboard/aoe4/custom?draw=2&columns[0][data]=&columns[0][name]=&columns[0][searchable]=false&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=&columns[1][name]=&columns[1][searchable]=false&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=&columns[3][name]=&columns[3][searchable]=false&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=&columns[4][name]=&columns[4][searchable]=false&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=&columns[5][name]=&columns[5][searchable]=false&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=&columns[6][name]=&columns[6][searchable]=false&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=&columns[7][name]=&columns[7][searchable]=false&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&order[0][column]=0&order[0][dir]=asc&search[value]=&search[regex]=false",
                0b1000000000,
            ),
            LeaderboardSetting(
                "aoe4",
                "qm_1v1",
                "AoE4 QM-1v1",
                "https://aoeiv.net/leaderboard/aoe4/qm-1v1?draw=1&columns[0][data]=&columns[0][name]=&columns[0][searchable]=false&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=&columns[1][name]=&columns[1][searchable]=false&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=&columns[3][name]=&columns[3][searchable]=false&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=&columns[4][name]=&columns[4][searchable]=false&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=&columns[5][name]=&columns[5][searchable]=false&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=&columns[6][name]=&columns[6][searchable]=false&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=&columns[7][name]=&columns[7][searchable]=false&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&order[0][column]=0&order[0][dir]=asc&search[value]=&search[regex]=false",
                0b10000000000,
            ),
            LeaderboardSetting(
                "aoe4",
                "qm_2v2",
                "AoE4 QM-2v2",
                "https://aoeiv.net/leaderboard/aoe4/qm-2v2?draw=3&columns[0][data]=&columns[0][name]=&columns[0][searchable]=false&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=&columns[1][name]=&columns[1][searchable]=false&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=&columns[3][name]=&columns[3][searchable]=false&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=&columns[4][name]=&columns[4][searchable]=false&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=&columns[5][name]=&columns[5][searchable]=false&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=&columns[6][name]=&columns[6][searchable]=false&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=&columns[7][name]=&columns[7][searchable]=false&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&order[0][column]=0&order[0][dir]=asc&search[value]=&search[regex]=false",
                0b100000000000,
            ),
            LeaderboardSetting(
                "aoe4",
                "qm_3v3",
                "AoE4 QM-3v3",
                "https://aoeiv.net/leaderboard/aoe4/qm-3v3?draw=4&columns[0][data]=&columns[0][name]=&columns[0][searchable]=false&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=&columns[1][name]=&columns[1][searchable]=false&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=&columns[3][name]=&columns[3][searchable]=false&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=&columns[4][name]=&columns[4][searchable]=false&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=&columns[5][name]=&columns[5][searchable]=false&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=&columns[6][name]=&columns[6][searchable]=false&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=&columns[7][name]=&columns[7][searchable]=false&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&order[0][column]=0&order[0][dir]=asc&search[value]=&search[regex]=false",
                0b1000000000000,
            ),
            LeaderboardSetting(
                "aoe4",
                "qm_4v4",
                "AoE4 QM-4v4",
                "https://aoeiv.net/leaderboard/aoe4/qm-4v4?draw=5&columns[0][data]=&columns[0][name]=&columns[0][searchable]=false&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=&columns[1][name]=&columns[1][searchable]=false&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=&columns[3][name]=&columns[3][searchable]=false&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=&columns[4][name]=&columns[4][searchable]=false&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=&columns[5][name]=&columns[5][searchable]=false&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=&columns[6][name]=&columns[6][searchable]=false&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=&columns[7][name]=&columns[7][searchable]=false&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&order[0][column]=0&order[0][dir]=asc&search[value]=&search[regex]=false",
                0b10000000000000,
            ),
        ],
    },
}

CACHE_FILES = glob.glob(
    f"{GLOBAL_SETTINGS['FILESYSTEM']['TEMPORARY_CACHE_FOLDER']}cache_*"
)
