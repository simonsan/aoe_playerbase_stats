import asyncio
import datetime
import logging
import lzma
import os
import pickle
import sys
import time

# Extern
import aiohttp

# Intern
from common import (
    AOC_REF_DATA,
    AOC_REF_DATA_FILE,
    CACHE_FILE,
    leaderboard_settings,
)

LOGGER = logging.getLogger(__name__)

DEBUG = False
CACHE = True
GRANULAR = False
SAVE_INTERMEDIATE_CACHE = False

# Check for cache hit
if os.path.exists(CACHE_FILE):
    CACHE_HIT = True
else:
    CACHE_HIT = False
    if CACHE:
        SAVE_CACHE = True
        if GRANULAR:
            SAVE_INTERMEDIATE_CACHE = True

# Set Debug logging if necessary
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
elif not DEBUG:
    logging.basicConfig(level=logging.INFO)


# Get aoc-ref-data
async def get_aoc_ref_data(session, url=AOC_REF_DATA):
    LOGGER.debug("querying aoc_ref_data")

    async with session.get(url) as resp:
        if resp.status == 200:
            data = await resp.json(content_type=None, encoding="utf8")
            LOGGER.debug(f"Data length: {len(data)} of aoc_ref_data")
            with open(AOC_REF_DATA_FILE, "wb") as handle:
                pickle.dump(data, handle)
        else:
            LOGGER.error(
                f"Response status not 'SUCCESS != {resp.status}'"
                " for aoc_ref_data"
            )
            return
    return (("aoc_ref", None), data)


# Get *all* account entries from *all* leaderboards
async def get_all_player_data_from_leaderboard(
    session, url, game, leaderboard
):

    start_time = time.time()

    # Wait seconds between requests
    # secs = 1
    offset = 0

    # This is the allowed maximum by the API
    if game == "aoe2":
        length = 10000
    else:
        length = 1000

    collector = []
    items = 0

    while True:

        req_url = f"{url}&start={offset}&length={length}"

        LOGGER.debug(f"querying at {game}_{leaderboard} with offset {offset}")
        # LOGGER.debug(f"DEBUG REQUEST: {req_url}")

        async with session.get(req_url) as resp:
            if resp.status == 200:
                # Deactivate content type check for instable API
                data = await resp.json(content_type=None, encoding="utf8")
                data_length = len(data["data"])
                LOGGER.debug(
                    f"Data length: {data_length} of {game}_{leaderboard}"
                )
                items += data_length
                for item in data["data"]:
                    collector.append(item)
            else:
                LOGGER.error(
                    f"Response status not 'SUCCESS != {resp.status}' for"
                    f" {game}_{leaderboard} request."
                )
                return ((game, leaderboard), None)

        if len(data["data"]) < length:
            # Write data back to file
            if SAVE_INTERMEDIATE_CACHE:
                with open(
                    f"./data_temp/{game}_{leaderboard}.pickle", "wb"
                ) as handle:
                    pickle.dump(collector, handle)

            break
        else:
            offset += length

        # TODO: Production
        # time.sleep(secs)

    LOGGER.info(
        f"Overall collected {items} item(s) from {game}_{leaderboard} in "
        f"{time.time() - start_time} seconds."
    )
    return ((game, leaderboard), collector)


# Main
async def main():

    LOGGER.info("Data collection started.")

    start_time = time.time()

    if not CACHE_HIT:
        LOGGER.info("Cache not hit, collecting data ...")

        now = datetime.datetime.now()

        # Setup basic data layout for leaderboard file
        main_data = {
            "date": now.isoformat(),
            "aoc_ref": [],
            "aoe2": {},
            "aoe3": {},
            "aoe4": {},
        }

        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(
                limit_per_host=5, limit=50, ssl=False
            )
        ) as session:

            tasks = []

            # Get data from the server
            for game, leaderboard, _, url in leaderboard_settings:
                tasks.append(
                    asyncio.ensure_future(
                        get_all_player_data_from_leaderboard(
                            session,
                            url,
                            game,
                            leaderboard,
                        )
                    )
                )

            tasks.append(get_aoc_ref_data(session=session))

            api_data = await asyncio.gather(*tasks)

        for ((game, leaderboard), data) in api_data:
            if leaderboard is not None and game != "aoc_ref":
                main_data[game][leaderboard] = data
            elif leaderboard is None and game == "aoc_ref":
                main_data[game] = data
            elif data is None:
                main_data[game] = None

        LOGGER.info(
            f"Data collection took: {time.time() - start_time} seconds"
        )

        start_time = time.time()

        # Write data back to data file
        LOGGER.info(f"Writing data to Cache: {CACHE_FILE}")
        if SAVE_CACHE:
            with lzma.open(CACHE_FILE, mode="wb") as handle:
                pickle.dump(main_data, handle)

        LOGGER.info(
            f"Writing to cache took: {time.time() - start_time} seconds"
        )

    else:
        print("We're done, it's cached. ;)")

    LOGGER.info("Finished.")
    sys.exit(0)


asyncio.get_event_loop().run_until_complete(main())
