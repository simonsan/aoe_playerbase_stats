"""
aoe_player_stat - A Command-line tool to collect, process, analyze and
 plot Age of Empires 2: DE, Age of Empires 3: DE, and Age of Empires 4
 leaderboard data


"""


import argparse
import sys

from aoe_playerbase_stats.stages.data_collecting import (
    data_collecting as collect,
)
from aoe_playerbase_stats.commons.settings import GLOBAL_SETTINGS
from aoe_playerbase_stats.utils.error import raise_error

# from .data_processing import data_processing as process
# from .data_analysing import data_analysing as analyse
# from .plotting import plotting as plot


def run(func, args=None):
    if args is None:
        return func()
    else:
        return func(args)


def main(argv=None):
    cli = argparse.ArgumentParser(
        "aoe-playerbase-stats",
        description=(
            "Command-line tool to collect, process, analyze and plot Age of"
            " Empires 2: DE, Age of Empires 3: DE, and Age of Empires 4"
            " leaderboard data"
        ),
    )
    verbosity = cli.add_mutually_exclusive_group()
    verbosity.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        default=False,
        help="increase verbosity",
    )
    verbosity.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        default=False,
        help="decrease verbosity",
    )

    cli.add_argument(
        "-y",
        dest="no_order",
        action="store_true",
        default=False,
        help="Do things normal users can't. E.g plotting without "
        "running other stages beforehand.",
    )

    cli.add_argument(
        "--stage",
        "-s",
        action="store",
        dest="stages",
        help=(
            "Run a specific stage.  Default: 'all'."
            "Possible values: ['all', 'collect', 'process', "
            "'analyse', 'plot']. You can also mix them, e.g. 'collect,"
            "process' (no whitespace)"
        ),
        default="all",
        required=False,
    )

    cli.add_argument(
        "--datafile-path",
        "-d",
        dest="datafile_path",
        help="Use another datafile than ours",
        action="store",
    )

    args = cli.parse_args()

    # TODO: Actually do something
    if args.verbose:
        pass
    if args.quiet:
        pass

    split = args.stages.split(",")
    if "all" in split:
        filtered_stages = GLOBAL_SETTINGS["VARIABLES"]["KNOWN_STAGES"]
    else:
        filtered_stages = [
            stage
            for stage in GLOBAL_SETTINGS["VARIABLES"]["KNOWN_STAGES"]
            if stage in split
        ]

    # TODO: What about other stages. Run "analyse without process and collect?"
    # We need a function here that checks for the presence of a file in a file
    # path for the different stages we can have a namedtuple that give the
    # settings for different stages
    # `Analyse stage` with existing parquet file should be fine
    # `Plot stage` with existing parquet file should be fine
    # `Process stage` without files in GLOBAL_SETTINGS['FILESYSTEM']
    # ['TEMPORARY_CACHE_FOLDER'] should not work and give a warning to run
    # `collect stage`
    # `Collect stage` should throw warning early if filesystem is not setup
    # for saving the files so we should just check if we can create the files
    # or we should actually try to create tempfiles for this stage
    if (
        "plot" in filtered_stages
        and (
            "process" not in filtered_stages
            or "analyse" not in filtered_stages
        )
        and not args.no_order
    ):
        raise_error(
            "Can't create a plot without processing and analysing stage. "
            "Please reevaluate your input or append `-y` for `yes` "
            "so we know that you know what you are doing."
        )

    for stage in filtered_stages:
        print(stage)
        # run(stage)
        collect()
    sys.exit(0)
