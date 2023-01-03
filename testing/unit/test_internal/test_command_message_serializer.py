import os
import unittest

# from nanome.api.structure import Complex
from nanome._internal.network.serialization.serializer import CommandMessageSerializer
test_assets = os.getcwd() + ("/testing/test_assets")


class CommandMessageSerializerTestCase(unittest.TestCase):

    def setUp(self):
        self.serializer = CommandMessageSerializer()

    def test_registered_commands(self):
        self.assertEqual(len(self.serializer._commands), 57)


    def test_registered_messages(self):
        self.assertEqual(len(self.serializer._messages), 56)

