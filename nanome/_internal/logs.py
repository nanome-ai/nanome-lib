import json
import logging
import os
import sys
import graypy
from logging.handlers import RotatingFileHandler
from multiprocessing import Pipe

from nanome._internal._network import _Packet
from tblib import pickling_support

pickling_support.install()

logger = logging.getLogger(__name__)


class PipeHandler(logging.Handler):
    """Send log records through pipe to main process.

    Resolves issues with logging from multiple processes.
    Also stores presenter info from PluginInstance, and adds to Logs before piping.
    """

    def __init__(self, plugin_instance):
        super(PipeHandler, self).__init__()
        self.pipe_conn = plugin_instance._log_pipe_conn
        self.org_name = None
        self.org_id = None
        self.account_id = None
        self.account_name = None
        self.set_presenter_info(plugin_instance)

    def handle(self, record):
        # Add account and org info to record
        record.__dict__.update({
            'org_name': self.org_name,
            'org_id': self.org_id,
            'user_id': self.account_id,
            'username': self.account_name,
        })
        super(PipeHandler, self).handle(record)

    def emit(self, record):
        try:
            self.pipe_conn.send(record)
        except BrokenPipeError:
            # Connection has been closed.
            pass

    def set_presenter_info(self, plugin_instance):
        """Get presenter info from plugin instance and store on handler."""
        plugin_instance.request_presenter_info(self._presenter_info_callback)

    def _presenter_info_callback(self, info):
        self.org_id = info.org_id
        self.org_name = info.org_name
        self.account_id = info.account_id
        self.account_name = info.account_name


class NTSLoggingHandler(graypy.handler.BaseGELFHandler):
    """Forward Log messages to NTS."""

    def __init__(self, plugin):
        super(NTSLoggingHandler, self).__init__()
        self._plugin = plugin

    def handle(self, record):
        # Add extra fields to the record.
        record.__dict__.update({
            'plugin_name': self._plugin.name,
            'plugin_class': self._plugin.plugin_class.__name__,
            'plugin_id': self._plugin._plugin_id,
            'nts_host': self._plugin.host,
            'source_type': 'Plugin',
            'version': self._plugin.version
        })
        return super(NTSLoggingHandler, self).handle(record)

    def emit(self, record):
        gelf_dict = self._make_gelf_dict(record)
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

    The LogsManager running in the main process has 2 pipe connections:
    main_pipe_conn and child_pipe_conn.

    When a child process is created, the child_pipe_conn is passed to the child process.
    The child process then uses a PipeHandler to send log records through the pipe to
    the main process.
    """

    def __init__(self, filename=None, plugin=None, write_log_file=True, remote_logging=False):
        self.filename = filename or ''
        self.plugin = plugin
        self.write_log_file = write_log_file
        self.remote_logging = remote_logging
        self.main_pipe_conn = None
        self.child_pipe_conn = None

    def configure_main_process(self, plugin_class):
        self.main_pipe_conn, self.child_pipe_conn = Pipe()
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
        self.console_handler.setLevel(logging_level)
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
    def configure_child_process(plugin_instance):
        """Set up a PipeHandler that forwards all Logs to the main Process."""
        # reset loggers on nanome-lib.
        nanome_logger = logging.getLogger("nanome")
        nanome_logger.handlers = []
        nanome_logger.setLevel(logging.DEBUG)

        # make sure plugin module is logged
        plugin_module = plugin_instance.__class__.__module__.split('.')[0]
        plugin_logger = logging.getLogger(plugin_module)
        plugin_logger.handlers = []
        plugin_logger.setLevel(logging.DEBUG)

        # Pipe should send all logs to main process
        # If debug logs are disabled, they will be filtered in main process.
        pipe_handler = PipeHandler(plugin_instance)
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

    def poll_for_logs(self):
        has_data = self.main_pipe_conn.poll()
        if has_data:
            record = self.main_pipe_conn.recv()
            record_logger = logging.getLogger(record.name)
            record_logger.handle(record)
