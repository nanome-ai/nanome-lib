import argparse
import sys
import unittest

from nanome import Plugin, PluginInstance
from nanome._internal._process import _ProcessManager

if sys.version_info.major >= 3:
    from unittest.mock import MagicMock
else:
    # Python 2.7 way of getting magicmock. Requires pip install mock
    from mock import MagicMock


class PluginTestCase(unittest.TestCase):

    def setUp(self):
        self.plugin = Plugin('Test Plugin', 'Unit Test Plugin')
        self.plugin._network = MagicMock()
        self.plugin.set_plugin_class(PluginInstance)

    def test_create_parser(self):
        parser = Plugin.create_parser()
        self.assertTrue(isinstance(parser, argparse.ArgumentParser))

    @unittest.mock.patch('nanome._internal._plugin.Network')
    @unittest.mock.patch('nanome._internal._plugin._Plugin._loop')
    @unittest.mock.patch('nanome._internal._plugin._Plugin._autoreload')
    def test_run(self, network_mock, loop_mock, autoreload_mock):
        host = 'anyhost'
        port = 8000
        key = ''
        self.plugin.run(host, port, key)
        self.assertEqual(self.plugin.host, host)
        self.assertEqual(self.plugin.port, port)
        self.assertEqual(self.plugin.key, key)
        self.assertEqual(self.plugin.plugin_class, PluginInstance)

        # Test with different args set
        write_log_file = "True"
        ignore = 'fake_file.py'
        name = 'custom plugin name'
        testargs = [
            'run.py',
            '--auto-reload',
            '--write-log-file', write_log_file,
            '--ignore', ignore,
            '--name', name,
            '--verbose'
        ]
        self.plugin._plugin._autoreload = MagicMock()
        with unittest.mock.patch.object(sys, 'argv', testargs):
            self.plugin.run(host, port, key)
        self.assertEqual(self.plugin.write_log_file, True)
        self.assertEqual(self.plugin.to_ignore, [ignore])
        self.assertEqual(self.plugin.name, name)
        self.assertEqual(self.plugin.has_verbose, True)

    @unittest.mock.patch('nanome._internal._plugin.Network')
    @unittest.mock.patch('nanome._internal._plugin._Plugin._loop')
    def test_setup(self, network_mock, loop_mock):
        name = 'Test Plugin'
        description = 'Test Plugin'
        tags = []
        has_advanced = True
        self.plugin.setup(name, description, tags, has_advanced, PluginInstance)

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
            # Set this for the various pre/post functions
            pass

        self.plugin.pre_run = test_callback_fn
        self.plugin.pre_run()

        self.plugin.post_run = test_callback_fn
        self.plugin.post_run()
