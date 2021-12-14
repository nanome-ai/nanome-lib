import json
import logging
import os
import sys
from collections import deque
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler

from nanome._internal._network import _Packet


class LogTypes:
    """Log Codes as expected by NTS."""
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3


class NTSFormatter(logging.Formatter):
    """Send NTS json data with specified log level numbers."""

    datefmt = "%Y-%m-%dT%H:%M:%S"

    fmt = {
        'timestamp': '%(asctime)s',
        'msg': '%(message)s',
        'sev': '%(levelname)s',  # Will be manually updated to val from LogType enum.
    }

    def __init__(self, fmt=None, **kwargs):
        # Use format saved by class, so no need to pass fmt kwarg
        fmt = json.dumps(self.fmt)
        super(NTSFormatter, self).__init__(fmt=fmt, datefmt=self.datefmt, **kwargs)

    def format(self, record):
        msg = super(NTSFormatter, self).format(record)
        json_msg = json.loads(msg.replace('\n', '\\n'))

        # Convert timestamp to UTC
        timestamp = json_msg['timestamp']
        timestamp_dt = datetime.strptime(timestamp, self.datefmt)
        utc_dt = timestamp_dt.astimezone(timezone.utc)
        json_msg['timestamp'] = utc_dt.strftime(self.datefmt)

        # Replace `sev` value with corresponding LogType from enum.
        level_name = json_msg['sev']
        enum_val = getattr(LogTypes, level_name)
        json_msg['sev'] = enum_val
        updated_msg = json.dumps(json_msg)
        return updated_msg


class NTSLoggingHandler(logging.Handler):
    """Forward Log messages to NTS."""

    def __init__(self, plugin, *args, **kwargs):
        super(NTSLoggingHandler, self).__init__(*args, **kwargs)
        self._plugin = plugin
        # Unique Identifier for current Nanome session
        self.formatter = NTSFormatter()

    def handle(self, record):
        # Use new NTS message format to forward logs.
        fmted_msg = self.formatter.format(record)
        packet = _Packet()
        packet.set(0, _Packet.packet_type_live_logs, 0)
        packet.write_string(fmted_msg)
        self._plugin._network.send(packet)


class ColorFormatter(logging.Formatter):
    """Print log outputs in color.

    https://stackoverflow.com/a/56944256
    """

    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    no_underline = "\x1b[24m"
    formats = {}

    def __init__(self, fmt=None, **kwargs):
        super(ColorFormatter, self).__init__(fmt, **kwargs)
        self.formats = {
            logging.DEBUG: self.grey + fmt + self.reset,
            logging.INFO: self.grey + fmt + self.reset,
            logging.WARNING: self.yellow + self.no_underline + fmt + self.reset,
            logging.ERROR: self.red + self.no_underline + fmt + self.reset,
            logging.CRITICAL: self.bold_red + fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        if self.supports_color():
            output = formatter.format(record)
        else:
            output = super(ColorFormatter, self).format(record)
        return output

    @staticmethod
    def supports_color():
        """Return True if the running system's terminal supports color, False otherwise.

        source: https://github.com/django/django/blob/main/django/core/management/color.py#L20
        """
        def vt_codes_enabled_in_windows_registry():
            """
            Check the Windows Registry to see if VT code handling has been enabled
            by default, see https://superuser.com/a/1300251/447564.
            """
            try:
                # winreg is only available on Windows.
                import winreg
            except ImportError:
                return False
            else:
                reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Console')
                try:
                    reg_key_value, _ = winreg.QueryValueEx(reg_key, 'VirtualTerminalLevel')
                except FileNotFoundError:
                    return False
                else:
                    return reg_key_value == 1

        # isatty is not always implemented, #6223.
        is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()

        return is_a_tty and (
            sys.platform != 'win32' or
            'ANSICON' in os.environ or
            # Windows Terminal supports VT codes.
            'WT_SESSION' in os.environ or
            # Microsoft Visual Studio Code's built-in terminal supports colors.
            os.environ.get('TERM_PROGRAM') == 'vscode' or
            vt_codes_enabled_in_windows_registry()
        )


class _LogsManager():
    """Manages our logging system, and creates required Handlers.

    - Every log manager has a console_handler, which outputs messages to the console.
    - If write_log_file is set to True, log_file_handler will write messages to file.
    - If remote_logging is True, Logs are forwarded to NTS.
    """

    _pending = deque()

    def __init__(self, filename=None, plugin=None, write_log_file=True, remote_logging=False):
        filename = filename or ''

        logging_level = logging.DEBUG
        self.logger = logging.getLogger(plugin.__class__.__name__)
        self.logger.setLevel(logging_level)

        self.console_handler = self.create_console_handler()
        self.log_file_handler = logging.NullHandler()
        self.nts_handler = logging.NullHandler()

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
        for _ in range(0, len(_LogsManager._pending)):
            log_type, entry = _LogsManager._pending.popleft()
            if log_type == 'info':
                self.logger.info(entry)
            elif log_type == 'warning':
                self.logger.warning(entry)
            elif log_type == 'debug':
                self.logger.debug(entry)
            elif log_type == 'error':
                self.logger.error(entry)

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
