import subprocess
from os import listdir, path
from pathlib import Path
from typing import Optional, List


def build(root: Path, filename: Optional[Path] = None, latexmk_opts: Optional[List[str]] = None):
    if filename is None:
        filepath = _find_first_tex_file(root)
    else:
        filepath = root / filename

    if latexmk_opts is None:
        latexmk_opts = []

    subprocess.run(["latexmk", *latexmk_opts, str(filepath)], cwd=str(root))


def install_pkg_from_file(path: Path):
    with open(path, 'r') as f:
        packages = f.read().splitlines()

    subprocess.run(["tlmgr", "install", *packages])


def _find_first_tex_file(root: Path) -> Path:
    for filename in listdir(root):
        _, ext = path.splitext(filename)
        if ext.lower() == '.tex':
            return root / Path(filename)

    raise FileNotFoundError(f'No .tex files found in {root}')
