import datetime
import subprocess
from typing import Iterator, Tuple

from repose.tool_paths import GIT


def get_commit_timestamps(
    repo_dir: str,
    branch: str = "master",
) -> Iterator[Tuple[str, datetime.datetime]]:
    log_lines = subprocess.check_output(
        [
            GIT,
            "log",
            "--reverse",
            "--date-order",
            "--pretty=%H:%ct",
            branch,
        ],
        cwd=repo_dir,
        encoding="utf-8",
    )
    for line in log_lines.splitlines():
        hash, timestamp = line.strip().split(":")
        yield (hash, datetime.datetime.utcfromtimestamp(float(timestamp)))


