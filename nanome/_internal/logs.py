import json
import logging
import os
import sys
from dateutil import parser
from logging.handlers import RotatingFileHandler

from nanome._internal._network import _Packet
from nanome._internal._util import _DataType, _ProcData


class LogTypes:
    """Log Codes as expected by NTS."""
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3


class PipeHandler(logging.Handler):
    """Send log records through pipe to main process.

    Resolves issues with logging from multiple processes.
    """
    def __init__(self, pipe_conn):
        super(PipeHandler, self).__init__()
        self.pipe_conn = pipe_conn

    def emit(self, record):
        to_send = _ProcData()
        to_send._type = _DataType.log
        to_send._data = record
        try:
            self.pipe_conn.send(to_send)
        except BrokenPipeError:
            # Connection has been closed.
            pass


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
        timestamp_dt = parser.parse(timestamp)
        json_msg['timestamp'] = timestamp_dt.strftime(self.datefmt)

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

    grey = "\x1b[0m"
    yellow = "\x1b[33m"
    red = "\x1b[91m"
    bold_red = "\x1b[91m"
    reset = "\x1b[0m"
    formats = {}

    def __init__(self, fmt=None, **kwargs):
        super(ColorFormatter, self).__init__(fmt, **kwargs)
        self.formats = {
            logging.DEBUG: self.grey + fmt + self.reset,
            logging.INFO: self.grey + fmt + self.reset,
            logging.WARNING: self.yellow + fmt + self.reset,
            logging.ERROR: self.red + fmt + self.reset,
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
        return not sys.platform == 'win32' or not sys.stdout.isatty()


class LogsManager():
    """Manages our logging system, and creates required Handlers.

    - Every log manager has a console_handler, which outputs messages to the console.
    - If write_log_file is set to True, log_file_handler will write messages to file.
    - If remote_logging is True, Logs are forwarded to NTS.
    """

    def __init__(self, filename=None, plugin=None, write_log_file=True, remote_logging=False):
        self.filename = filename or ''
        self.plugin = plugin
        self.write_log_file = write_log_file
        self.remote_logging = remote_logging

    def configure_main_process(self):
        logging_level = logging.INFO
        if self.plugin and self.plugin.verbose:
            logging_level = logging.DEBUG
        self.logger = logging.getLogger()
        self.logger.setLevel(logging_level)

        self.console_handler = self.create_console_handler()
        self.log_file_handler = logging.NullHandler()
        self.nts_handler = logging.NullHandler()

        # If timezone not specified, set to UTC
        if not os.environ.get('TZ'):
            os.environ['TZ'] = 'UTC'

        existing_handler_types = set([type(hdlr) for hdlr in logging.getLogger().handlers])
        if self.write_log_file and self.filename:
            self.log_file_handler = self.create_log_file_handler(self.filename)
            self.log_file_handler.setLevel(logging_level)
            if type(self.log_file_handler) not in existing_handler_types:
                self.logger.addHandler(self.log_file_handler)

        if self.remote_logging and self.plugin:
            self.nts_handler = self.create_nts_handler(self.plugin)
            self.nts_handler.setLevel(logging_level)
            if type(self.nts_handler) not in existing_handler_types:
                self.logger.addHandler(self.nts_handler)

        if type(self.console_handler) not in existing_handler_types:
            self.logger.addHandler(self.console_handler)

    @classmethod
    def configure_child_process(cls, pipe_conn, plugin_name):
        """Set up a PipeHandler that forwards all Logs to the main Process."""
        if os.name == 'nt':
            # Windows requires pipes going to main process to access logs
            # Send all logs, and let main process determine what logging level to show.
            logger = logging.getLogger()
            logger.setLevel(logging.DEBUG)
            pipe_handler = PipeHandler(pipe_conn)
            pipe_handler.level = logging.DEBUG
            logger.addHandler(pipe_handler)
        else:
            # Mac/Linux can be configured the same way as the main process
            # Get logging settings from sys.argv and config
            from nanome.api import Plugin
            parser = Plugin.create_parser()
            settings, _ = parser.parse_known_args()
            filename = plugin_name + ".log"
            obj = cls(filename=filename, write_log_file=settings.write_log_file, remote_logging=settings.remote_logging)
            obj.configure_main_process()

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

    @staticmethod
    def log_record(record):
        """When a log record is received through the PipeHandler, log it."""
        logger = logging.getLogger(record.name)
        logger.handle(record)
