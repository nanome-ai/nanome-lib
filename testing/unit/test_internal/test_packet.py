# import json
import os
import unittest
from nanome._internal.network import Packet, Data


test_assets = os.getcwd() + ("/testing/test_assets")


class PacketTestCase(unittest.TestCase):

    def setUp(self):
        self.packet = Packet()

    def test_write_string(self):
        test_payload = 'test'
        self.packet.write_string(test_payload)
        payload = self.packet.payload
        expected_value = test_payload.encode('utf-8')
        self.assertEqual(payload, expected_value)

    def test_write(self):
        test_payload_1 = 'test1'.encode('utf-8')
        self.packet.write(test_payload_1)
        payload = self.packet.payload
        expected_value = test_payload_1
        self.assertEqual(payload, expected_value)
        # extend payload
        test_payload_2 = 'test2'.encode('utf-8')
        self.packet.write(test_payload_2)
        expected_value = test_payload_1 + test_payload_2  # test1test2
        self.assertEqual(self.packet.payload, expected_value)

    def test_compress(self):
        self.assertEqual(self.packet.payload_length, 0)
        test_payload = 'test1test2test3'
        test_payload_compressed = b'*I-.1,\x01\x12F \xc2\x18\x00\x00\x00\xff\xff'
        self.packet.write_string(test_payload)
        self.assertEqual(self.packet.payload_length, len(test_payload))
        self.packet.compress()
        self.assertEqual(self.packet.payload_length, len(test_payload_compressed))
        self.assertEqual(self.packet.payload, test_payload_compressed)

    def test_pack_unpack(self):
        # Generate a packet with a payload.
        session_id = 121
        packet_type = Packet.packet_type_client_connection
        plugin_id = 0
        packet = Packet()
        packet.set(session_id, packet_type, plugin_id)
        self.assertEqual(packet.session_id, session_id)
        self.assertEqual(packet.packet_type, packet_type)
        self.assertEqual(packet.plugin_id, plugin_id)
        test_payload = b'test1test2test3'
        packet.write(test_payload)
        sent_bytes = packet.pack()

        # Receive sent bytes and parse.
        new_packet = Packet()
        data = Data()
        data.received_data(sent_bytes)
        # Get header
        header = new_packet.get_header(data)
        self.assertTrue(header)
        self.assertEqual(new_packet.packet_type, packet_type)
        self.assertEqual(new_packet.plugin_id, plugin_id)
        self.assertEqual(new_packet.session_id, session_id)
        # Make sure payload matches what was originally sent.
        new_packet.get_payload(data)
        self.assertEqual(new_packet.payload, test_payload)
