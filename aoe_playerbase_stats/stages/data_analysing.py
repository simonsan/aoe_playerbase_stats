# Intern
import logging

from ..commons.settings import GLOBAL_SETTINGS
from ..utils.data_analyser import DataAnalyser

DEBUG = True
WRITE = False


def data_analysing():
    # Set Debug logging if necessary
    if DEBUG:
        logging.basicConfig(level=logging.DEBUG)
    elif not DEBUG:
        logging.basicConfig(level=logging.INFO)

    # Initialise the analyser
    data_analyser = DataAnalyser.new_with_parquet_file()

    data_analyser.create_leaderboard_player_count()

    # Does all that juicy work.
    # data_analyser.create_player_profiles()

    # Utility
    # data_analyser.save_profile_stats()

    # Statistics
    # data_analyser.calculate_leaderboard_activity()
    # data_analyser.calculate_game_activity()
    # data_analyser.calculate_franchise_activity()
    # data_analyser.countries_per_game()
    # data_analyser.countries_for_franchise()
    # data_analyser.platforms_per_game()
    # data_analyser.platforms_for_franchise()

    # EXPORT EXTERNAL DATASET
    # Append to old dataset
    # if WRITE:
    #     data_analyser.append_to_dataset()


if __name__ == "__main__":
    data_analysing()
