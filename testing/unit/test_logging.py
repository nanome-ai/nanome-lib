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


class PluginLoggingTestCase(unittest.TestCase):

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

    @patch('nanome._internal._plugin._Plugin._run')
    @patch('nanome._internal._plugin.Network._NetInstance')
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

    @patch('nanome._internal._plugin._Plugin._run')
    @patch('nanome._internal._plugin.Network._NetInstance')
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

    @patch('nanome._internal._plugin._Plugin._run')
    @patch('nanome._internal._plugin.Network._NetInstance')
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
        self.plugin._logs_manager.log_file_handler.handle = MagicMock()
        Logs.message('Log file handler should be called.')
        self.plugin._logs_manager.log_file_handler.handle.assert_called()

    @patch('nanome._internal._plugin._Plugin._run')
    @patch('nanome._internal._plugin.Network._NetInstance')
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

    @patch('nanome._internal._plugin._Plugin._loop')
    @patch('nanome._internal._plugin.Network._NetInstance.connect')
    @patch('nanome._internal._plugin.Network._NetInstance.send')
    def test_nts_logger_handler(self, send_mock, *args):
        """Ensure NTSLoggingHandler.handle() triggers a network request."""
        with patch.object(sys, 'argv', ['run.py', '--remote-logging', 'True']):
            self.plugin.run(self.host, self.port, self.key)
        send_mock.assert_called()

    @patch('nanome._internal._plugin._Plugin._run')
    @patch('nanome._internal._plugin.Network._NetInstance')
    def test_console_handler_called(self, *args):
        """Assert logs are always logged to the console."""
        testargs = [
            'run.py',
            '--remote-logging', False,
            '--write-log-file', False
        ]

        with patch.object(sys, 'argv', testargs):
            self.plugin.run(self.host, self.port, self.key)
            console_handler = self.plugin._logs_manager.console_handler
            with patch.object(console_handler, 'handle') as handle_mock:
                Logs.message("Should be printed to console")
                handle_mock.assert_called()


class LogUtilTestCase(unittest.TestCase):

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
