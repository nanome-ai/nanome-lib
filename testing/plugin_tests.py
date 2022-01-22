import argparse
import sys
import unittest

from nanome import Plugin, PluginInstance
from nanome._internal._process import _ProcessManager

if sys.version_info.major >= 3:
    from unittest.mock import MagicMock, patch
else:
    # Python 2.7 way of getting magicmock. Requires pip install mock
    from mock import MagicMock, patch


class PluginTestCase(unittest.TestCase):

    def setUp(self):
        self.plugin = Plugin('Test Plugin', 'Unit Test Plugin')
        self.plugin._network = MagicMock()
        self.plugin.set_plugin_class(PluginInstance)

    def test_create_parser(self):
        parser = Plugin.create_parser()
        self.assertTrue(isinstance(parser, argparse.ArgumentParser))

    @patch('nanome._internal._plugin._Plugin._autoreload')
    @patch('nanome._internal._plugin._Plugin._loop')
    @patch('nanome._internal._plugin.Network._NetInstance.connect')
    @patch('nanome._internal._plugin.Network._NetInstance.send')
    def test_run(self, send_mock, connect_mock, loop_mock, autoreload_mock):
        host = 'anyhost'
        port = 8000
        key = ''
        self.plugin.run(host, port, key)
        self.assertEqual(self.plugin.host, host)
        self.assertEqual(self.plugin.port, port)
        self.assertEqual(self.plugin.key, key)
        self.assertEqual(self.plugin.plugin_class, PluginInstance)
        loop_mock.assert_called_once()
        connect_mock.assert_called_with(host, port)
        send_mock.assert_called_once()

        # Test with different args set
        write_log_file = "yes"
        remote_logging = "false"
        ignore = 'fake_file.py'
        name = 'custom plugin name'
        testargs = [
            'run.py',
            '--auto-reload',
            '--write-log-file', write_log_file,
            '--remote-logging', remote_logging,
            '--ignore', ignore,
            '--name', name,
            '--verbose'
        ]
        with patch.object(sys, 'argv', testargs):
            self.plugin.run(host, port, key)
        self.assertEqual(self.plugin.write_log_file, True)
        self.assertEqual(self.plugin.remote_logging, False)
        self.assertEqual(self.plugin.to_ignore, [ignore])
        self.assertEqual(self.plugin.name, name)
        self.assertEqual(self.plugin.verbose, True)
        autoreload_mock.assert_called_once()

    @patch('nanome._internal._plugin._Plugin._loop')
    @patch('nanome._internal._plugin.Network._NetInstance')
    def test_setup(self, netinstance_mock, loop_mock):
        name = 'Test Plugin'
        description = 'Test Plugin'
        tags = []
        has_advanced = True
        self.plugin.setup(name, description, tags, has_advanced, PluginInstance)
        netinstance_mock.assert_called_once()
        loop_mock.assert_called_once()

    def test_custom_data(self):
        # Test set_custom_data()
        custom_data = "Data that may be needed inside PluginInstance"
        self.plugin.set_custom_data(custom_data)
        self.assertEqual(self.plugin._custom_data[0], custom_data)

    def test_set_maximum_processes_count(self):
        new_value = 5
        self.plugin.set_maximum_processes_count(new_value)
        self.assertEqual(_ProcessManager._max_process_count, new_value)

    def test_pre_and_post_run(self):
        def test_callback_fn():
            pass

        self.plugin.pre_run = test_callback_fn
        self.plugin.pre_run()

        self.plugin.post_run = test_callback_fn
        self.plugin.post_run()

    @patch('nanome._internal._plugin._Plugin._loop')
    @patch('nanome._internal._plugin.Network._NetInstance')
    @patch('nanome._internal._plugin.Network._NetInstance')
    def test_config_priority(self, send_mock, connect_mock, loop_mock):
        # make sure that the config priority is held in tact
        host = 'anyhost'
        port = 8000
        key = ''
        self.plugin.run(host, port, key)
        self.assertEqual(self.plugin.host, host)
        self.assertEqual(self.plugin.port, port)
        self.assertEqual(self.plugin.key, key)
        self.assertEqual(self.plugin.plugin_class, PluginInstance)

        # Test with different args set as environment variables.
        env_host = 'environ_host'
        env_port = 8001
        env_key = 'env_key12345'
        environ_dict = {
            'NTS_HOST': env_host,
            'NTS_PORT': str(env_port),
            'NTS_KEYFILE': env_key
        }
        with patch.dict('os.environ', environ_dict):
            self.plugin.run()
            self.assertEqual(self.plugin.host, env_host)
            self.assertEqual(self.plugin.port, env_port)
            self.assertEqual(self.plugin.key, env_key)

        # # Test with different args set
        # write_log_file = "True"
        # ignore = 'fake_file.py'
        # name = 'custom plugin name'
        # testargs = [
        #     'run.py',
        #     '--auto-reload',
        #     '--write-log-file', write_log_file,
        #     '--ignore', ignore,
        #     '--name', name,
        #     '--verbose'
        # ]
        # with patch.object(sys, 'argv', testargs):
        #     self.plugin.run(host, port, key)
        # self.assertEqual(self.plugin.write_log_file, True)
        # self.assertEqual(self.plugin.to_ignore, [ignore])
        # self.assertEqual(self.plugin.name, name)
        # self.assertEqual(self.plugin.verbose, True)
        # autoreload_mock.assert_called_once()
