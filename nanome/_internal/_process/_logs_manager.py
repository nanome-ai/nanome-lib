from collections import deque
import logging
from logging.handlers import RotatingFileHandler


class _LogsManager():
    __pending = deque()

    def __init__(self, filename, write_log_file=True, forward_to_nts=True):
        self.write_log_file = write_log_file
        self.forward_to_nts = forward_to_nts
        # Set up File Logger
        self._file_logger = logging.getLogger('file_logger')
        self._file_logger.setLevel(logging.DEBUG)
        self._file_handler = RotatingFileHandler(filename, maxBytes=1048576, backupCount=3, delay=False)
        self._file_logger.addHandler(self._file_handler)

        # Set up Log Forwarding to NTS
        self._nts_logger = logging.getLogger('file_logger')
        self._nts_logger.setLevel(logging.DEBUG)
        self._nts_handler = logging.StreamHandler()
        self._nts_logger.addHandler(self._nts_handler)

    def update(self):
        for _ in range(0, len(_LogsManager.__pending)):
            entry = _LogsManager.__pending.popleft()
            if self.write_log_file:
                self._file_logger.info(entry)
            if self.forward_to_nts:
                self._nts_logger.info(entry)

    @classmethod
    def received_request(cls, request):
        cls.__pending.append(request)
