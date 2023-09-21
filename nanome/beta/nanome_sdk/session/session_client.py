import asyncio
import logging
from nanome.api import ui
from nanome.api.serializers import CommandMessageSerializer
from nanome.util import enums
from nanome._internal.network.packet import Packet
from nanome._internal.enums import Messages
from nanome.beta.nanome_sdk import utils
from nanome.beta.nanome_sdk.session.bonding import Bonding


__all__ = ["SessionClient"]


class SessionClient:
    """Provides API for connecting to a Nanome session."""

    def __init__(self, plugin_id, session_id, version_table):
        self.version_table = version_table
        self.plugin_id = plugin_id
        self.session_id = session_id
        self.logger = logging.getLogger(__name__)
        self.request_futs = {}
        self.reader = self.writer = None
        self.deserialize_payloads = True  # By default, convert received payloads into Nanome objects.

    def __new__(cls, *args, **kwargs):
        # Create Singleton object
        if not hasattr(cls, 'instance'):
            cls.instance = super(SessionClient, cls).__new__(cls)
        return cls.instance

    def update_menu(self, menu, shallow=False):
        self.logger.debug("Sending Update Menu.")
        message_type = Messages.menu_update
        expects_response = False
        args = [menu, shallow]
        self._send_message(message_type, args, expects_response)

    async def request_complex_list(self):
        message_type = Messages.complex_list_request
        expects_response = True
        args = None
        request_id = self._send_message(message_type, args, expects_response)
        result = await self._process_payload(request_id)
        return result

    async def send_connect(self, plugin_id, session_id, version_table):
        """Let NTS know session is connected and ready to party."""
        self.reader, self.writer = await utils.connect_stdin_stdout()
        serializer = CommandMessageSerializer()
        message_type = Messages.connect
        request_id = utils.random_request_id()
        args = [Packet._compression_type(), version_table]
        expects_response = False
        message = serializer.serialize_message(request_id, message_type, args, version_table, expects_response)

        packet = Packet()
        packet.set(session_id, Packet.packet_type_message_to_client, plugin_id)
        packet.write(message)
        pack = packet.pack()
        self.writer.write(pack)
        self.logger.debug(f'Session {session_id} Connected')

    async def request_workspace(self):
        message_type = Messages.workspace_request
        expects_response = True
        args = None
        request_id = self._send_message(message_type, args, expects_response)
        result = await self._process_payload(request_id)
        return result

    async def request_complexes(self, id_list):
        message_type = Messages.complexes_request
        expects_response = True
        args = id_list
        request_id = self._send_message(message_type, args, expects_response)
        result = await self._process_payload(request_id)
        return result

    def update_workspace(self, workspace):
        message_type = Messages.workspace_update
        expects_response = False
        args = [workspace]
        self._send_message(message_type, args, expects_response)

    async def send_notification(self, notification_type, message):
        message_type = Messages.notification_send
        expects_response = False
        args = [notification_type, message]
        self._send_message(message_type, args, expects_response)

    async def update_structures_deep(self, structures):
        message_type = Messages.structures_deep_update
        expects_response = True
        args = structures
        request_id = self._send_message(message_type, args, expects_response)
        result = await self._process_payload(request_id)
        return result

    def update_structures_shallow(self, structures):
        message_type = Messages.structures_shallow_update
        expects_response = False
        args = structures
        self._send_message(message_type, args, expects_response)

    def zoom_on_structures(self, structures):
        message_type = Messages.structures_zoom
        expects_response = False
        args = structures
        self._send_message(message_type, args, expects_response)

    def center_on_structures(self, structures):
        message_type = Messages.structures_center
        expects_response = False
        args = structures
        self._send_message(message_type, args, expects_response)

    async def add_to_workspace(self, complex_list):
        message_type = Messages.add_to_workspace
        expects_response = True
        args = complex_list
        request_id = self._send_message(message_type, args, expects_response)
        result = await self._process_payload(request_id)
        return result

    async def remove_from_workspace(self, complex_list):
        """By removing all atoms from complexes, we can remove them from the workspace."""
        from nanome.api.structure import Complex
        message_type = Messages.structures_deep_update
        expects_response = True
        empty_complexes = []
        for complex in complex_list:
            empty = Complex()
            empty.index = complex.index
            empty_complexes.append(empty)
        args = empty_complexes
        request_id = self._send_message(message_type, args, expects_response)
        result = await self._process_payload(request_id)
        return result

    def update_content(self, *content):
        message_type = Messages.content_update
        expects_response = False
        args = list(content)
        self._send_message(message_type, args, expects_response)

    def update_node(self, *nodes):
        message_type = Messages.node_update
        expects_response = False
        args = nodes
        self._send_message(message_type, args, expects_response)

    def set_menu_transform(self, index, position, rotation, scale):
        message_type = Messages.menu_transform_set
        expects_response = False
        args = [index, position, rotation, scale]
        self._send_message(message_type, args, expects_response)

    async def request_menu_transform(self, index):
        message_type = Messages.menu_transform_request
        expects_response = True
        args = [index]
        request_id = self._send_message(message_type, args, expects_response)
        result = await self._process_payload(request_id)
        return result

    async def save_files(self, file_list):
        message_type = Messages.file_save
        expects_response = True
        args = file_list
        request_id = self._send_message(message_type, args, expects_response)
        result = await self._process_payload(request_id)
        return result

    async def create_writing_stream(self, indices_list, stream_type):
        message_type = Messages.stream_create
        expects_response = True
        args = (stream_type, indices_list, enums.StreamDirection.writing)
        request_id = self._send_message(message_type, args, expects_response)
        result = await self._process_payload(request_id)
        return result

    async def create_reading_stream(self, indices_list, stream_type):
        message_type = Messages.stream_create
        expects_response = True
        args = (stream_type, indices_list, enums.StreamDirection.reading)
        request_id = self._send_message(message_type, args, expects_response)
        result = await self._process_payload(request_id)
        return result

    async def add_volume(self, comp, volume, properties, complex_to_align_index=-1):
        message_type = Messages.add_volume
        expects_response = True
        args = (comp, complex_to_align_index, volume, properties)
        request_id = self._send_message(message_type, args, expects_response)
        result = await self._process_payload(request_id)
        return result

    def open_url(self, url, desktop_browser=False):
        message_type = Messages.open_url
        expects_response = False
        args = (url, desktop_browser)
        self._send_message(message_type, args, expects_response)

    async def request_presenter_info(self):
        message_type = Messages.presenter_info_request
        expects_response = True
        args = None
        request_id = self._send_message(message_type, args, expects_response)
        result = await self._process_payload(request_id)
        return result

    async def request_controller_transforms(self):
        message_type = Messages.controller_transforms_request
        expects_response = True
        args = None
        request_id = self._send_message(message_type, args, expects_response)
        result = await self._process_payload(request_id)
        return result

    def set_plugin_list_button(self, button: ui.Button, text: str = None, usable: bool = None):
        message_type = Messages.plugin_list_button_set
        expects_response = False
        args = (button, text, usable)
        self._send_message(message_type, args, expects_response)

    async def send_files_to_load(self, files_list):
        message_type = Messages.load_file
        expects_response = True
        args = (files_list, True, True)
        request_id = self._send_message(message_type, args, expects_response)
        result = await self._process_payload(request_id)
        return result

    async def shapes_upload_multiple(self, shape_list):
        message_type = Messages.set_shape
        expects_response = True
        args = shape_list
        request_id = self._send_message(message_type, args, expects_response)
        result = await self.request_futs[request_id]
        del self.request_futs[request_id]
        # Make sure indices get set.
        if not isinstance(result, bytearray):
            indices = result[0]
            for shape, index in zip(shape_list, indices):
                shape._index = index
        return shape_list

    async def request_export(self, format, entities=None):
        message_type = Messages.export_files
        expects_response = True
        args = (format, entities)
        request_id = self._send_message(message_type, args, expects_response)
        result = await self._process_payload(request_id)
        return result

    def apply_color_scheme(self, color_scheme, target, only_carbons):
        message_type = Messages.apply_color_scheme
        expects_response = False
        args = (color_scheme, target, only_carbons)
        self._send_message(message_type, args, expects_response)

    def add_bonds(self, comp_list):
        Bonding.start(comp_list)

    def _send_message(self, message_type, args, expects_response=False):
        request_id = utils.random_request_id()
        serializer = CommandMessageSerializer()
        message = serializer.serialize_message(request_id, message_type, args, self.version_table, expects_response)
        packet = Packet()
        packet.set(self.session_id, Packet.packet_type_message_to_client, self.plugin_id)
        packet.write(message)
        pack = packet.pack()
        if expects_response:
            # Store future to receive any response required
            fut = asyncio.Future()
            self.request_futs[request_id] = fut
        # self.logger.debug(f'Sending Message: {message_type.name} Size: {len(pack)} bytes')
        self.writer.write(pack)
        return request_id

    async def _process_payload(self, request_id: int):
        payload = await self.request_futs[request_id]
        del self.request_futs[request_id]
        result = payload
        if self.deserialize_payloads:
            result = self._deserialize_payload(payload)
        return result

    def _deserialize_payload(self, payload: bytearray):
        serializer = CommandMessageSerializer()
        received_obj_list, _, _ = serializer.deserialize_command(payload, self.version_table)
        return received_obj_list
