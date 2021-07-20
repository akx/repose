import os
from operator import itemgetter

import click
import tqdm

from repose.command.utils import validate_resolution
from repose.db import ReposeDB
from repose.gen import calculate_revision_stats
from repose.git import get_commit_timestamps
from repose.ts import thin_time_sequence


@click.argument("repo")
@click.option(
    "-r",
    "--resolution",
    callback=validate_resolution,
    default="1d",
    help="resolution (e.g. 1d, 1w, ...)",
)
@click.option("-d", "--database", required=True, help="path to database file to save")
@click.command()
def scan(repo, resolution, database):
    repo = os.path.realpath(repo)
    hashes_and_timestamps = list(get_commit_timestamps(repo))

    thinned_hashes_and_timestamps = list(
        thin_time_sequence(
            hashes_and_timestamps,
            time_getter=itemgetter(1),
            interval=resolution,
        )
    )

    db = ReposeDB(database)

    with tqdm.tqdm(thinned_hashes_and_timestamps, unit="rev", unit_scale=True) as pb:
        for hash, timestamp in pb:
            if db.has_hash(hash):
                continue
            pb.set_postfix_str(str(timestamp))
            data = calculate_revision_stats(repo, hash)
            db.add_data(hash=hash, timestamp=timestamp, data=data)
            db.commit()
