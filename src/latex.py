import subprocess
from enum import Enum
from os import listdir, path
from pathlib import Path
from typing import Optional


class OutFormat(Enum):
    Pdf = '-pdf'
    Dvi = '-dvi'
    Ps = '-ps'


def build(root: Path, filename: Optional[Path] = None, out_format: OutFormat = OutFormat.Pdf):
    if filename is None:
        filepath = _find_first_tex_file(root)
    else:
        filepath = root / filename

    subprocess.run(["latexmk", out_format.value, str(filepath)], cwd=str(root))


def clean_up(root: Path):
    subprocess.run(["latexmk", "-c"], cwd=str(root))


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
