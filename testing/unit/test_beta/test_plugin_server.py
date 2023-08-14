import asyncio
import unittest
from unittest.mock import patch, MagicMock, AsyncMock, ANY
from nanome._internal.network import Packet
from nanome.beta.nanome_sdk.plugin_server import PluginServer


class TestPluginServer(unittest.TestCase):

    def setUp(self):
        self.server = PluginServer()
        # Create mock packet.
        self.packet = Packet()
        session_id = 121
        packet_type = Packet.packet_type_client_connection
        self.plugin_id = 0
        self.packet.set(session_id, packet_type, self.plugin_id)
        test_payload = b'test1test2test3'
        self.packet.write(test_payload)

        stop_bytes = bytearray("CLOSEPIPE", "utf-8")
        self.stop_packet = Packet()
        self.stop_packet.set(0, Packet.packet_type_plugin_disconnection, 0)
        self.stop_packet.write(stop_bytes)

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    @patch("asyncio.open_connection", new_callable=AsyncMock)
    @patch.object(PluginServer, "connect_plugin", new_callable=AsyncMock)
    @patch.object(PluginServer, "keep_alive", new_callable=AsyncMock)
    @patch.object(PluginServer, "poll_nts", new_callable=AsyncMock)
    def test_run(self, mock_poll_nts, mock_keep_alive, mock_connect_plugin, mock_open_connection):
        mock_open_connection.return_value = (MagicMock(), MagicMock())
        mock_connect_plugin.return_value = "test_plugin_id"
        asyncio.run(self.server.run("host", "port", "name", "description", "plugin_class"))

        mock_open_connection.assert_called_once_with("host", "port", ssl=ANY)
        mock_connect_plugin.assert_called_once_with("name", "description")
        mock_poll_nts.assert_called_once()

    def test_keep_alive(self) -> None:
        self.server.nts_writer = MagicMock()
        self.server.nts_writer.write = MagicMock()
        self.server.nts_writer.drain = AsyncMock()

        # run the keep_alive function and simulate a single loop iteration
        task = self.loop.create_task(self.server.keep_alive(self.plugin_id))
        self.loop.run_until_complete(asyncio.sleep(1))
        task.cancel()
        self.server.nts_writer.write.assert_called_once()
        self.server.nts_writer.drain.assert_called_once()

    @patch.object(PluginServer, "route_bytes", new_callable=AsyncMock)
    def test_poll_nts(self, route_bytes_mock):
        self.server.nts_reader = MagicMock()
        
        packed_packet = self.packet.pack()
        header_fut = asyncio.Future()
        header_fut.set_result(packed_packet[:Packet.packet_header_length])
        payload_fut = asyncio.Future()
        payload_fut.set_result(packed_packet[Packet.packet_header_length:])

        packed_stop_packet = self.stop_packet.pack()
        stop_packet_header_fut = asyncio.Future()
        stop_packet_header_fut.set_result(packed_stop_packet[:Packet.packet_header_length])
        stop_packet_payload_fut = asyncio.Future()
        stop_packet_payload_fut.set_result(packed_stop_packet[Packet.packet_header_length:])
        self.server.nts_reader.readexactly.side_effect = [
            header_fut, payload_fut, stop_packet_header_fut, stop_packet_payload_fut]

        # Run task to process two packets set up above, and then cancel task
        task = self.loop.create_task(self.server.poll_nts())
        self.loop.run_until_complete(asyncio.sleep(2))  # 2 seconds is plenty ofs time to wait.
        task.cancel()
        self.assertEqual(route_bytes_mock.call_count, 2)

    @patch.object(Packet, "header_unpack")
    def test_connect_plugin(self, mock_header_unpack):
        self.server.nts_writer = MagicMock()
        self.server.nts_writer.write = AsyncMock()
        self.server.nts_writer.drain = AsyncMock()
        self.server.nts_reader = MagicMock()
        self.server.nts_reader.readexactly = AsyncMock()
        
        mock_header_unpack.return_value = [0, 0, 0, "test_plugin_id", 0]

        plugin_id = asyncio.run(self.server.connect_plugin("name", "description"))
        
        self.assertEqual(plugin_id, "test_plugin_id")

    # Add more test methods as necessary

if __name__ == "__main__":
    unittest.main()