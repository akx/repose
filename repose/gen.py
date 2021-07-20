import json
import shutil
import subprocess
import tempfile

from repose.git import export_revision


def calculate_revision_stats(repo_dir: str, revision: str) -> dict:
    tempdir = tempfile.mkdtemp(prefix="repose-checkout-")
    try:
        export_revision(repo_dir, revision, tempdir)
        output = subprocess.check_output(
            "/usr/bin/env tokei -o json .",
            cwd=tempdir,
            shell=True,
        ).decode()
        return json.loads(output)
    finally:
        shutil.rmtree(tempdir)
