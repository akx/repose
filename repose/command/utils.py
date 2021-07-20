from datetime import timedelta
from typing import Optional

import click

from repose.ts import parse_resolution


def validate_resolution(
    ctx: click.Context, param: click.Option, value: Optional[str]
) -> Optional[timedelta]:
    if value is None:
        return None
    resolution = parse_resolution(value)
    if resolution.total_seconds() < 0:
        raise click.BadParameter("resolution too small")
    return resolution
