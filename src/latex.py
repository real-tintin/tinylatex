import subprocess
from pathlib import Path
from typing import Optional, List


def build(tex_path: Path, latexmk_opts: Optional[List[str]] = None):
    if latexmk_opts is None:
        latexmk_opts = []

    subprocess.run(["latexmk", *latexmk_opts, str(tex_path)], cwd=str(tex_path.parent))


def install_packages(packages: List[str]):
    subprocess.run(["tlmgr", "install", *packages])
