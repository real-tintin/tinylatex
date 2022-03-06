import json
from pathlib import Path
from unittest.mock import mock_open, patch

from config_reader import Config, Font, from_file

CONFIG_AS_JSON = json.dumps({
    'packages': ['ham', 'spam'],
    'fonts': [{'name': 'fake', 'url': 'does/not/exist'}, {'name': 'no', 'url': '404'}]
})

EXP_CONFIG = Config(
    packages=['ham', 'spam'],
    fonts=[Font(name='fake', url='does/not/exist'), Font(name='no', url='404')]
)


def test_from_file():
    with patch('config_reader.open', mock_open(read_data=CONFIG_AS_JSON), create=True) as _:
        act_config = from_file(path=Path('mocked'))
        assert act_config == EXP_CONFIG
