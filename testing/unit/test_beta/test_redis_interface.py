import unittest
from unittest.mock import patch, Mock, MagicMock
from nanome.beta.redis_interface import StreamRedisInterface, PluginInstanceRedisInterface
from nanome.util import enums

class TestStreamRedisInterface(unittest.TestCase):
    def setUp(self):
        self.mock_plugin_interface = Mock()
        self.stream_data = {'id': '123'}
        self.stream_redis_interface = StreamRedisInterface(self.stream_data, self.mock_plugin_interface)

    def test_update(self):
        self.stream_redis_interface.update('test_data')
        self.mock_plugin_interface._rpc_request.assert_called_once_with('stream_update', args=['123', 'test_data'])

    def test_destroy(self):
        self.stream_redis_interface.destroy()
        self.mock_plugin_interface._rpc_request.assert_called_once_with('stream_destroy', args=['123'])


class TestPluginInstanceRedisInterface(unittest.TestCase):

    def setUp(self):
        self.mock_redis = Mock()
        with patch('redis.Redis', return_value=self.mock_redis):
            self.redis_interface = PluginInstanceRedisInterface('localhost', 6379, 'password', 'channel')

    def test_set_channel(self):
        self.redis_interface.set_channel('new_channel')
        self.assertEqual(self.redis_interface.channel, 'new_channel')

    def test_ping(self):
        self.redis_interface.ping()
        self.mock_redis.ping.assert_called_once()

    def test_create_writing_stream(self):
        with patch.object(self.redis_interface, '_rpc_request', return_value=MagicMock()):
            atom_indices = [1, 2, 3]
            stream_type = enums.StreamType.color
            response = self.redis_interface.create_writing_stream(atom_indices, stream_type)
            self.assertIsNotNone(response)
            self.assertIsInstance(response, StreamRedisInterface)

    # Add more tests for other methods similarly ...

    def test_rpc_request(self):
        # This test is complex because it deals with time, subscription to Redis, etc.
        # The example here is simple and doesn't handle all the edge cases.
        # You might need to expand on it depending on the specifics of your application.
        function_name = 'request_complex_list'
        with patch('json.dumps', return_value='json_string'), \
             patch('time.time', side_effect=[0, 1, 2, 31]), \
             patch.object(self.redis_interface, 'redis'):
            mock_pubsub = Mock()
            mock_pubsub.get_message.return_value = {'type': 'message', 'data': b'[]'}
            mock_pubsub.channels.keys.return_value = [b'channel']
            self.redis_interface.redis.pubsub.return_value = mock_pubsub

            self.redis_interface._rpc_request(function_name, args=[])

            # Verify interaction with Redis, etc.
            self.redis_interface.redis.publish.assert_called_once_with('channel', 'json_string')
        
    def test_request_complex_list(self):
        fn_name = 'request_complex_list'
        with patch.object(self.redis_interface, '_rpc_request') as mock_rpc_request:
            mock_rpc_request.return_value = []
            atom_indices = [1, 2, 3]
            stream_type = enums.StreamType.color
            response = self.redis_interface.request_complex_list()
            mock_rpc_request.assert_called_once_with(fn_name, args=[])
