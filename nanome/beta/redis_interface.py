import os
import pickle
import random
import redis
import time
import uuid
from typing import List, Union
from nanome import PluginInstance
from nanome._internal.enums import Messages
from nanome._internal.network import Packet
from nanome.api.serializers import CommandMessageSerializer
from nanome.api.streams import Stream
from nanome.api import shapes, structure, ui, user
from nanome.util import Logs, enums, Vector3, Quaternion
from nanome.util.file import LoadInfoDone

__all__ = ['PluginInstanceRedisInterface']

workspace_struct = Union[
    structure.Complex, structure.Molecule, structure.Chain,
    structure.Residue, structure.Atom, structure.Bond]

ui_content = Union[
    ui.Button, ui.Label, ui.Mesh, ui.Image,
    ui.Dropdown, ui.DropdownItem, ui.LoadingBar,
    ui.Slider, ui.TextInput
]
NTS_RESPONSE_TIMEOUT = os.environ.get('NTS_RESPONSE_TIMEOUT', 30)


def random_request_id():
    """Generate a random but valid request id."""
    max_req_id = 4294967295
    request_id = random.randint(0, max_req_id)
    return request_id


class PluginInstanceRedisInterface:
    """Provides interface for publishing PluginInstance RPC requests over Redis.

    The idea is to feel like you're using the standard
    PluginInstance, but all calls are being made through Redis.
    """

    def __init__(self, redis_host, redis_port, redis_password, redis_channel=None):
        """Initialize the Connection to Redis."""
        self.redis = redis.Redis(host=redis_host, port=redis_port, password=redis_password)
        self.plugin_class = PluginInstance
        self.channel = redis_channel
        self.plugin_id = None
        self.session_id = None
        self.version_table = None

    def connect(self):
        """Ping Redis, and then get data from plugin required for serialization."""
        self.redis.ping()
        plugin_data = self.get_plugin_data()
        self.plugin_id = plugin_data['plugin_id']
        self.session_id = plugin_data['session_id']
        self.version_table = plugin_data['version_table']

    def create_writing_stream(self, indices_list: List[int], stream_type: enums.StreamType) -> Stream:
        """Create a stream allowing the plugin to continuously update properties of many objects."""
        message_type = Messages.stream_create
        expects_response = True
        args = (stream_type, indices_list, enums.StreamDirection.writing)
        response = self._send_message(message_type, args, expects_response)
        err_code, stream_args = response[0], response[1:]
        if err_code != 0:
            raise ValueError(f"Error creating stream: {err_code}")
        stream = Stream(None, *stream_args)
        return stream

    def request_workspace(self) -> structure.Workspace:
        """Request the entire workspace, in deep mode"""
        message_type = Messages.workspace_request
        expects_response = True
        args = None
        response = self._send_message(message_type, args, expects_response)
        return response

    def request_complexes(self, id_list: List[int]) -> List[structure.Complex]:
        """Requests a list of complexes by their indices.

        Complexes returned contains the full structure (atom/bond/residue/chain/molecule)
        """
        message_type = Messages.complexes_request
        expects_response = True
        args = id_list
        response = self._send_message(message_type, args, expects_response)
        return response

    def update_structures_shallow(self, structures: List[workspace_struct]):
        """Update the specific molecular structures in the scene to match the structures in parameter.

        Only updates the structure's data, will not update children or other descendents.
        """
        message_type = Messages.structures_shallow_update
        expects_response = False
        args = structures
        self._send_message(message_type, args, expects_response)

    def update_structures_deep(self, struct_list: List[workspace_struct]):
        """Update the specific molecular structures in the scene to match the structures in parameter.

        Will also update descendent structures and can be used to remove descendent structures.
        """
        message_type = Messages.structures_deep_update
        expects_response = True
        args = struct_list
        response = self._send_message(message_type, args, expects_response)
        return response

    def request_complex_list(self) -> List[structure.Complex]:
        """Request the list of all complexes in the workspace, in shallow mode."""
        message_type = Messages.complex_list_request
        args = None
        expects_response = True
        response = self._send_message(message_type, args, expects_response)
        return response

    def _send_message(self, message_type: Messages, fn_args, expects_response):
        function_name = message_type.name
        request_id, packet = self._build_packet(message_type, fn_args, expects_response)
        message = self._build_message(function_name, request_id, packet, expects_response)
        serialized_response = self._rpc_request(message, expects_response=expects_response)
        if serialized_response is not None:
            response = self._deserialize_payload(serialized_response)
            return response

    def zoom_on_structures(self, structures: workspace_struct) -> None:
        """Repositions and resizes the workspace such that the provided structure(s) will be in the

        center of the users view.
        """
        message_type = Messages.structures_zoom
        expects_response = False
        args = structures
        self._send_message(message_type, args, expects_response)

    async def send_notification(self, notification_type: enums.NotificationTypes, message: str):
        """Send a notification to the user"""
        message_type = Messages.notification_send
        expects_response = False
        args = [notification_type, message]
        self._send_message(message_type, args, expects_response)

    def center_on_structures(self, structures: workspace_struct):
        """Repositions the workspace such that the provided structure(s) will be in the center of the world."""
        message_type = Messages.structures_center
        expects_response = False
        args = structures
        self._send_message(message_type, args, expects_response)

    def add_to_workspace(self, complex_list: List[structure.Complex]):
        """Add a list of complexes to the current workspace."""
        message_type = Messages.add_to_workspace
        expects_response = True
        args = complex_list
        response = self._send_message(message_type, args, expects_response)
        return response

    def open_url(self, url: str, desktop_browser: bool = False) -> None:
        """Open a URL in the user's browser."""
        message_type = Messages.open_url
        expects_response = False
        args = (url, desktop_browser)
        self._send_message(message_type, args, expects_response)

    def request_presenter_info(self) -> user.PresenterInfo:
        """Get info about the presenter."""
        message_type = Messages.presenter_info_request
        expects_response = True
        args = None
        result = self._send_message(message_type, args, expects_response)
        return result

    def request_controller_transforms(self):
        """Requests presenter controller info.

        (head position, head rotation, left controller position,
        left controller rotation, right controller position,
        right controller rotation)
        """
        message_type = Messages.controller_transforms_request
        expects_response = True
        args = None
        result = self._send_message(message_type, args, expects_response)
        return result

    def apply_color_scheme(self, color_scheme: enums.ColorScheme, target: enums.ColorSchemeTarget, only_carbons: bool = False):
        """Applies a color scheme to selected atoms."""
        message_type = Messages.apply_color_scheme
        expects_response = False
        args = (color_scheme, target, only_carbons)
        self._send_message(message_type, args, expects_response)

    def _rpc_request(self, message, expects_response=False):
        """Publish an RPC request to redis, and await response.

        :rtype: data returned by PluginInstance function called by RPC.
        """
        pubsub = self.redis.pubsub(ignore_subscribe_messages=True)
        function_name = message['function']
        if 'response_channel' in message:
            response_channel = message['response_channel']
            pubsub.subscribe(response_channel)
        message_pickle = pickle.dumps(message)
        Logs.message(f"Sending {function_name} Request to Redis Channel {self.channel}")
        self.redis.publish(self.channel, message_pickle)
        # Start polling for response message.
        start_time = time.time()
        while expects_response:
            message = pubsub.get_message()
            if time.time() >= start_time + NTS_RESPONSE_TIMEOUT:
                raise TimeoutError(f"Timeout waiting for response from RPC {function_name}")
            if not message:
                continue
            if message.get('type') == 'message':
                Logs.message(f"Response received on channel {response_channel}")
                pickled_message_data = message['data']
                pubsub.unsubscribe()
                message_data = pickle.loads(pickled_message_data)
                return message_data

    def upload_shapes(self, shape_list: List[shapes.Shape]):
        """Upload a list of shapes to the server.

        :arg: shape_list: List of shapes to upload.
        :rtype: list. List of shape IDs.
        """
        message_type = Messages.set_shape
        expects_response = True
        args = shape_list
        shape_indices, _bytes = self._send_message(message_type, args, expects_response)
        for shape, shape_index in zip(shape_list, shape_indices):
            shape._index = shape_index
        return shape_list

    def get_plugin_data(self) -> dict:
        """Custom function to get data necessary for serialization from the remote plugin."""
        function_name = 'get_plugin_data'
        expects_response = True
        message = self._build_message(function_name, None, None, expects_response)
        response = self._rpc_request(message, expects_response=expects_response)
        return response

    def _build_packet(self, message_type, args=None, expects_response=False):
        serializer = CommandMessageSerializer()
        request_id = random_request_id()
        message = serializer.serialize_message(request_id, message_type, args, self.version_table, expects_response)
        packet = Packet()
        packet.set(self.session_id, Packet.packet_type_message_to_client, self.plugin_id)
        packet.write(message)
        return request_id, packet

    def update_content(self, *content: ui_content) -> None:
        """Update specific UI elements (button, slider, list...)
        """
        message_type = Messages.content_update
        expects_response = False
        args = list(content)
        self._send_message(message_type, args, expects_response)

    def update_node(self, *nodes: List[ui.LayoutNode]) -> None:
        """Updates layout nodes and their children."""
        message_type = Messages.node_update
        expects_response = False
        args = nodes
        self._send_message(message_type, args, expects_response)

    def set_menu_transform(self, index: int, position: Vector3, rotation: Quaternion, scale: Vector3):
        """Update the position, scale, and rotation of the menu."""
        message_type = Messages.menu_transform_set
        expects_response = False
        args = [index, position, rotation, scale]
        self._send_message(message_type, args, expects_response)

    def request_menu_transform(self, index: int):
        """Requests spatial information of the plugin menu (position, rotation, scale)."""
        message_type = Messages.menu_transform_request
        expects_response = True
        args = [index]
        response = self._send_message(message_type, args, expects_response)
        return response

    def update_stream(self, stream: Stream, data: List):
        """Feed new data into an existing stream."""
        message_type = Messages.stream_feed
        expects_response = True

        stream_id = stream.id
        data_type = stream.data_type
        args = [stream_id, data, data_type]

        response = self._send_message(message_type, args, expects_response)
        return response

    def destroy_stream(self, stream: Stream):
        """Delete an existing stream."""
        message_type = Messages.stream_destroy
        expects_response = False
        args = stream.id
        self._send_message(message_type, args, expects_response)

    def send_files_to_load(self, files_list: List[str]) -> LoadInfoDone:
        """Send a molecular structure file (PDB, SDF, etc.) to the workspace to render."""
        message_type = Messages.load_file
        expects_response = True
        files_and_data = []
        for file in files_list:
            if isinstance(file, tuple):
                full_path, file_name = file
                file_name += '.' + full_path.split('.')[-1]
            else:
                full_path = file.replace('\\', '/')
                file_name = full_path.split('/')[-1]
            with open(full_path, 'rb') as content_file:
                data = content_file.read()
            files_and_data.append((file_name, data))
        fn_args = (files_and_data, True, True)  # idk what the True, True does
        response = self._send_message(message_type, fn_args, expects_response)
        return response

    @staticmethod
    def _build_message(function_name, request_id, packet=None, expects_response=False):
        response_channel = str(uuid.uuid4())
        message = {
            'function': function_name,
            'request_id': request_id
        }
        if packet:
            pack = packet.pack()
            message['packet'] = pack
        if expects_response:
            message['response_channel'] = response_channel
        return message

    def _deserialize_payload(self, payload: bytearray):
        serializer = CommandMessageSerializer()
        received_obj_list, command_hash, request_id = serializer.deserialize_command(
            payload, self.version_table)
        return received_obj_list
