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


class LoggingTestCase(unittest.TestCase):

    def setUp(self):
        self.plugin = Plugin('Test Plugin', 'Unit Test Plugin')
        self.plugin.set_plugin_class(PluginInstance)

        self.host = 'anyhost'
        self.port = 8000
        self.key = ''

    @patch('nanome._internal._plugin._Plugin._loop')
    @patch('nanome._internal._plugin.Network._NetInstance')
    @patch('nanome._internal._process._logs_manager.NTSLoggingHandler.handle')
    def test_nts_handler_called(self, handle_mock, netinstance_mock, loop_mock):
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
        self.plugin._logs_manager.update()
        handle_mock.assert_called()

    @patch('nanome._internal._plugin._Plugin._loop')
    @patch('nanome._internal._plugin.Network._NetInstance')
    @patch('nanome._internal._process._logs_manager.NTSLoggingHandler.handle')
    def test_nts_handler_not_called(self, handle_mock, netinstance_mock, loop_mock):
        """Assert logs don't get forwarded to NTS if remote-logging is False."""
        remote_logging = False

        testargs = [
            'run.py',
            '--remote-logging', remote_logging
        ]
        with patch.object(sys, 'argv', testargs):
            self.plugin.run(self.host, self.port, self.key)

        # Write log, and make sure NTSLogging Handler not called.
        Logs.message('This should be forwarded to NTS.')
        self.plugin._logs_manager.update()

        # log_file_handler should be called, but set to NullHandler
        nts_handler = self.plugin._logs_manager.nts_handler
        self.assertTrue(isinstance(nts_handler, logging.NullHandler))

    @patch('nanome._internal._plugin._Plugin._loop')
    @patch('nanome._internal._plugin.Network._NetInstance')
    def test_file_handler_called(self, netinstance_mock, loop_mock):
        """Assert if write_log_file is True, the file logger is utilized."""
        write_log_file = "True"
        testargs = [
            'run.py',
            '--write-log-file', write_log_file,
        ]
        with patch.object(sys, 'argv', testargs):
            self.plugin.run(self.host, self.port, self.key)

        self.plugin._logs_manager.log_file_handler.handle = MagicMock()
        # Write log, and make sure File logger called.
        Logs.message('Log file handler should be called.')
        self.plugin._logs_manager.update()
        self.plugin._logs_manager.log_file_handler.handle.assert_called()

    @patch('nanome._internal._plugin._Plugin._loop')
    @patch('nanome._internal._plugin.Network._NetInstance')
    def test_file_handler_not_called(self, netinstance_mock, loop_mock):
        """Assert if write_log_file is False, the file logger is not utilized."""
        write_log_file = False
        testargs = [
            'run.py',
            '--write-log-file', write_log_file,
        ]
        with patch.object(sys, 'argv', testargs):
            self.plugin.run(self.host, self.port, self.key)

        self.plugin._logs_manager.log_file_handler.handle = MagicMock()
        Logs.message('Log file should not be called')
        self.plugin._logs_manager.update()

        # log_file_handler should be called, but set to NullHandler
        log_file_handler = self.plugin._logs_manager.log_file_handler
        log_file_handler.handle.assert_called()
        self.assertTrue(isinstance(log_file_handler, logging.NullHandler))

    @patch('nanome._internal._plugin._Plugin._loop')
    @patch('nanome._internal._plugin.Network._NetInstance.connect')
    @patch('nanome._internal._plugin.Network._NetInstance.send')
    def test_nts_logger_handler(self, send_mock, connect_mock, loop_mock):
        """Ensure NTSLoggingHandler.handle() triggers a network request."""

        with patch.object(sys, 'argv', ['run.py', '--remote-logging', 'True']):
            self.plugin.run(self.host, self.port, self.key)

        # Add fresh patch, and make sure network send is called during log update.
        Logs.message("Test!")
        with patch('nanome._internal._plugin.Network._NetInstance.send') as network_patch:
            self.plugin._logs_manager.update()
            network_patch.assert_called()

    @patch('nanome._internal._plugin._Plugin._loop')
    @patch('nanome._internal._plugin.Network._NetInstance.connect')
    @patch('nanome._internal._plugin.Network._NetInstance.send')
    def test_warnings(self, send_mock, connect_mock, loop_mock):

        with patch.object(sys, 'argv', ['run.py', '--remote-logging', 'True', '--write-log-file', 'True']):
            self.plugin.run(self.host, self.port, self.key)

        Logs.warning("This is a warning")
        self.plugin._logs_manager.update()
