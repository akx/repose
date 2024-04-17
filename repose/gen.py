import os
import shlex
import shutil
import subprocess
import tempfile

from repose._json import loads
from repose.tool_paths import TOKEI, TOKEI_TAR


def calculate_revision_stats(repo_dir: str, revision: str) -> dict:
    if TOKEI_TAR:
        return calculate_revision_stats_with_tokei_tar(repo_dir, revision)
    return calculate_revision_stats_with_export(repo_dir, revision)


def calculate_revision_stats_with_export(repo_dir: str, revision: str):
    tempdir = tempfile.mkdtemp(prefix="repose-checkout-")
    try:
        os.makedirs(tempdir, exist_ok=True)
        subprocess.check_call(
            f"git archive --format=tar {shlex.quote(revision)} | tar x -C {shlex.quote(tempdir)}",
            cwd=repo_dir,
            shell=True,
        )
        output = subprocess.check_output([TOKEI, "-o", "json", "."], cwd=tempdir)
        return loads(output)
    finally:
        shutil.rmtree(tempdir)


def calculate_revision_stats_with_tokei_tar(repo_dir: str, revision: str) -> dict:
    lines = []
    for line in subprocess.check_output(
        f"git archive --format=tar {shlex.quote(revision)} | {TOKEI_TAR}",
        cwd=repo_dir,
        shell=True,
    ).splitlines():
        lines.append(loads(line))
    return {"format": "tokei-tar", "lines": lines}
