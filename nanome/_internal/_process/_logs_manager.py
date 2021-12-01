from collections import deque
import logging
from logging.handlers import RotatingFileHandler


class NTSLoggingHandler(logging.StreamHandler):
    """Forward Log messages to NTS."""

    def __init__(self, plugin, *args, **kwargs):
        self._plugin = plugin
        super(NTSLoggingHandler, self).__init__(*args, **kwargs)

    def handle(self, record):
        # Use new NTS message format to forward logs.
        log_code = 'SomethingSomething'  # What should this real value be?
        expects_response = False
        self._plugin._network.send(log_code, record.msg, expects_response)


class ColorFormatter(logging.Formatter):
    """Print log outputs in color."""

    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    def __init__(self, fmt_string, *args, **kwargs):
        super(ColorFormatter, self).__init__(fmt_string, *args, **kwargs)
        self.formats = {
            logging.DEBUG: self.grey + fmt_string + self.reset,
            logging.INFO: self.grey + fmt_string + self.reset,
            logging.WARNING: self.yellow + fmt_string + self.reset,
            logging.ERROR: self.red + fmt_string + self.reset,
            logging.CRITICAL: self.bold_red + fmt_string + self.reset
        }

    def format(self, record):
        log_fmt = self.formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class _LogsManager():
    _pending = deque()

    def __init__(self, filename, plugin=None, write_log_file=True, remote_logging=False):
        self.logger = logging.getLogger(plugin.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)

        self.console_handler = self.create_console_handler()
        self.log_file_handler = logging.NullHandler()
        self.nts_handler = logging.NullHandler()

        if write_log_file:
            self.log_file_handler = self.create_log_file_handler(filename)
        if remote_logging:
            self.nts_handler = self.create_nts_handler(plugin)

        self.logger.addHandler(self.console_handler)
        self.logger.addHandler(self.log_file_handler)
        self.logger.addHandler(self.nts_handler)

    def update(self):
        """Pass log into logger under the appropriate levelname."""
        for _ in range(0, len(_LogsManager._pending)):
            log_type, entry = _LogsManager._pending.popleft()
            if log_type == 'warning':
                self.logger.warning(entry)
            elif log_type == 'debug':
                self.logger.debug(entry)
            elif log_type == 'error':
                self.logger.error(entry)
            elif log_type == 'info':
                self.logger.info(entry)

    @classmethod
    def received_request(cls, log_type, request):
        cls._pending.append((log_type, request))

    @staticmethod
    def create_log_file_handler(filename):
        """Return handler that writes logs to provided filepath."""
        handler = RotatingFileHandler(filename, maxBytes=1048576, backupCount=3, delay=False)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        return handler

    @staticmethod
    def create_nts_handler(plugin):
        """Return handler that forwards logs to NTS."""
        handler = NTSLoggingHandler(plugin)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        return handler

    @staticmethod
    def create_console_handler():
        """Return handler that writes log to console."""
        handler = logging.StreamHandler()
        color_formatter = ColorFormatter("%(message)s")
        handler.setFormatter(color_formatter)
        return handler
