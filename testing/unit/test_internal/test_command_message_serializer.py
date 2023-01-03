import json
import os
import unittest

# from nanome.api.structure import Complex
from nanome._internal.network.serialization.serializer import CommandMessageSerializer
from nanome._internal.network.commands.enums import Messages

test_assets = os.getcwd() + ("/testing/test_assets")


class CommandMessageSerializerTestCase(unittest.TestCase):

    def setUp(self):
        self.serializer = CommandMessageSerializer()
        version_table_file = os.path.join(test_assets, "version_table_1_24_2.json")
        with open(version_table_file, 'r') as f:
            self.version_table = json.load(f)

    def test_registered_commands(self):
        self.assertEqual(len(self.serializer._commands), 57)

    def test_registered_messages(self):
        self.assertEqual(len(self.serializer._messages), 56)
    
    def test_serialize_message(self):
        """Test that the serializer returns a set of bytes."""
        request_id = 1
        message_type = Messages.complex_list_request
        arg = None
        version_table = self.version_table
        expects_response = False
        context = self.serializer.serialize_message(request_id, message_type, arg, version_table, expects_response)
        self.assertTrue(isinstance(context, memoryview))

