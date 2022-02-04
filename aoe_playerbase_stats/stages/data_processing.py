# Intern
import lzma
import os
import pickle
from shutil import copyfile, move, SameFileError

# Progress bar
from tqdm import tqdm

from ..commons.settings import CACHE_FILES, GLOBAL_SETTINGS
from ..utils.data_processor import DataProcessor
from ..utils.error import raise_error

LOGGER = GLOBAL_SETTINGS["LOGGING"]

WRITE = False


def backup_parquet_file(file: str) -> bool:
    filename = os.path.basename(file)
    folder = os.path.dirname(file)

    try:
        copyfile(file, f"{folder}/{filename}.bkp")
    except OSError:
        raise_error(
            f"Location for backup not writable: {folder}/{filename}.bkp"
        )
    except SameFileError:
        raise_error(
            f"File already exists in location: {folder}/{filename}.bkp"
        )

    return True


def archive_cache_file(cache_file: str) -> bool:

    # Stripped filename
    filename = os.path.basename(cache_file)

    try:
        os.makedirs(
            GLOBAL_SETTINGS["FILESYSTEM"]["ARCHIVED_CACHE_FOLDER"],
            exist_ok=True,
        )
    except OSError:
        raise_error(
            "Invalid path name for archive path: "
            f"{GLOBAL_SETTINGS['FILESYSTEM']['ARCHIVED_CACHE_FOLDER']}"
            f"{filename} or not enough disk space."
        )

    full_path = (
        f"{GLOBAL_SETTINGS['FILESYSTEM']['ARCHIVED_CACHE_FOLDER']}{filename}"
    )

    LOGGER.debug(f"Moving cache file to {full_path} ...")
    if not os.path.exists(full_path):
        move(cache_file, full_path)
    else:
        raise_error(f"Cache file already exists in location: {full_path}")
    LOGGER.debug("Cache file archived.")

    return True


def data_processing() -> bool:

    if os.path.exists(GLOBAL_SETTINGS["FILESYSTEM"]["PARQUET_FILE_PATH"]):
        data_processor = DataProcessor.new_with_parquet_file(
            GLOBAL_SETTINGS["FILESYSTEM"]["PARQUET_FILE_PATH"]
        )
    else:
        try:
            os.makedirs(
                os.path.dirname(
                    GLOBAL_SETTINGS["FILESYSTEM"]["PARQUET_FILE_PATH"]
                ),
                exist_ok=True,
            )
        except OSError:
            raise_error(
                "Invalid path name for parquet file: "
                f"""{os.path.basename(
                    GLOBAL_SETTINGS['FILESYSTEM']['PARQUET_FILE_PATH']
                    )}
                """
            )
        data_processor = DataProcessor.new_without_parquet_file()

    pbar = tqdm(
        total=len(CACHE_FILES),
        desc="Processing cache file",
        unit=" files",
        initial=0,
    )

    for cache_file in CACHE_FILES:

        # LOGGER.info(
        #     f"Processing cache file ({cache_file_count}/"
        #     f"{len(CACHE_FILES)}): {cache_file}. Please wait ..."
        # )

        # Import data
        try:
            if os.path.exists(cache_file):
                with lzma.open(cache_file, mode="rb") as handle:
                    # We are aware of Pickle security implications
                    cache_data = pickle.load(handle)  # nosec
        except (FileNotFoundError):
            LOGGER.error("Cache file not found.")
            raise_error(f"Error opening cache at: {cache_file}")

        # Appends new data from cache
        data_processor.process_new_data_from(cache_data)

        LOGGER.debug(f"Processing of cache file: {cache_file} finished.")

        pbar.update(1)

    pbar.close()

    # Creates the dataframes from collected data
    data_processor.produce_dataframe()

    LOGGER.info("Updating/exporting parquet file ...")
    try:
        backup_parquet_file(GLOBAL_SETTINGS["FILESYSTEM"]["PARQUET_FILE_PATH"])
        data_processor.export_dataframe_to_parquet()
    except OSError:
        raise_error(
            "Please check if you have enough disk space. OS threw an error."
        )

    # Archive cache files
    for file in CACHE_FILES:
        archive_cache_file(file)

    return True


if __name__ == "__main__":
    data_processing()
