import os
from operator import itemgetter

import click
import tqdm

from repose.chart import generate_chart_data, generate_streamchart
from repose.db import ReposeDB
from repose.gen import calculate_revision_stats
from repose.git import get_commit_timestamps
from repose.ts import parse_resolution, thin_time_sequence


def validate_resolution(ctx, param, value):
    if value is None:
        return None
    resolution = parse_resolution(value)
    if resolution.total_seconds() < 0:
        raise click.BadParameter('resolution too small')
    return resolution


@click.group()
def cli():
    pass


@cli.command()
@click.argument('repo')
@click.option('-r', '--resolution', callback=validate_resolution, default='1d', help='resolution (e.g. 1d, 1w, ...)')
@click.option('-d', '--database', required=True, help='path to database file to save')
def scan(repo, resolution, database):
    repo = os.path.realpath(repo)
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


@cli.command()
@click.option('-r', '--resolution', callback=validate_resolution, default=None)
@click.option('-o', '--output', default='chart.html')
@click.argument('database', required=True)
def chart(database, resolution, output):
    db = ReposeDB(database)
    chart_data = generate_chart_data(db, resolution)
    streamchart = generate_streamchart(chart_data)
    streamchart = streamchart.interactive()
    streamchart.save(output)


if __name__ == '__main__':
    cli()
