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
        # self.plugin._network = MagicMock()
        self.plugin_instance = PluginInstance()
        # self.plugin_instance._network = MagicMock()
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

        testargs = ['run.py', '--auto-reload']
        self.plugin._plugin._autoreload = MagicMock()
        with unittest.mock.patch.object(sys, 'argv', testargs):
            self.plugin.run(host, port, key)

