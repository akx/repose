from operator import itemgetter

import click
import tqdm

from repose.db import ReposeDB
from repose.gen import calculate_revision_stats
from repose.git import get_commit_timestamps
from repose.ts import parse_resolution, thin_time_sequence


def validate_resolution(ctx, param, value):
    resolution = parse_resolution(value)
    if resolution.total_seconds() <= 0:
        raise click.BadParameter('resolution too small')
    return resolution


@click.group()
def cli():
    pass


@cli.command()
@click.argument('repo')
@click.option('-r', '--resolution', callback=validate_resolution, default='1d')
@click.option('-d', '--database', required=True)
def scan(repo, resolution, database):
    hashes_and_timestamps = list(get_commit_timestamps(repo))

    thinned_hashes_and_timestamps = list(thin_time_sequence(
        hashes_and_timestamps,
        time_getter=itemgetter(1),
        interval=resolution,
    ))

    db = ReposeDB(database)

    with tqdm.tqdm(thinned_hashes_and_timestamps, unit='rev', unit_scale=True) as pb:
        for hash, timestamp in pb:
            if db.has_hash(hash):
                continue
            pb.set_postfix_str(str(timestamp))
            data = calculate_revision_stats(repo, hash)
            db.add_data(hash=hash, timestamp=timestamp, data=data)
            db.commit()


if __name__ == '__main__':
    cli()
