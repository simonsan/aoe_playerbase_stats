# Intern
import logging
import lzma
import os
import pickle
import shutil
import sys

from util.common import CACHE_FILES, PARQUET_FILE, ARCHIVED_CACHE_PATH
from util.data_processor import DataProcessor

LOGGER = logging.getLogger(__name__)

DEBUG = True
WRITE = False

# Set Debug logging if necessary
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
elif not DEBUG:
    logging.basicConfig(level=logging.INFO)

for cache_file in CACHE_FILES:

    LOGGER.info(f"Processing cache file: {cache_file}. Please wait ...")

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
    data_processor = DataProcessor.new_with_collected_data(cache_data)

    # Update our data file
    try:
        if os.path.exists(PARQUET_FILE):
            LOGGER.info("Updating parquet file ...")
            data_processor.update_parquet_file()
        else:
            LOGGER.info("Creating new parquet file ...")
            data_processor.create_dataframe_from_newly_collected_data(
                mode="create_new"
            )
            data_processor.export_dataframe_to_parquet()
    except (FileNotFoundError):
        LOGGER.error("Data file not found.")
        sys.exit(f"Error opening data file at: {PARQUET_FILE}")

    LOGGER.info(f"Processing of cache file: {cache_file} finished.")

    filename = os.path.basename(cache_file)
    full_path = f"{ARCHIVED_CACHE_PATH}{filename}"

    LOGGER.info(f"Moving cache file to {full_path} ...")
    shutil.move(cache_file, full_path)
    LOGGER.info("Cache file moved.")

sys.exit(0)
