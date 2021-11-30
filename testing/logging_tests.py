import sys
import unittest

from nanome import Plugin, PluginInstance
from nanome._internal._process._logs_manager import _LogsManager
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

    @patch('nanome._internal._plugin._Plugin._loop')
    @patch('nanome._internal._plugin.Network._NetInstance')
    @patch('nanome._internal._process._logs_manager.NTSLoggingHandler.handle')
    def test_nts_handler_called(self, handle_mock, netinstance_mock, loop_mock):
        """Assert logs get forwarded to NTS."""
        remote_logging = "True"
        host = 'anyhost'
        port = 8000
        key = ''

        testargs = [
            'run.py',
            '--remote-logging', remote_logging
        ]

        with patch.object(sys, 'argv', testargs):
            self.plugin.run(host, port, key)

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
        host = 'anyhost'
        port = 8000
        key = ''

        testargs = [
            'run.py',
            '--remote-logging', remote_logging
        ]
        with patch.object(sys, 'argv', testargs):
            self.plugin.run(host, port, key)

        # Write log, and make sure NTSLogging Handler not called.
        Logs.message('This should be forwarded to NTS.')
        self.plugin._logs_manager.update()
        handle_mock.assert_not_called()

    @patch('nanome._internal._plugin._Plugin._loop')
    @patch('nanome._internal._plugin.Network._NetInstance')
    def test_file_logger_called(self, netinstance_mock, loop_mock):
        """Assert if write_log_file is True, the file logger is utilized."""
        write_log_file = "True"
        host = 'anyhost'
        port = 8000
        key = ''

        testargs = [
            'run.py',
            '--write-log-file', write_log_file,
        ]
        with patch.object(sys, 'argv', testargs):
            self.plugin.run(host, port, key)

        self.plugin._logs_manager.file_logger.info = MagicMock()
        # Write log, and make sure File logger called.
        Logs.message('Test message')
        self.plugin._logs_manager.update()
        self.plugin._logs_manager.file_logger.info.assert_called()

    @patch('nanome._internal._plugin._Plugin._loop')
    @patch('nanome._internal._plugin.Network._NetInstance')
    def test_file_logger_not_called(self, netinstance_mock, loop_mock):
        """Assert if write_log_file is False, the file logger is not utilized."""
        write_log_file = False
        host = 'anyhost'
        port = 8000
        key = ''

        testargs = [
            'run.py',
            '--write-log-file', write_log_file,
        ]
        with patch.object(sys, 'argv', testargs):
            self.plugin.run(host, port, key)

        self.plugin._logs_manager.file_logger.info = MagicMock()
        Logs.message('Test message')
        self.plugin._logs_manager.update()
        self.plugin._logs_manager.file_logger.info.assert_not_called()

    @patch('nanome._internal._plugin._Plugin._loop')
    @patch('nanome._internal._plugin.Network._NetInstance.connect')
    @patch('nanome._internal._plugin.Network._NetInstance.send')
    def test_nts_logger_handler(self, send_mock, connect_mock, loop_mock):
        """Ensure NTSLoggingHandler.handle() triggers a network request."""
        host = 'anyhost'
        port = 8000
        key = ''

        with patch.object(sys, 'argv', ['run.py', '--remote-logging', 'True']):
            self.plugin.run(host, port, key)

        # Add fresh patch, and make sure network send is called during log update.
        Logs.message("Test!")
        with patch('nanome._internal._plugin.Network._NetInstance.send') as network_patch:
            self.plugin._logs_manager.update()
            network_patch.assert_called()
