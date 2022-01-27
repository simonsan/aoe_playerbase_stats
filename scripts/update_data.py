import logging
import datetime
import json
import asyncio

# Intern
from common import DATA_FILE, leaderboard_settings

# Extern
import aiohttp

LOGGER = logging.getLogger(__name__)


async def get_player_amount(session, url, game, leaderboard):
    async with session.get(url) as resp:
        if resp.status == 200:
            # Deactivate content type check for instable API
            data = await resp.json(content_type=None)
            return ((game, leaderboard), data["recordsFiltered"])


# Main
async def main():
    LOGGER.info("Opening data file ...")
    with open(DATA_FILE, "r") as handle:
        leaderboard_data = json.load(handle)
    LOGGER.info("Data file loaded.")

    today = datetime.date.today()

    # Setup basic data layout for leaderboard file
    data_entry = {
        "date": today.isoformat(),
        "aoe2": {},
        "aoe3": {},
        "aoe4": {},
    }

    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False)
    ) as session:

        tasks = []
        # Get data from the server
        for game, leaderboard, _, url in leaderboard_settings:
            tasks.append(
                asyncio.ensure_future(
                    get_player_amount(
                        session,
                        url,
                        game,
                        leaderboard,
                    )
                )
            )

        api_data = await asyncio.gather(*tasks)

    for (game, leaderboard), data in api_data:
        data_entry[game][leaderboard] = data

    # Append the new data
    leaderboard_data.append(data_entry)

    # Write data back to data file
    with open(DATA_FILE, "w") as handle:
        json.dump(leaderboard_data, handle, indent=4)


asyncio.get_event_loop().run_until_complete(main())
