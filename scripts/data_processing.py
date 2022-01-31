# Intern
import logging
import lzma
import os
import pickle
import sys

from common import CACHE_FILE, PARQUET_FILE
from util.data_processor import DataProcessor

LOGGER = logging.getLogger(__name__)

DEBUG = True
WRITE = False


# TODO: We might also want to be able to pass more than one file
# e.g. wrapping all the following into a function and call that within a loop
# or better(?) add an array of cache files
# or add a folder containing the files and open them all (probably worse)

# TODO: Check what needs to be done to make

# Import data
try:
    if os.path.exists(CACHE_FILE):
        with lzma.open(CACHE_FILE, mode="rb") as handle:
            # We are aware of Pickle security implications
            cache_data = pickle.load(handle)  # nosec
except (FileNotFoundError):
    LOGGER.error("Cache file not found.")
    sys.exit(f"Error opening cache at: {CACHE_FILE}")

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
        data_processor.update_parquet_file()
    else:
        data_processor.create_dataframe_from_newly_collected_data(
            mode="create_new"
        )
        data_processor.export_dataframe_to_parquet()
except (FileNotFoundError):
    LOGGER.error("Data file not found.")
    sys.exit(f"Error opening data file at: {PARQUET_FILE}")

sys.exit(0)
