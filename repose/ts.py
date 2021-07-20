import re
from datetime import timedelta

from repose.utils import make_thinner


def thin_time_sequence(sequence, time_getter, interval):
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
    "d": lambda v: timedelta(days=v),
    "m": lambda v: timedelta(minutes=v),
    "mo": lambda v: timedelta(days=v * 30),
    "w": lambda v: timedelta(weeks=v),
}
resolution_bit_re = re.compile("([0-9.]+)\s*(\w+)")


def parse_resolution(value):
    delta = timedelta()
    for bit in resolution_bit_re.finditer(value):
        value, suffix = bit.groups()
        value = float(value)
        delta += resolution_suffixes[suffix](value)
    return delta
