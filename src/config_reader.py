import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict


@dataclass
class Font:
    name: str
    url: str


@dataclass
class Config:
    packages: List[str]
    fonts: List[Font]


def from_file(path: Path) -> Config:
    with open(path, 'r') as f:
        as_dict = json.loads(f.read())

    return _dict_to_config(as_dict)


def _dict_to_config(d: Dict) -> Config:
    return Config(
        packages=d['packages'],
        fonts=[Font(**font) for font in d['fonts']]
    )
