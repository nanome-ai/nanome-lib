import argparse
from distutils.util import strtobool
import sys
import unittest

from nanome import Plugin, PluginInstance
from nanome._internal._process import ProcessManager
from nanome.util import config

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
        # Store original config values and reset on tearDown
        # We don't want tests changing the configs permanently
        self.original_config_host = config.fetch('host')
        self.original_config_port = config.fetch('port')
        self.original_config_key = config.fetch('key')

    def tearDown(self):
        config.set('host', self.original_config_host)
        config.set('port', self.original_config_port)
        config.set('key', self.original_config_key)
        super(PluginTestCase, self).tearDown()

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

        config.set('host', 'anyhost')
        config.set('port', 8000)
        config.set('key', 'abcdefg1234')
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
        self.assertEqual(ProcessManager._max_process_count, new_value)

    def test_pre_and_post_run(self):
        def test_callback_fn():
            pass

        self.plugin.pre_run = test_callback_fn
        self.plugin.pre_run()

        self.plugin.post_run = test_callback_fn
        self.plugin.post_run()

    @patch('nanome._internal._plugin._Plugin._loop')
    @patch('nanome._internal._plugin.Network._NetInstance')
    @patch('nanome._internal._plugin._Plugin._autoreload')
    def test_config_priority(self, *args):
        """Validate order of priority for plugin settings.

        Order of priority for settings:
        1. First, parameters to run() function are checked
        2) Then CLI args are checked.
        3) Then environment variables.
        4) Finally, fall back on config file.
        """
        # Lowest priority: nanome.util.config config file.
        config_host = 'config_host'
        config_port = 8000
        config_key = 'config_key54321'
        config.set('host', config_host)
        config.set('port', config_port)
        config.set('key', config_key)

        self.plugin.run()
        self.assertEqual(self.plugin.host, config_host)
        self.assertEqual(self.plugin.port, config_port)
        self.assertEqual(self.plugin.key, config_key)

        # Environment variables should take precedent over config file.
        env_host = 'environ_host'
        env_port = '8001'
        env_key = 'environ_key12345'
        env_name = "Environment Name"
        env_verbose = 'True'
        env_write_log_file = 'False'
        env_remote_logging = 'False'
        env_auto_reload = 'True'
        env_ignore = '/app/fakefile1,/app/fakefile2'

        environ_dict = {
            'NTS_HOST': env_host,
            'NTS_PORT': env_port,
            'NTS_KEY': env_key,
            'PLUGIN_NAME': env_name,
            'PLUGIN_VERBOSE': env_verbose,
            'PLUGIN_WRITE_LOG_FILE': env_write_log_file,
            'PLUGIN_REMOTE_LOGGING': env_remote_logging,
            'PLUGIN_AUTO_RELOAD': env_auto_reload,
            'PLUGIN_IGNORE': env_ignore
        }

        with patch.dict('os.environ', environ_dict):
            self.plugin.run()

        self.assertEqual(self.plugin.host, env_host)
        self.assertEqual(self.plugin.port, int(env_port))
        self.assertEqual(self.plugin.key, env_key)
        self.assertEqual(self.plugin.name, env_name)
        self.assertEqual(self.plugin.verbose, bool(strtobool(env_verbose)))
        self.assertEqual(self.plugin.write_log_file, bool(strtobool(env_write_log_file)))
        self.assertEqual(self.plugin.remote_logging, bool(strtobool(env_remote_logging)))
        self.assertEqual(self.plugin.write_log_file, bool(strtobool(env_write_log_file)))
        self.assertEqual(self.plugin.has_autoreload, bool(strtobool(env_auto_reload)))
        self.assertEqual(self.plugin.to_ignore, env_ignore.split(','))

        # CLI args should take precedent over environment variables.
        cli_host = 'cli_host'
        cli_port = 8003
        cli_key = 'cli_key12345'
        cli_write_log_file = 'false'
        cli_name = 'cli-plugin-name'
        cli_ignore = 'cli_ignore.py'
        cli_remote_logging = 'y'
        testargs = [
            'run.py',
            '--write-log-file', cli_write_log_file,
            '--ignore', cli_ignore,
            '--name', cli_name,
            '--key', cli_key,
            '--verbose',
            '-a', cli_host,
            '-p', str(cli_port),
            '--remote-logging', cli_remote_logging
        ]
        with patch.object(sys, 'argv', testargs), patch.dict('os.environ', environ_dict):
            self.plugin.run()
        self.assertEqual(self.plugin.write_log_file, False)
        self.assertEqual(self.plugin.to_ignore, [cli_ignore])
        self.assertEqual(self.plugin.name, cli_name)
        self.assertEqual(self.plugin.verbose, True)
        self.assertEqual(self.plugin.remote_logging, True)

        # fn parameters take precedent over everything
        kwarg_host = 'anyhost'
        kwarg_port = 8000
        kwarg_key = ''
        with patch.dict('os.environ', environ_dict), patch.object(sys, 'argv', testargs):
            self.plugin.run(kwarg_host, kwarg_port, kwarg_key)
            self.assertEqual(self.plugin.host, kwarg_host)
            self.assertEqual(self.plugin.port, kwarg_port)
            self.assertEqual(self.plugin.key, kwarg_key)
