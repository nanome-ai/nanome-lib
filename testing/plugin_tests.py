import argparse
import sys
import unittest

from nanome import Plugin, PluginInstance

if sys.version_info.major >= 3:
    from unittest.mock import MagicMock
else:
    # Python 2.7 way of getting magicmock. Requires pip install mock
    from mock import MagicMock


class PluginTestCase(unittest.TestCase):

    def setUp(self):
        self.plugin = Plugin('Test Plugin', 'Unit Test Plugin')
        self.plugin._network = MagicMock()
        self.plugin_instance = PluginInstance()
        self.plugin.set_plugin_class(PluginInstance)

    def test_create_parser(self):
        parser = Plugin.create_parser()
        self.assertTrue(isinstance(parser, argparse.ArgumentParser))

    @unittest.mock.patch('nanome._internal._plugin.Network')
    def test_run(self, plugin_mock):
        host = 'anyhost'
        port = 8000
        key = ''
        self.plugin._plugin._loop = MagicMock()
        self.plugin.run(host, port, key)

        # Test code paths with args set
        testargs = [
            'run.py',
            '--auto-reload',
            '--write-log-file', "True",
            '--ignore', 'fake_file.py',
            '--name', 'custom plugin name'
        ]
        self.plugin._plugin._autoreload = MagicMock()
        with unittest.mock.patch.object(sys, 'argv', testargs):
            self.plugin.run(host, port, key)

    @unittest.mock.patch('nanome._internal._plugin.Network')
    @unittest.mock.patch('nanome._internal._plugin._Plugin._loop')
    def test_setup(self, plugin_mock, loop_mock):
        name = 'Test Plugin'
        description = 'Test Plugin'
        tags = []
        has_advanced = True
        plugin_class = MagicMock()
        plugin_class.__name__ = 'Test PluginInstance'
        self.plugin.setup(name, description, tags, has_advanced, plugin_class)
