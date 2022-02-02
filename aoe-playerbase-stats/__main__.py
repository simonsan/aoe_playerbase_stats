"""
Command-line tool to collect, process, analyze and plot Age of Empires 2: DE,
Age of Empires 3: DE, and Age of Empires 4 leaderboard data
"""

import argparse
import sys
from data_collecting import main as fetch_data


def run(func, args=None):
    if args is None:
        return func()
    else:
        return func(args)


def main():
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

    if "," in args.stages:
        args.stages = args.stages.split(",")
        for stage in args.stages:
            if stage == "collect":
                print("We'll do it!")
                run(fetch_data)
            # DEBUG
            print(stage)
    else:
        if args.stages == "collect":
            run(fetch_data)

    sys.exit(0)


if __name__ == "__main__":
    sys.exit(main())
