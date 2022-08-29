import datetime
import os
import shlex
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


def export_revision(repo_dir: str, revision: str, target_dir: str) -> None:
    target_dir = os.path.realpath(target_dir)
    os.makedirs(target_dir, exist_ok=True)
    subprocess.check_output(
        f"git archive --format=tar {shlex.quote(revision)} | tar x -C {shlex.quote(target_dir)}",
        cwd=repo_dir,
        shell=True,
    )
