import json
import pickle
import os
import redis
import uuid
import time

from nanome import PluginInstance
from nanome._internal.enums import Messages
from nanome._internal.network import Packet
from nanome.api import schemas
from nanome.api.serializers import CommandMessageSerializer
from nanome.util import Logs
from marshmallow import fields
from nanome.api.schemas.api_definitions import api_function_definitions
import random

__all__ = ['PluginInstanceRedisInterface', 'StreamRedisInterface']

NTS_RESPONSE_TIMEOUT = os.environ.get('NTS_RESPONSE_TIMEOUT', 30)
import sys
import os


def random_request_id():
    """Generate a random but valid request id."""
    max_req_id = 4294967295
    request_id = random.randint(0, max_req_id)
    return request_id


class StreamRedisInterface:
    """Gets wrapped around a stream object on creation, and is used to send data to the stream through redis.

    The PluginService has functions set up to handle streams, because streams on the client side aren't networked.
    This should not be called explicitly, but used through the RedisPluginInterface class.
    """

    def __init__(self, stream_data, plugin_interface):
        self.stream_id = stream_data['id']
        # self.error = stream_data['error']
        self._plugin_interface = plugin_interface

    def update(self, stream_data):
        response = self._plugin_interface._rpc_request(
            'stream_update', args=[self.stream_id, stream_data])
        return response

    def destroy(self):
        response = self._plugin_interface._rpc_request(
            'stream_destroy', args=[self.stream_id])
        return response


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

    def set_channel(self, value):
        self.channel = value

    def connect(self):
        """Ping Redis, and then get data from plugin required for serialization."""
        self.redis.ping()
        plugin_data = self.get_plugin_data()
        self.plugin_id = plugin_data['plugin_id']
        self.session_id = plugin_data['session_id']
        self.version_table = plugin_data['version_table']

    def create_writing_stream(self, indices_list, stream_type):
        """Return a stream wrapped in the RedisStreamInterface"""
        function_name = 'create_writing_stream'
        args = [indices_list, stream_type]
        stream = self._rpc_request(function_name, args=args)
        if stream:
            stream_interface = StreamRedisInterface(stream, self)
            response = stream_interface
        return response

    def request_workspace(self):
        function_name = 'request_workspace'
        args = []
        response = self._rpc_request(function_name, args=args)
        return response

    def request_complexes(self, comp_id_list):
        function_name = 'request_complexes'
        args = [comp_id_list]
        response = self._rpc_request(function_name, args=args)
        return response

    def update_structures_shallow(self, struct_list):
        function_name = 'update_structures_shallow'
        args = [struct_list]
        response = self._rpc_request(function_name, args=args)
        return response

    def update_structures_deep(self, struct_list):
        function_name = 'update_structures_deep'
        args = [struct_list]
        response = self._rpc_request(function_name, args=args)
        return response

    def request_complex_list(self):
        function_name = 'request_complex_list'
        message_type = Messages.complexes_request
        args = None
        expects_response = True
        self.send_message(message_type, function_name, args, expects_response)
    
    def send_message(self, message_type: Messages, function_name, args, expects_response):
        request_id, packet = self.build_packet(message_type, args, expects_response)
        message = self.build_message(function_name, request_id, packet, expects_response)
        response = self._rpc_request(message, expects_response=expects_response)
        return response

    def stream_update(self, stream_id, stream_data):
        function_name = 'stream_update'
        args = [stream_id, stream_data]
        response = self._rpc_request(function_name, args=args)
        return response

    def update_workspace(self, workspace):
        function_name = 'update_workspace'
        args = [workspace]
        response = self._rpc_request(function_name, args=args)
        return response

    def zoom_on_structures(self, struct_list):
        function_name = 'zoom_on_structures'
        args = [struct_list]
        response = self._rpc_request(function_name, args=args)
        return response

    def send_notification(self):
        function_name = 'send_notification'
        args = []
        response = self._rpc_request(function_name, args=args)
        return response

    def center_on_structures(self, struct_list):
        function_name = 'center_on_structures'
        args = [struct_list]
        response = self._rpc_request(function_name, args=args)
        return response

    def add_to_workspace(self, comp_list):
        function_name = 'add_to_workspace'
        args = [comp_list]
        response = self._rpc_request(function_name, args=args)
        return response

    def add_bonds(self, comp_list):
        function_name = 'add_bonds'
        args = [comp_list]
        response = self._rpc_request(function_name, args=args)
        return response

    def open_url(self, url):
        function_name = 'open_url'
        args = [url]
        response = self._rpc_request(function_name, args=args)
        return response

    def request_presenter_info(self):
        function_name = 'request_presenter_info'
        args = []
        response = self._rpc_request(function_name, args=args)
        return response

    def request_controller_transforms(self):
        function_name = 'request_controller_transforms'
        args = []
        response = self._rpc_request(function_name, args=args)
        return response

    def apply_color_scheme(self, color_scheme, color_scheme_target, apply_to_all):
        function_name = 'apply_color_scheme'
        args = [color_scheme, color_scheme_target, apply_to_all]
        response = self._rpc_request(function_name, args=args)
        return response

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
                response_channel = next(iter(pubsub.channels.keys())).decode('utf-8')
                Logs.message(f"Response received on channel {response_channel}")
                message_data = message['data']
                # response_data = json.loads(message_data_str)
                pubsub.unsubscribe()
                return message_data

    def upload_shapes(self, shape_list):
        """Upload a list of shapes to the server.

        :arg: shape_list: List of shapes to upload.
        :rtype: list. List of shape IDs.
        """
        function_name = 'upload_shapes'
        args = [shape_list]
        response = self._rpc_request(function_name, args=args)
        return response

    def stream_update(self, stream_id, stream_data):
        """Update stream with data.
        """
        function_name = 'stream_update'
        args = [stream_id, stream_data]
        response = self._rpc_request(function_name, args=args)
        return response

    def get_plugin_data(self):
        function_name = 'get_plugin_data'
        expects_response = True
        message = self.build_message(function_name, None, None, expects_response)
        pickled_response = self._rpc_request(message, expects_response=expects_response)
        response = pickle.loads(pickled_response)
        return response

    def build_packet(self, message_type, args=None, expects_response=False):
        serializer = CommandMessageSerializer()
        request_id = random_request_id()
        message = serializer.serialize_message(request_id, message_type, args, self.version_table, expects_response)
        packet = Packet()
        packet.set(self.session_id, Packet.packet_type_message_to_client, self.plugin_id)
        packet.write(message)
        return request_id, packet

    @staticmethod
    def build_message(function_name, request_id, packet=None, expects_response=False):
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




