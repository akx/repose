from repose._json import loads
import shutil
import subprocess
import tempfile

from repose.tool_paths import TOKEI
from repose.git import export_revision


def calculate_revision_stats(repo_dir: str, revision: str) -> dict:
    tempdir = tempfile.mkdtemp(prefix="repose-checkout-")
    try:
        export_revision(repo_dir, revision, tempdir)
        output = subprocess.check_output([TOKEI, "-o", "json", "."], cwd=tempdir)
        return loads(output)
    finally:
        shutil.rmtree(tempdir)
