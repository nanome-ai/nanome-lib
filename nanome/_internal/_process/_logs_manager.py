from collections import deque
import logging
from logging.handlers import RotatingFileHandler


class _LogsManager():
    __pending = deque()

    def __init__(self, filename, write_log_file=True):
        self._logger = logging.getLogger('plugin_logger')
        self._logger.setLevel(logging.DEBUG)
        if write_log_file:
            self._handler = RotatingFileHandler(filename, maxBytes=1048576, backupCount=3, delay=False)
        else:
            self._handler = logging.StreamHandler()
        self._logger.addHandler(self._handler)

    def _update(self):
        for _ in range(0, len(_LogsManager.__pending)):
            entry = _LogsManager.__pending.popleft()
            self._logger.info(entry)

    @classmethod
    def _received_request(cls, request):
        cls.__pending.append(request)
