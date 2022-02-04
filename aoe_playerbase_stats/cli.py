"""
aoe_playerbase_stats -- A Command-line tool to collect, process, analyze and
 plot Age of Empires 2: DE, Age of Empires 3: DE, and Age of Empires 4
 leaderboard data

Usage:
  aoe_playerbase_stats [stages <stages>...] [--data-file=<PATH>] [-y] [--verbose]
  aoe_playerbase_stats (-h | --help)
  aoe_playerbase_stats --version

Arguments:
  stages            Runs a specific stage [all, collect, process, analyse, plot]
                    Default: all
  -v, --version     Show version
  -h --help         Show this screen

Options:
  -y                Do things normal users can't. E.g plotting without running
                    other stages beforehand.
  --verbose         Increase verbosity
  -d, --d           Run in debug mode
"""


import sys
import logging

from docopt import docopt  # type: ignore

# from schema import Schema, And, Or, Use, SchemaError

from .__version__ import __version__
from aoe_playerbase_stats.commons.settings import GLOBAL_SETTINGS

# These are not found because we call them dynamically with
# globals()[func]()
from aoe_playerbase_stats.stages.data_collecting import (
    data_collecting as collect,
)

from aoe_playerbase_stats.stages.data_processing import (
    data_processing as process,
)

# from aoe_playerbase_stats.stages.data_analysing import (
#     data_analysing as analyse,
# )
# from aoe_playerbase_stats.stages.plotting import plotting as plot
from aoe_playerbase_stats.utils.error import raise_error


def main(argv=None):
    """entry point for the command line interface"""

    args = docopt(
        __doc__, argv=argv, version=__package__ + " v" + __version__, help=True
    )

    # TODO: Schema validation
    # schema = Schema(
    #     {
    #         "--data-file": [
    #             None,
    #             Use(open, error="Data file should be readable"),
    #         ],
    #         "PATH": And(os.path.exists, error="PATH should exist"),
    #     }
    # )
    # try:
    #     args = schema.validate(args)
    # except SchemaError as e:
    #     exit(e)

    if args["--verbose"]:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if args["stages"]:
        if not args["<stages>"]:
            # Defaults to all stages if no stage is given
            filtered_stages = GLOBAL_SETTINGS["VARIABLES"]["KNOWN_STAGES"]
        elif "all" in args["<stages>"]:
            filtered_stages = GLOBAL_SETTINGS["VARIABLES"]["KNOWN_STAGES"]
        else:
            filtered_stages = [
                stage
                for stage in GLOBAL_SETTINGS["VARIABLES"]["KNOWN_STAGES"]
                if stage in args["<stages>"]
            ]
    else:
        filtered_stages = GLOBAL_SETTINGS["VARIABLES"]["KNOWN_STAGES"]

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
        and not args["-y"]
    ):
        raise_error(
            "Can't create a plot without processing and analysing stage. "
            "Please reevaluate your input or append `-y` for `yes` "
            "so we know that you know what you are doing."
        )

    for stage in filtered_stages:
        # TODO: DEBUG
        if stage in ["collect", "process", "plot"]:
            print(f"Ignored stage {stage}!")
        else:
            globals()[stage]()

    # TODO: DEBUG
    print(args)
    print(filtered_stages)

    sys.exit(0)
