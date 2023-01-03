import json
import os
import unittest

from nanome._internal import network
from nanome._internal.serializers import CommandMessageSerializer
from nanome._internal.network.enums import Messages
from nanome.api.structure import Workspace
from nanome.api import ui
from nanome.util import enums

test_assets = os.getcwd() + ("/testing/test_assets")


class CommandDeserializerTestCase(unittest.TestCase):

    def setUp(self):
        version_table_file = os.path.join(test_assets, "version_table_1_24_2.json")
        with open(version_table_file, 'r') as f:
            self.version_table = json.load(f)
        self.serializer = CommandMessageSerializer()

    def test_registered_commands(self):
        self.assertEqual(len(self.serializer._commands), 57)

    def test_deserialize_command(self):
        """Test that we can deserialze bytes from test ReceiveWorkspace Message."""
        bytes_file = os.path.join(test_assets, "ReceiveWorkspaceMessage.bin")
        with open(bytes_file, 'rb') as f:
            payload = f.read()
        received_object, command_hash, request_id = self.serializer.deserialize_command(payload, self.version_table)
        self.assertTrue(isinstance(received_object, Workspace))
        self.assertEqual(command_hash, 783319662)
        self.assertEqual(request_id, 2)


class MessageSerializeTestCase(unittest.TestCase):

    def setUp(self):
        self.plugin_id = 7
        self.serializer = CommandMessageSerializer()
        version_table_file = os.path.join(test_assets, "version_table_1_24_2.json")
        with open(version_table_file, 'r') as f:
            self.version_table = json.load(f)

    def test_registered_messages(self):
        self.assertEqual(len(self.serializer._messages), 56)

    def test_connect(self):
        request_id = 1
        message_type = Messages.connect
        arg = None
        expects_response = True
        arg = [network.Packet.packet_type_plugin_connection, self.version_table]
        payload = self.serializer.serialize_message(request_id, message_type, arg, self.version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))
        # Deserialize
        # received_object, command_hash, request_id = self.serializer.deserialize_command(payload, self.version_table)
        # self.assertEqual(received_object, None)
        # self.assertEqual(command_hash, None)
        # self.assertEqual(request_id, None)
    
    def test_plugin_list_button_set(self):
        request_id = 1
        message_type = Messages.plugin_list_button_set
        arg = [enums.PluginListButtonType.run, "Button Text!", True]
        expects_response = False
        payload = self.serializer.serialize_message(request_id, message_type, arg, self.version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))
        # Deserialize
        # received_object, command_hash, request_id = self.serializer.deserialize_command(payload, self.version_table)
        # self.assertEqual(received_object, None)
        # self.assertEqual(command_hash, None)
        # self.assertEqual(request_id, None)

    def test_serialize_message_complex_list_request(self):
        """Test that the serializer returns a set of bytes."""
        request_id = 1
        message_type = Messages.complex_list_request
        arg = None
        version_table = self.version_table
        expects_response = False
        context = self.serializer.serialize_message(request_id, message_type, arg, version_table, expects_response)
        self.assertTrue(isinstance(context, memoryview))

    def test_serialize_message_menu_update(self):
        """Test that the serializer returns a set of bytes."""
        request_id = 2
        message_type = Messages.menu_update
        menu = ui.Menu.io.from_json(os.path.join(test_assets, "test_menu_smina.json"))
        shallow = False
        args = [menu, shallow]
        version_table = self.version_table
        expects_response = False
        payload = self.serializer.serialize_message(request_id, message_type, args, version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))
        # deserialize
        # received_object, command_hash, request_id = self.serializer.deserialize_command(payload, self.version_table)
        # self.assertTrue(isinstance(received_object, ui.Menu))
