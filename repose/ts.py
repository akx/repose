import re
from datetime import datetime, timedelta
from operator import itemgetter
from typing import Any, Iterator, Tuple

from repose.utils import make_thinner


def thin_time_sequence(
    sequence: Iterator[Any], time_getter: itemgetter, interval: timedelta
) -> Iterator[Tuple[str, datetime]]:
    item = last_item = None
    thinner = make_thinner(interval)
    for item in sequence:
        curr_time = time_getter(item)
        if thinner(curr_time):
            last_item = item
            yield item
    if last_item is not item:
        yield item


resolution_suffixes = {
    "m": lambda v: timedelta(minutes=v),
    "h": lambda v: timedelta(hours=v),
    "d": lambda v: timedelta(days=v),
    "w": lambda v: timedelta(weeks=v),
    "mo": lambda v: timedelta(days=v * 30),
}
resolution_bit_re = re.compile("([0-9.]+)\s*(\w+)")


def parse_resolution(value: str) -> timedelta:
    delta = timedelta()
    for bit in resolution_bit_re.finditer(value):
        value, suffix = bit.groups()
        value = float(value)
        delta += resolution_suffixes[suffix](value)
    return delta
