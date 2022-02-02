from collections import defaultdict
from collections.abc import Iterable

import pandas as pd
from aoe_playerbase_stat.settings import DATA_SET_TIMESTAMP


def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from flatten(x, ignore_types)
        else:
            yield x


def unpack_list(_list):
    if len(_list) == 0:
        return _list
    if isinstance(_list[0], list):
        return unpack_list(_list[0]) + unpack_list(_list[1:])
    return _list[:1] + unpack_list(_list[1:])


def initialise_defaultdict_recursive():
    return defaultdict(initialise_defaultdict_recursive)


def get_temp_df():
    temp_df = pd.DataFrame()
    temp_df["timestamp"] = [DATA_SET_TIMESTAMP]
    temp_df.set_index("timestamp", inplace=True)
    return temp_df
