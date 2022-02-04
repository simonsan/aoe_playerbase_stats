import argparse
import re
import subprocess
from pathlib import Path

SRC_FOLDER = "aoe_playerbase_stat"
CURRENT_FOLDER = Path(__file__).resolve().parent


def ask_confirm(text):
    while True:
        answer = input(f"{text} [y/n]: ").lower()
        if answer in ("j", "y", "ja", "yes"):
            return True
        if answer in ("n", "no", "nein"):
            return False


def set_version(args):
    """
    - reads and validates version number
    - updates __version__.py
    - updates pyproject.toml
    """
    from aoe_playerbase_stat.__version__ import __version__ as current_version

    print(f"Current version is {current_version}.")

    # read version from input if not given
    version = args.version

    if not version:
        version = input("Version number: ")

    # validate and remove 'v' if present
    version = version.lower()
    if not re.match(r"v?\d+\.\d+.*", version):
        return
    if version.startswith("v"):
        version = version[1:]

    # safety check
    if not ask_confirm(f"Creating version v{version}. Continue?"):
        return

    # update library version
    versionfile = CURRENT_FOLDER / SRC_FOLDER / "__version__.py"
    with open(versionfile, "w") as f:
        print(f"Updating {versionfile}")
        f.write(f'__version__ = "{version}"\n')

    # update poetry version
    print("Updating pyproject.toml")
    subprocess.run(["poetry", "version", version], check=True)

    # if ask_confirm("Commit changes?"):
    #     subprocess.run(
    #         [
    #             "git",
    #             "add",
    #             "pyproject.toml",
    #             "*/__version__.py",
    #             "CHANGELOG.md",
    #         ]
    #     )
    #     subprocess.run((["git", "commit", "-m",
    #           f"bump version to v{version}"]))

    # print("Please push to github and wait for CI to pass.")
    print("Success.")


def main():
    assert CURRENT_FOLDER == Path.cwd().resolve()

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_version = subparsers.add_parser(
        "version", help="Set the version number"
    )
    parser_version.add_argument(
        "version", type=str, help="The version number", nargs="?", default=None
    )
    parser_version.set_defaults(func=set_version)

    args = parser.parse_args()
    if not vars(args):
        parser.print_help()
    else:
        args.func(args)


if __name__ == "__main__":
    main()
