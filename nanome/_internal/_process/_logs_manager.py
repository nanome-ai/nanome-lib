import logging
import os
import sys
from collections import deque
from logging.handlers import RotatingFileHandler

from nanome._internal.logging import ColorFormatter, NTSLoggingHandler


class LogsManager():
    """Manages our logging system, and creates required Handlers.

    - Every log manager has a console_handler, which outputs messages to the console.
    - If write_log_file is set to True, log_file_handler will write messages to file.
    - If remote_logging is True, Logs are forwarded to NTS.
    """

    _pending = deque()

    def __init__(self, filename=None, plugin=None, write_log_file=True, remote_logging=False):
        filename = filename or ''

        logging_level = logging.INFO
        if plugin.verbose:
            logging_level = logging.DEBUG

        self.logger = logging.getLogger()
        self.logger.setLevel(logging_level)

        self.console_handler = self.create_console_handler()
        self.log_file_handler = logging.NullHandler()
        self.nts_handler = logging.NullHandler()

        # If timezone not specified, set to UTC
        if not os.environ.get('TZ'):
            os.environ['TZ'] = 'UTC'

        if write_log_file and filename:
            self.log_file_handler = self.create_log_file_handler(filename)
            self.log_file_handler.setLevel(logging_level)
        if remote_logging and plugin:
            self.nts_handler = self.create_nts_handler(plugin)
            self.nts_handler.setLevel(logging_level)

        self.logger.addHandler(self.console_handler)
        self.logger.addHandler(self.log_file_handler)
        self.logger.addHandler(self.nts_handler)

    def update(self):
        """Pass log into logger under the appropriate levelname."""
        for _ in range(0, len(LogsManager._pending)):
            log_type, entry = LogsManager._pending.popleft()
            if log_type == 'info':
                self.logger.info(entry)
            elif log_type == 'warning':
                self.logger.warning(entry)
            elif log_type == 'debug':
                self.logger.debug(entry)
            elif log_type == 'error':
                # Only include exc_info if sys.exc_info is not None.
                # Otherwise logging formatter adds Nonetype:None to end of log,
                # which breaks JSON formatted log messages.
                use_exc_info = sys.exc_info()[0] is not None
                self.logger.error(entry, exc_info=use_exc_info)

    @classmethod
    def received_request(cls, log_type, request):
        cls._pending.append((log_type, request))

    @staticmethod
    def create_log_file_handler(filename):
        """Return handler that writes logs to provided filepath."""
        handler = RotatingFileHandler(filename, maxBytes=1048576, backupCount=3, delay=False)
        fmt = '%(asctime)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        return handler

    @staticmethod
    def create_nts_handler(plugin):
        """Return handler that forwards logs to NTS."""
        handler = NTSLoggingHandler(plugin)
        return handler

    @staticmethod
    def create_console_handler():
        """Return handler that writes log to console."""
        handler = logging.StreamHandler()
        fmt = "%(message)s"
        color_formatter = ColorFormatter(fmt)
        handler.setFormatter(color_formatter)
        return handler
