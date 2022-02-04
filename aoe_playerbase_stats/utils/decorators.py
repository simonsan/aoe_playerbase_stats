import functools
import time

import pandas as pd

from ..commons.settings import DF_OUT
from ..commons.shared import get_temp_df


def with_temporary_dataframe(func):
    """Use a temporary dataframe to enhance performance"""

    @functools.wraps(func)
    def wrapper_with_temporary_dataframe(*args, **kwargs):
        global DF_OUT
        temp_df = get_temp_df()
        value = func(temp_df, *args, **kwargs)
        new = pd.concat([DF_OUT, value], axis=1)
        # De-fragment frame
        DF_OUT = new.copy()
        return

    return wrapper_with_temporary_dataframe


def timing(func):
    """Print the runtime of the decorated function"""

    @functools.wraps(func)
    def wrapper_timing(*args, **kwargs):
        start_time = time.perf_counter()  # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()  # 2
        run_time = end_time - start_time  # 3
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value

    return wrapper_timing


def debug(func):
    """Print the function signature and return value"""

    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]  # 1
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
        signature = ", ".join(args_repr + kwargs_repr)  # 3
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")  # 4
        return value

    return wrapper_debug


def slow_down(func):
    """Sleep 1 second before calling the function"""

    @functools.wraps(func)
    def wrapper_slow_down(*args, **kwargs):
        time.sleep(1)
        return func(*args, **kwargs)

    return wrapper_slow_down
