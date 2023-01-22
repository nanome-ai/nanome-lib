import json
import os
import sys
import unittest

if sys.version_info.major >= 3:
    from unittest.mock import MagicMock
else:
    # Python 2.7 way of getting magicmock. Requires pip install mock
    from mock import MagicMock

from nanome._internal.logs import LogsManager
from nanome.api.serializers import CommandMessageSerializer
from nanome._internal.enums import Messages
from nanome._internal.network import PluginNetwork

test_assets = os.getcwd() + ("/testing/test_assets")


class PluginNetworkTestCase(unittest.TestCase):

    def setUp(self):
        version_table_file = os.path.join(test_assets, "version_table_1_24_2.json")
        with open(version_table_file, 'r') as f:
            self.version_table = json.load(f)

        self.plugin = MagicMock()
        # Mock args that are passed to setup plugin instance networking
        self.session_id = self.plugin_network = self.queue_in = self.queue_out = \
            self.log_pipe_conn = self.original_version_table = self.permissions = MagicMock()
        self.serializer = CommandMessageSerializer()
        plugin_id = 123
        self.network = PluginNetwork(
            self.plugin, self.session_id, self.queue_in, self.queue_out, self.serializer,
            plugin_id, self.version_table)

    def test_on_run(self):
        self.network._on_run()
        self.plugin.on_run.assert_called_once()

    def test_on_advanced_settings(self):
        self.network.on_advanced_settings()
        self.plugin.on_advanced_settings.assert_called_once()

    def test_on_complex_added(self):
        self.network.on_complex_added()
        self.plugin.on_complex_added.assert_called_once()
        self.plugin.on_complex_list_changed.assert_called_once()

    def test_on_presenter_change(self):
        LogsManager.configure_child_process = MagicMock()
        self.network._on_presenter_change()
        self.plugin.on_presenter_change.assert_called_once()
        LogsManager.configure_child_process.assert_called_once()

    def test_call(self):
        request_id = 1
        self.network._call(request_id)
        self.plugin._call.assert_called_once()

    def test_close(self):
        self.network._close()
        self.network._queue_out.close.assert_called_once()

    def test_send(self):
        code = Messages.complex_list_request
        arg = []
        expects_response = True
        starting_command_id = self.network._command_id
        self.network.send(code, arg, expects_response)
        self.assertEqual(self.network._command_id, starting_command_id + 1)
        self.network._queue_out.put.assert_called_once()

    def test_receive(self):
        bytes_file = os.path.join(test_assets, "ReceiveWorkspaceMessage.bin")
        with open(bytes_file, 'rb') as f:
            payload = f.read()
        self.network._queue_in.empty = MagicMock(return_value=False)
        self.network._queue_in.get = MagicMock(return_value=payload)
        self.network._receive()
        self.network._queue_in.get.assert_called_once()
        # Simple callback should trigger plugin._call
        self.plugin._call.assert_called_once()

    def test_receive_stop_bytes(self):
        payload = bytearray("CLOSEPIPE", "utf-8")
        self.network._queue_in.empty = MagicMock(return_value=False)
        self.network._queue_in.get = MagicMock(return_value=payload)
        self.network._receive()
        self.network._queue_in.get.assert_called_once()
        # stopbytes should prevent plugin._call from executing
        self.plugin._call.assert_not_called()
