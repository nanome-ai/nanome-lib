from collections import deque
import logging
from logging.handlers import RotatingFileHandler


class NTSLoggingHandler(logging.StreamHandler):
    """Forward Log records to NTS."""

    def __init__(self, plugin, *args, **kwargs):
        self._plugin = plugin
        super().__init__(*args, **kwargs)

    def handle(self, record):
        super().handle(record)
        # Use new NTS message format to forward logs.
        log_code = 'SomethingSomething'  # What should this real value be?
        expects_response = False
        self._plugin._network.send(log_code, record, expects_response)


class _LogsManager():
    __pending = deque()

    def __init__(self, filename, write_log_file=True, plugin=None, remote_logging=False):
        self.write_log_file = write_log_file
        self.remote_logging = remote_logging
        self.plugin = plugin

        # Set up File Logger
        self.file_logger = logging.getLogger('file_logger')
        self.file_logger.setLevel(logging.DEBUG)
        self._file_handler = RotatingFileHandler(filename, maxBytes=1048576, backupCount=3, delay=False)
        self.file_logger.addHandler(self._file_handler)

        # Set up Log Forwarding to NTS
        self.nts_logger = logging.getLogger('nts_logger')
        self.nts_logger.setLevel(logging.DEBUG)
        self._nts_handler = NTSLoggingHandler(self.plugin)
        self.nts_logger.addHandler(self._nts_handler)

    def update(self):
        for _ in range(0, len(_LogsManager.__pending)):
            entry = _LogsManager.__pending.popleft()
            if self.write_log_file:
                self.file_logger.info(entry)
            if self.remote_logging:
                self.nts_logger.info(entry)

    @classmethod
    def received_request(cls, request):
        cls.__pending.append(request)
