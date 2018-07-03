import os
import shlex
import subprocess
import datetime


def get_commit_timestamps(repo_dir, branch='master'):
    log_lines = subprocess.check_output(
        'git log --reverse --date-order --pretty=%%H:%%ct %s' % shlex.quote(branch),
        cwd=repo_dir,
        shell=True,
    )
    for line in log_lines.splitlines():
        hash, timestamp = line.strip().decode().split(':')
        yield (hash, datetime.datetime.utcfromtimestamp(float(timestamp)))


def export_revision(repo_dir, revision, target_dir):
    target_dir = os.path.realpath(target_dir)
    os.makedirs(target_dir, exist_ok=True)
    subprocess.check_output(
        'git archive --format=tar %(revision)s | tar x -C %(target_dir)s' % {
            'revision': shlex.quote(revision),
            'target_dir': shlex.quote(target_dir),
        },
        cwd=repo_dir,
        shell=True,
    )
