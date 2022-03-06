import subprocess
from os import listdir, path
from pathlib import Path
from typing import Optional, List


def build(root: Path, main: Optional[Path] = None, latexmk_opts: Optional[List[str]] = None):
    if main is None:
        filepath = _find_first_tex_file(root)
    else:
        filepath = root / main

    if latexmk_opts is None:
        latexmk_opts = []

    subprocess.run(["latexmk", *latexmk_opts, str(filepath)], cwd=str(root))


def install_packages(packages: List[str]):
    subprocess.run(["tlmgr", "install", *packages])


def _find_first_tex_file(root: Path) -> Path:
    for filename in listdir(root):
        _, ext = path.splitext(filename)
        if ext.lower() == '.tex':
            return root / Path(filename)

    raise FileNotFoundError(f'No .tex files found in {root}')
