from abc import abstractmethod
from os import path, listdir
from pathlib import Path
from typing import Optional, List

import latex


class Builder:

    def __init__(self, root: Path, main: Optional[Path] = None, latexmk_opts: Optional[List[str]] = None):
        self._root = root
        self._latexmk_opts = latexmk_opts

        if main is None:
            self._tex_path = self._find_first_tex_file(root)
        else:
            self._tex_path = root / main

        self._version = 0

    @abstractmethod
    def build(self):
        latex.build(tex_path=self._tex_path, latexmk_opts=self._latexmk_opts)
        self._version += 1

    def get_version(self):
        return self._version

    def get_tex_path(self):
        return self._tex_path

    @staticmethod
    def _find_first_tex_file(root: Path) -> Path:
        for filename in listdir(root):
            _, ext = path.splitext(filename)
            if ext.lower() == '.tex':
                return root / Path(filename)

        raise FileNotFoundError(f'No .tex files found in {root}')
