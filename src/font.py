import os
from io import BytesIO
from pathlib import Path
from sys import platform
from typing import List, Dict
from zipfile import ZipFile

import requests
from werkzeug.http import parse_options_header

from config_reader import Font

FONT_ROOT = Path(os.environ["FONT_ROOT"])


def download(fonts: List[Font]):
    if platform != 'linux':
        raise NotImplementedError('Unsupported operating system')

    for font in fonts:
        print(f"Downloading {font.name} from {font.url}")

        response = requests.get(url=font.url)
        filename = _get_headers_filename(response.headers)

        if filename.suffix == '.otf' or filename.suffix == '.ttf':
            with open(file=FONT_ROOT / filename, mode="wb") as f:
                f.write(response.content)

        elif filename.suffix == '.zip':
            with ZipFile(BytesIO(response.content), mode='r') as zf:
                zf.extractall(FONT_ROOT)

        else:
            raise NotImplementedError("Unsupported file type.")


def _get_headers_filename(headers: Dict) -> Path:
    content_disposition = parse_options_header(headers['Content-Disposition'])
    return Path(content_disposition[1]['filename'])
