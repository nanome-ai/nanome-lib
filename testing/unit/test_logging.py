import logging
import sys
import unittest

from nanome import Plugin, PluginInstance
from nanome.util import Logs

if sys.version_info.major >= 3:
    from unittest.mock import MagicMock, patch
else:
    # Python 2.7 way of getting magicmock. Requires pip install mock
    from mock import MagicMock, patch

import collections
import logging


class _BaseTestCaseContext(object):

    def __init__(self, test_case):
        self.test_case = test_case


__all__ = ['_LoggingWatcher', '_BaseTestCaseContext', '_CapturingHandler', '_AssertLogsContext']


class Py2AssertLogs(object):
    """Py2 compatible version of unittest.Testcase.assertLogs"""

    def __init__(self, *args, **kwargs):
        super(Py2AssertLogs, self).__init__(*args, **kwargs)
        if sys.version_info.major < 3:
            self.assertLogs = self._assertLogs

    def _assertLogs(self, logger=None, level=None):
        "Py2 compatible version of self.assertLogs"
        return _AssertLogsContext(self, logger, level)


class PluginLoggingTestCase(Py2AssertLogs, unittest.TestCase):

    def setUp(self):
        self.plugin = Plugin('Test Plugin', 'Unit Test Plugin')
        self.plugin.set_plugin_class(PluginInstance)

        self.host = 'anyhost'
        self.port = 8000
        self.key = ''

        # Make it so that Logs logged in this module are handled the same as "nanome"
        testing_logger = logging.getLogger(__name__)
        nanome_logger = logging.getLogger('nanome')
        testing_logger.handlers = nanome_logger.handlers
        testing_logger.setLevel(logging.INFO)
        nanome_logger.setLevel(logging.WARNING)

        # Hides noisy "Starting Plugin" output
        logging.getLogger('nanome.api.plugin.Plugin.run').setLevel(logging.ERROR)

    @classmethod
    def tearDownClass(cls):
        # Make sure remote logging always off after test.
        # Without this teardown, logging configs persist to tests run after this.
        super(PluginLoggingTestCase, cls).tearDownClass()
        nanome_logger = logging.getLogger("nanome")
        testing_logger = logging.getLogger(__name__)
        nanome_logger.handlers = []
        testing_logger.handlers = []

    @patch('nanome.api.Plugin._run')
    @patch('nanome._internal.network.NetInstance')
    @patch('nanome._internal.logs.NTSLoggingHandler.handle')
    def test_nts_handler_called(self, handle_mock, *args):
        """Assert logs get forwarded to NTS."""
        remote_logging = "True"
        testargs = [
            'run.py',
            '--remote-logging', remote_logging
        ]

        with patch.object(sys, 'argv', testargs):
            self.plugin.run(self.host, self.port, self.key)

        # Write log, and make sure NTSLogging Handler called.
        Logs.message('This should be forwarded to NTS.')
        handle_mock.assert_called()

    @patch('nanome.api.Plugin._run')
    @patch('nanome._internal.network.NetInstance')
    @patch('nanome._internal.logs.NTSLoggingHandler.handle')
    def test_nts_handler_not_called(self, *args):
        """Assert logs don't get forwarded to NTS if remote-logging is False."""
        remote_logging = False

        testargs = [
            'run.py',
            '--remote-logging', remote_logging
        ]
        with patch.object(sys, 'argv', testargs):
            self.plugin.run(self.host, self.port, self.key)

        # Write log, and make sure NTSLogging Handler not called.
        Logs.message('This should not be forwarded to NTS.')

        # log_file_handler should be called, but set to NullHandler
        nts_handler = self.plugin._logs_manager.nts_handler
        self.assertTrue(isinstance(nts_handler, logging.NullHandler))

    @patch('nanome.api.Plugin._run')
    @patch('nanome._internal.network.NetInstance')
    def test_file_handler_called(self, *args):
        """Assert if write_log_file is True, the log_file_handler is utilized."""
        write_log_file = "True"
        testargs = [
            'run.py',
            '--write-log-file', write_log_file,
        ]
        with patch.object(sys, 'argv', testargs):
            self.plugin.run(self.host, self.port, self.key)

        # Write log, and make sure log_file_handler is called.
        logger = logging.getLogger(__name__)
        active_rfh = [
            h for h in logger.handlers
            if isinstance(h, logging.handlers.RotatingFileHandler)
        ][0]
        active_rfh.handle = MagicMock()
        Logs.message('Log file handler should be called.')
        active_rfh.handle.assert_called()

    @patch('nanome.api.Plugin._run')
    @patch('nanome._internal.network.NetInstance')
    def test_file_handler_not_called(self, *args):
        """Assert if write_log_file is False, the log_file_handler is not utilized."""
        write_log_file = False
        testargs = [
            'run.py',
            '--write-log-file', write_log_file,
        ]
        with patch.object(sys, 'argv', testargs):
            self.plugin.run(self.host, self.port, self.key)

        self.plugin._logs_manager.log_file_handler.handle = MagicMock()
        Logs.message('Log file should not be called')

    @patch('nanome.api.Plugin._loop')
    @patch('nanome._internal.network.NetInstance.connect')
    @patch('nanome._internal.network.NetInstance.send')
    def test_nts_logger_handler(self, send_mock, *args):
        """Ensure NTSLoggingHandler.handle() triggers a network request."""
        with patch.object(sys, 'argv', ['run.py', '--remote-logging', 'True']):
            self.plugin.run(self.host, self.port, self.key)
        send_mock.assert_called()

    @patch('nanome.api.Plugin._run')
    @patch('nanome._internal.network.NetInstance')
    def test_console_handler_called(self, *args):
        """Assert logs are always logged to the console."""
        testargs = [
            'run.py',
            '--remote-logging', False,
            '--write-log-file', False
        ]

        with patch.object(sys, 'argv', testargs):
            self.plugin.run(self.host, self.port, self.key)
            logger = logging.getLogger(__name__)
            console_handler = [
                h for h in logger.handlers
                if isinstance(h, logging.StreamHandler)
            ][0]
            console_handler.handle = MagicMock()
            Logs.message("Should be printed to console")
            console_handler.handle.assert_called()


class LogUtilTestCase(Py2AssertLogs, unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def test_log_warning(self):
        with self.assertLogs(self.logger, logging.WARNING) as captured:
            message = "This is a warning"
            Logs.warning(message)
            self.assertEqual(len(captured.records), 1)
            self.assertEqual(captured.records[0].getMessage(), message)

    def test_log_error(self):
        with self.assertLogs(self.logger, logging.ERROR) as captured:
            message = "This is an error"
            Logs.error(message)
            self.assertEqual(len(captured.records), 1)
            self.assertEqual(captured.records[0].getMessage(), message)

    def test_log_debug(self):
        with self.assertLogs(self.logger, logging.DEBUG) as captured:
            message = "This is a debug message"
            Logs.debug(message)
            self.assertEqual(len(captured.records), 1)
            self.assertEqual(captured.records[0].getMessage(), message)

    def test_log_message(self):
        with self.assertLogs(self.logger, logging.INFO) as captured:
            message = "This is a regular messge"
            Logs.message(message)
            self.assertEqual(len(captured.records), 1)
            self.assertEqual(captured.records[0].getMessage(), message)


_LoggingWatcher = collections.namedtuple("_LoggingWatcher", ["records", "output"])


class _BaseTestCaseContext(object):

    def __init__(self, test_case):
        self.test_case = test_case

    def _raiseFailure(self, standardMsg):
        msg = self.test_case._formatMessage(self.msg, standardMsg)
        raise self.test_case.failureException(msg)


class _CapturingHandler(logging.Handler):
    """
    A logging handler capturing all (raw and formatted) logging output.
    """

    def __init__(self):
        logging.Handler.__init__(self)
        self.watcher = _LoggingWatcher([], [])

    def flush(self):
        pass

    def emit(self, record):
        self.watcher.records.append(record)
        msg = self.format(record)
        self.watcher.output.append(msg)


class _AssertLogsContext(_BaseTestCaseContext):
    """A context manager used to implement TestCase.assertLogs()."""

    LOGGING_FORMAT = "%(levelname)s:%(name)s:%(message)s"

    def __init__(self, test_case, logger_name, level):
        _BaseTestCaseContext.__init__(self, test_case)
        self.logger_name = logger_name
        if level:
            self.level = logging._levelNames.get(level, level)
        else:
            self.level = logging.INFO
        self.msg = None

    def __enter__(self):
        if isinstance(self.logger_name, logging.Logger):
            logger = self.logger = self.logger_name
        else:
            logger = self.logger = logging.getLogger(self.logger_name)
        formatter = logging.Formatter(self.LOGGING_FORMAT)
        handler = _CapturingHandler()
        handler.setFormatter(formatter)
        self.watcher = handler.watcher
        self.old_handlers = logger.handlers[:]
        self.old_level = logger.level
        self.old_propagate = logger.propagate
        logger.handlers = [handler]
        logger.setLevel(self.level)
        logger.propagate = False
        return handler.watcher

    def __exit__(self, exc_type, exc_value, tb):
        self.logger.handlers = self.old_handlers
        self.logger.propagate = self.old_propagate
        self.logger.setLevel(self.old_level)
        if exc_type is not None:
            # let unexpected exceptions pass through
            return False
        if len(self.watcher.records) == 0:
            self._raiseFailure(
                "no logs of level {} or higher triggered on {}"
                .format(logging.getLevelName(self.level), self.logger.name))
