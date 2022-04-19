import logging
import time
from os import path
from pathlib import Path
from threading import Thread
from typing import Callable, List, Optional, Dict

logger = logging.getLogger(__name__)


class FileWatcher:
    def __init__(self,
                 root: Path,
                 cb: Callable,
                 interval_s: float = 1.0,
                 globs: Optional[List] = None):
        """
        Monitors file changes in root on a given interval_s. Calls
        the cb on file changes matching globs.
        """
        if globs is None:
            globs = ['*.']

        self._root = root
        self._cb = cb
        self._interval_s = interval_s
        self._globs = globs

        self._run = False
        self._thread = Thread(target=self._run_in_thread)

        self._timed_content_old = {}

    def start(self):
        self._run = True
        self._thread.start()

    def stop(self):
        self._run = False
        self._thread.join()

    def _run_in_thread(self):
        while self._run:
            if self._is_content_updated():
                self._cb()

            time.sleep(self._interval_s)

    def _is_content_updated(self) -> bool:
        timed_content_new = self._get_timed_content(self._root, self._globs)

        timed_content_diff = set(timed_content_new.items()) - set(self._timed_content_old.items())
        timed_content_diff_paths = [str(timed_path[0]) for timed_path in timed_content_diff]

        self._timed_content_old = timed_content_new

        is_updated = len(timed_content_diff) > 0

        if is_updated:
            logger.info(f'File(s) updated {timed_content_diff_paths}')

        return is_updated

    @staticmethod
    def _get_timed_content(root: Path, globs: List) -> Dict:
        timed_content = {}

        for glob in globs:
            for content in root.rglob(glob):
                timed_content[content] = path.getmtime(content)

        return timed_content
