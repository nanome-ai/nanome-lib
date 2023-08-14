import asyncio
import unittest
from unittest.mock import patch, MagicMock, AsyncMock, ANY
from nanome._internal.network import Packet
from nanome.beta.nanome_sdk.plugin_server import PluginServer


class TestPluginServer(unittest.TestCase):

    def setUp(self):
        self.server = PluginServer()

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

    @patch("asyncio.sleep", new_callable=AsyncMock)
    def test_keep_alive(self, mock_sleep):
        self.server.nts_writer = MagicMock()
        self.server.nts_writer.write = AsyncMock()
        self.server.nts_writer.drain = AsyncMock()

        # run the keep_alive function and simulate a single loop iteration
        asyncio.run(self.server.keep_alive("test_plugin_id"))
        
        self.server.nts_writer.write.assert_called_once()
        self.server.nts_writer.drain.assert_called_once()

    @patch.object(PluginServer, "route_bytes", new_callable=AsyncMock)
    def test_poll_nts(self, mock_route_bytes):
        self.server.nts_reader = MagicMock()
        self.server.nts_reader.readexactly = AsyncMock()
        self.server.nts_reader.readexactly.side_effect = [
            bytes([0] * Packet.packet_header_length),
            bytes([0] * 5)  # dummy payload
        ]
        
        asyncio.run(self.server.poll_nts())
        
        self.assertEqual(mock_route_bytes.call_count, 1)

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