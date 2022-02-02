# Intern
import logging
import lzma
import os
import pickle
import pkgutil
import shutil
import sys

from .settings import GLOBAL_SETTINGS, LOGGER, CACHE_FILES
from utils.data_processor import DataProcessor
from utils.error import raise_error

DEBUG = True
WRITE = False


def data_processing():

    # Set Debug logging if necessary
    if DEBUG:
        logging.basicConfig(level=logging.DEBUG)
    elif not DEBUG:
        logging.basicConfig(level=logging.INFO)

    cache_file_count = 0
    overall_number_of_cache_files = len(CACHE_FILES)

    # TODO: Pass data file
    data_file = pkgutil.get_data(
        __package__, GLOBAL_SETTINGS["FILESYSTEM"]["PARQUET_FILE_PATH"]
    )

    for cache_file in CACHE_FILES:

        cache_file_count += 1

        LOGGER.info(
            f"Processing cache file ({cache_file_count}/"
            f"{overall_number_of_cache_files}): {cache_file}. Please wait ..."
        )

        # Import data
        try:
            if os.path.exists(cache_file):
                with lzma.open(cache_file, mode="rb") as handle:
                    # We are aware of Pickle security implications
                    cache_data = pickle.load(handle)  # nosec
        except (FileNotFoundError):
            LOGGER.error("Cache file not found.")
            sys.exit(f"Error opening cache at: {cache_file}")

        # Set Debug logging if necessary
        if DEBUG:
            logging.basicConfig(level=logging.DEBUG)
        elif not DEBUG:
            logging.basicConfig(level=logging.INFO)

        # Parsing
        # TODO: We need to initialize the data_processor outside
        # of the loop to keep our data file open and only write
        # once as soon as we have processed all cache files
        # NOTE: This is only needed for bulk import of many cache
        # files at once (e.g. in case of reimporting all older
        # cache files) so not really needed for now, but nice to
        # have anyway
        data_processor = DataProcessor.new_with_collected_data(cache_data)

        # Update our data file

        try:
            if os.path.exists(
                GLOBAL_SETTINGS["FILESYSTEM"]["PARQUET_FILE_PATH"]
            ):
                LOGGER.info("Updating parquet file ...")
                # TODO: When there are more than one cache file
                # keep the parquet file open until we imported
                # the last dataset and then write to disk
                # saves time
                data_processor.update_parquet_file()
            else:
                LOGGER.info("Creating new parquet file ...")
                data_processor.create_dataframe_from_newly_collected_data(
                    mode="create_new"
                )
                data_processor.export_dataframe_to_parquet()
        except (FileNotFoundError):
            LOGGER.error("Data file not found.")
            # flake8: noqa: E501
            raise_error(
                f"Error opening data file at: {GLOBAL_SETTINGS['FILESYSTEM']['PARQUET_FILE_PATH']}"
            )

        LOGGER.info(f"Processing of cache file: {cache_file} finished.")

        filename = os.path.basename(cache_file)
        full_path = f"{GLOBAL_SETTINGS['FILESYSTEM']['ARCHIVED_CACHE_FOLDER']}{filename}"

        LOGGER.info(f"Moving cache file to {full_path} ...")
        shutil.move(cache_file, full_path)
        LOGGER.info("Cache file moved.")


if __name__ == "__main__":
    data_processing()
