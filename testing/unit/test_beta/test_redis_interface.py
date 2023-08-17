import unittest
from unittest.mock import patch, Mock, MagicMock
from nanome.api import shapes, structure
from nanome.beta.redis_interface import StreamRedisInterface, PluginInstanceRedisInterface
from nanome.util import enums, Color


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
            args = []
            response = self.redis_interface.request_complex_list()
            self.assertIsNotNone(response)
            mock_rpc_request.assert_called_once_with(fn_name, args=args)

    def test_upload_shapes(self):
        fn_name = 'upload_shapes'
        with patch.object(self.redis_interface, '_rpc_request') as mock_rpc_request:
            mock_rpc_request.return_value = [MagicMock()]
            shape_list = [shapes.Sphere()]  # Represents Shapes
            args = [shape_list]
            response = self.redis_interface.upload_shapes(shape_list)
            self.assertIsNotNone(response)
            mock_rpc_request.assert_called_once_with(fn_name, args=args)

    def test_stream_update(self):
        fn_name = 'stream_update'
        with patch.object(self.redis_interface, '_rpc_request') as mock_rpc_request:
            mock_rpc_request.return_value = [MagicMock()]
            stream_id = 1
            stream_data = [Color.Blue()]  # Represents Shapes
            args = [stream_id, stream_data]
            response = self.redis_interface.stream_update(*args)
            self.assertIsNotNone(response)
            mock_rpc_request.assert_called_once_with(fn_name, args=args)

    def test_get_plugin_data(self):
        fn_name = 'get_plugin_data'
        with patch.object(self.redis_interface, '_rpc_request') as mock_rpc_request:
            mock_rpc_request.return_value = {}
            response = self.redis_interface.get_plugin_data()
            self.assertIsNotNone(response)
            mock_rpc_request.assert_called_once_with(fn_name)

    def test_request_workspace(self):
        fn_name = 'request_workspace'
        with patch.object(self.redis_interface, '_rpc_request') as mock_rpc_request:
            mock_rpc_request.return_value = [structure.Workspace()]
            response = self.redis_interface.request_workspace()
            self.assertIsNotNone(response)
            mock_rpc_request.assert_called_once_with(fn_name, args=[])

    def test_request_complexes(self):
        fn_name = 'request_complexes'
        with patch.object(self.redis_interface, '_rpc_request') as mock_rpc_request:
            comp_ids = [1, 2, 3]
            args = [comp_ids]
            mock_rpc_request.return_value = [structure.Complex()]
            response = self.redis_interface.request_complexes(*args)
            self.assertIsNotNone(response)
            mock_rpc_request.assert_called_once_with(fn_name, args=args)

    def test_update_structures_shallow(self):
        fn_name = 'update_structures_shallow'
        with patch.object(self.redis_interface, '_rpc_request') as mock_rpc_request:
            struct_list = [structure.Complex(), structure.Complex()]
            args = [struct_list]
            mock_rpc_request.return_value = [structure.Complex()]
            response = self.redis_interface.update_structures_shallow(*args)
            self.assertIsNotNone(response)
            mock_rpc_request.assert_called_once_with(fn_name, args=args)

    def test_update_structures_deep(self):
        fn_name = 'update_structures_deep'
        with patch.object(self.redis_interface, '_rpc_request') as mock_rpc_request:
            struct_list = [structure.Complex(), structure.Complex()]
            args = [struct_list]
            mock_rpc_request.return_value = [structure.Complex()]
            response = self.redis_interface.update_structures_deep(*args)
            self.assertIsNotNone(response)
            mock_rpc_request.assert_called_once_with(fn_name, args=args)

    def test_update_workspace(self):
        fn_name = 'update_workspace'
        with patch.object(self.redis_interface, '_rpc_request') as mock_rpc_request:
            ws = structure.Workspace()
            args = [ws]
            mock_rpc_request.return_value = []
            response = self.redis_interface.update_workspace(*args)
            self.assertIsNotNone(response)
            mock_rpc_request.assert_called_once_with(fn_name, args=args)

    def test_zoom_on_structures(self):
        fn_name = 'zoom_on_structures'
        with patch.object(self.redis_interface, '_rpc_request') as mock_rpc_request:
            struct_to_zoom_on = structure.Complex()
            args = [struct_to_zoom_on]
            mock_rpc_request.return_value = []
            response = self.redis_interface.zoom_on_structures(*args)
            self.assertIsNotNone(response)
            mock_rpc_request.assert_called_once_with(fn_name, args=args)

    def test_center_on_structures(self):
        fn_name = 'center_on_structures'
        with patch.object(self.redis_interface, '_rpc_request') as mock_rpc_request:
            struct_to_center_on = structure.Complex()
            args = [struct_to_center_on]
            mock_rpc_request.return_value = []
            response = self.redis_interface.center_on_structures(*args)
            self.assertIsNotNone(response)
            mock_rpc_request.assert_called_once_with(fn_name, args=args)

    def test_add_to_workspace(self):
        fn_name = 'add_to_workspace'
        with patch.object(self.redis_interface, '_rpc_request') as mock_rpc_request:
            comp = structure.Complex()
            args = [comp]
            mock_rpc_request.return_value = []
            response = self.redis_interface.add_to_workspace(*args)
            self.assertIsNotNone(response)
            mock_rpc_request.assert_called_once_with(fn_name, args=args)

    def test_add_bonds(self):
        fn_name = 'add_bonds'
        with patch.object(self.redis_interface, '_rpc_request') as mock_rpc_request:
            comp = structure.Complex()
            args = [comp]
            mock_rpc_request.return_value = []
            response = self.redis_interface.add_bonds(*args)
            self.assertIsNotNone(response)
            mock_rpc_request.assert_called_once_with(fn_name, args=args)

    def test_open_url(self):
        fn_name = 'open_url'
        with patch.object(self.redis_interface, '_rpc_request') as mock_rpc_request:
            url = 'https://nanome.ai'
            args = [url]
            mock_rpc_request.return_value = []
            response = self.redis_interface.open_url(*args)
            self.assertIsNotNone(response)
            mock_rpc_request.assert_called_once_with(fn_name, args=args)

    def test_request_presenter_info(self):
        fn_name = 'request_presenter_info'
        with patch.object(self.redis_interface, '_rpc_request') as mock_rpc_request:
            args = []
            mock_rpc_request.return_value = []
            response = self.redis_interface.request_presenter_info(*args)
            self.assertIsNotNone(response)
            mock_rpc_request.assert_called_once_with(fn_name, args=args)

    def test_request_controller_transforms(self):
        fn_name = 'request_controller_transforms'
        with patch.object(self.redis_interface, '_rpc_request') as mock_rpc_request:
            args = []
            mock_rpc_request.return_value = []
            response = self.redis_interface.request_controller_transforms(*args)
            self.assertIsNotNone(response)
            mock_rpc_request.assert_called_once_with(fn_name, args=args)

    def test_apply_color_scheme(self):
        fn_name = 'apply_color_scheme'
        with patch.object(self.redis_interface, '_rpc_request') as mock_rpc_request:
            color_scheme = enums.ColorScheme.BFactor
            color_scheme_target = enums.ColorSchemeTarget.Ribbon
            apply_to_all = True
            args = [color_scheme, color_scheme_target, apply_to_all]
            mock_rpc_request.return_value = []
            response = self.redis_interface.apply_color_scheme(*args)
            self.assertIsNotNone(response)
            mock_rpc_request.assert_called_once_with(fn_name, args=args)
