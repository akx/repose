import multiprocessing
import os
import datetime
from operator import itemgetter

import click
import tqdm

from repose.command.utils import validate_resolution
from repose.db import ReposeDB
from repose.gen import calculate_revision_stats
from repose.git import get_commit_timestamps
from repose.ts import thin_time_sequence


def _calculate_revision_stats(job):
    repo, revision, timestamp = job
    return (job, calculate_revision_stats(repo, revision))


@click.argument("repo")
@click.option(
    "-r",
    "--resolution",
    callback=validate_resolution,
    default="1d",
    show_default=True,
    help="resolution (e.g. 1d, 1w, ...)",
)
@click.option("-d", "--database", required=True, help="path to database file to save")
@click.command()
def scan(repo: str, resolution: datetime.timedelta, database: str):
    repo = os.path.realpath(repo)
    db = ReposeDB(database)

    jobs = [
        (repo, revision, timestamp)
        for (revision, timestamp) in thin_time_sequence(
            get_commit_timestamps(repo),
            time_getter=itemgetter(1),
            interval=resolution,
        )
        if not db.has_hash(revision)
    ]
    if not jobs:
        print(f"Nothing to do; likely all commits already scanned")
        return

    with multiprocessing.Pool(
        processes=max(1, multiprocessing.cpu_count() - 2)
    ) as pool, tqdm.tqdm(total=len(jobs), unit="rev", unit_scale=True) as pb:

        for (repo, revision, timestamp), data in pool.imap_unordered(
            _calculate_revision_stats, jobs, chunksize=3
        ):
            pb.set_postfix_str(str(timestamp), refresh=False)
            pb.update(1)
            db.add_data(hash=revision, timestamp=timestamp, data=data)
            db.commit()
