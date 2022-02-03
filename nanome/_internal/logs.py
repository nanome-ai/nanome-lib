import json
import logging
import os
import sys
import graypy
from logging.handlers import RotatingFileHandler

from nanome._internal._network import _Packet
from nanome._internal._util import _DataType, _ProcData
from tblib import pickling_support

pickling_support.install()

logger = logging.getLogger(__name__)


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


class NTSLoggingHandler(graypy.handler.BaseGELFHandler):
    """Forward Log messages to NTS."""

    def __init__(self, plugin):
        super(NTSLoggingHandler, self).__init__()
        self._plugin = plugin

    def make_gelf_dict(self, record):
        gelf_dict = self._make_gelf_dict(record)
        gelf_dict.update({
            'plugin_name': self._plugin.name,
            'plugin_class': self._plugin.plugin_class.__name__,
            'plugin_id': self._plugin._plugin_id
        })
        return gelf_dict

    def emit(self, record):
        gelf_dict = self.make_gelf_dict(record)
        packet = _Packet()
        packet.set(0, _Packet.packet_type_live_logs, 0)
        packet.write_string(json.dumps(gelf_dict))
        if self._plugin and self._plugin.connected:
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

    def configure_main_process(self, plugin_class):
        logging_level = logging.INFO
        if self.plugin and self.plugin.verbose:
            logging_level = logging.DEBUG

        lib_logger = logging.getLogger("nanome")
        lib_logger.setLevel(logging_level)

        # Set up logger for plugin modules
        plugin_module = plugin_class.__module__.split('.')[0]
        plugin_logger = logging.getLogger(plugin_module)
        plugin_logger.setLevel(logging_level)

        existing_handler_types = set([type(hdlr) for hdlr in lib_logger.handlers])

        self.console_handler = self.create_console_handler()
        self.log_file_handler = logging.NullHandler()
        self.nts_handler = logging.NullHandler()

        if type(self.console_handler) not in existing_handler_types:
            lib_logger.addHandler(self.console_handler)
            plugin_logger.addHandler(self.console_handler)

        if self.write_log_file and self.filename:
            self.log_file_handler = self.create_log_file_handler(self.filename)
            self.log_file_handler.setLevel(logging_level)
            if type(self.log_file_handler) not in existing_handler_types:
                lib_logger.addHandler(self.log_file_handler)
                plugin_logger.addHandler(self.log_file_handler)

        if self.remote_logging:
            self.nts_handler = self.create_nts_handler(self.plugin)
            self.nts_handler.setLevel(logging_level)
            if type(self.nts_handler) not in existing_handler_types:
                lib_logger.addHandler(self.nts_handler)
                plugin_logger.addHandler(self.nts_handler)

        # If timezone not specified, set to UTC
        if not os.environ.get('TZ'):
            os.environ['TZ'] = 'UTC'

    @staticmethod
    def configure_child_process(pipe_conn, plugin_class):
        """Set up a PipeHandler that forwards all Logs to the main Process."""
        # reset loggers on nanome-lib.
        nanome_logger = logging.getLogger("nanome")
        nanome_logger.handlers = []
        nanome_logger.setLevel(logging.DEBUG)

        # make sure plugin module is logged
        plugin_module = plugin_class.__module__.split('.')[0]
        plugin_logger = logging.getLogger(plugin_module)
        plugin_logger.handlers = []
        plugin_logger.setLevel(logging.DEBUG)

        # Pipe should send all logs to main process
        # If debug logs are disabled, they will be filtered in main process.
        pipe_handler = PipeHandler(pipe_conn)
        pipe_handler.level = logging.DEBUG

        nanome_logger.addHandler(pipe_handler)
        plugin_logger.addHandler(pipe_handler)

    @staticmethod
    def create_log_file_handler(filename):
        """Return handler that writes logs to provided filepath."""
        handler = RotatingFileHandler(filename, maxBytes=1048576, backupCount=3, delay=False)
        fmt = '%(asctime)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        return handler

    @staticmethod
    def create_nts_handler(plugin=None):
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
        record_logger = logging.getLogger(record.name)
        record_logger.handle(record)
