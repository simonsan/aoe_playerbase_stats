import logging
import datetime
import os
import json
import asyncio
import time
import sys

# Intern
from common import leaderboard_settings, CACHE_FILE

# from common import DATA_FILE

# Extern
import aiohttp

LOGGER = logging.getLogger(__name__)

DEBUG = True
CACHE = True

# Check for cache hit
if os.path.exists(CACHE_FILE):
    CACHE_HIT = True
else:
    CACHE_HIT = False
    if CACHE:
        SAVE_CACHE = True

# Set Debug logging if necessary
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
elif not DEBUG:
    logging.basicConfig(level=logging.INFO)


# Get *all* account entries from *all* leaderboards
async def get_all_player_data_from_leaderboard(
    session, url, game, leaderboard
):
    # Wait seconds between requests
    secs = 1
    offset = 0

    # This is the allowed maximum by the API
    length = 10000

    collector = []

    while True:

        req_url = f"{url}?start={offset}&length={length}"

        LOGGER.debug(f"querying at {game}_{leaderboard} with offset {offset}")
        LOGGER.debug(f"DEBUG REQUEST: {req_url}")

        async with session.get(req_url) as resp:
            if resp.status == 200:
                # Deactivate content type check for instable API
                data = await resp.json(content_type=None, encoding="utf8")
                collector.append(data["data"])

        if len(data["data"]) < length:
            # Write data back to file
            if SAVE_CACHE:
                with open(
                    f"./data_temp/{game}_{leaderboard}.json", "w"
                ) as handle:
                    json.dump(collector, handle, indent=4)
            break
        else:
            offset += length

        time.sleep(secs)

    return ((game, leaderboard), collector)


# Main
async def main():
    if not CACHE_HIT:
        today = datetime.date.today()

        # Setup basic data layout for leaderboard file
        main_data = {
            "date": today.isoformat(),
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
            for leaderboard in leaderboard_settings:
                tasks.append(
                    asyncio.ensure_future(
                        get_all_player_data_from_leaderboard(
                            session,
                            leaderboard.url,
                            leaderboard.game,
                            leaderboard.leaderboard,
                        )
                    )
                )

            api_data = await asyncio.gather(*tasks)

        for ((game, leaderboard), data) in api_data:

            # TODO: Check if flatten works
            temp_collector = []
            for part in data:
                temp_collector.append(part)

            main_data[game][leaderboard] = temp_collector

        # Write data back to data file
        if SAVE_CACHE:
            with open(CACHE_FILE, "w") as handle:
                json.dump(main_data, handle, indent=4)
    else:
        print("We're done, it's cached. ;)")

    sys.exit(0)


asyncio.get_event_loop().run_until_complete(main())
