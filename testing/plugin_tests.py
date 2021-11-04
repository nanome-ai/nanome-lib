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
        self.plugin_instance._network = MagicMock()
        self.plugin.set_plugin_class(PluginInstance)

    def test_create_parser(self):
        parser = Plugin.create_parser()
        self.assertTrue(isinstance(parser, argparse.ArgumentParser))

    @unittest.mock.patch('nanome._internal._plugin.Network')
    # @unittest.mock.patch('nanome._internal._plugin.Network')
    def test_run(self, mock):
        host = 'anyhost'
        port = 8000
        key = ''
        import multiprocessing, time
        p = multiprocessing.Process(target=self.plugin.run, args=(host, port, key))
        p.start()
        time.sleep(2)
        p.terminate()
        p.join()
