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
    def test_log_manager(self, netinstance_mock, loop_mock):
        host = 'anyhost'
        port = 8000
        key = ''

        # Set write_log_file to False, and verify LogsManager is still created.
        write_log_file = 0
        testargs = [
            'run.py',
            '--write-log-file', write_log_file,
        ]
        with patch.object(sys, 'argv', testargs):
            self.plugin.run(host, port, key)
        self.assertEqual(self.plugin.write_log_file, False)
        self.assertTrue(isinstance(self.plugin._logs_manager, _LogsManager))

        # Set write_log_file to True, and verify LogsManager is still created.
        write_log_file = "True"
        testargs = [
            'run.py',
            '--write-log-file', write_log_file,
        ]
        with patch.object(sys, 'argv', testargs):
            self.plugin.run(host, port, key)
        self.assertEqual(self.plugin.write_log_file, True)
        self.assertTrue(isinstance(self.plugin._logs_manager, _LogsManager))

    @patch('nanome._internal._plugin._Plugin._loop')
    @patch('nanome._internal._plugin.Network._NetInstance')
    @patch('nanome._internal._process._logs_manager.NTSLoggingHandler.handle')
    def test_nts_handler_called(self, handle_mock, netinstance_mock, loop_mock):
        """Assert logs get forwarded to NTS."""
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

        # Write log, and make sure NTSLogging Handler called.
        Logs.message('Test message')
        # Test that NTSLoggingHandler used when updating logs.
        self.plugin._logs_manager.update()
        handle_mock.assert_called()
        logger_mock.assert_called()
