import sys
import struct
import zlib
from nanome._internal.enum_utils import IntEnum


class PacketTypes(IntEnum):
    plugin_list = 0
    plugin_connection = 1
    client_connection = 2
    message_to_plugin = 3
    message_to_client = 4
    plugin_disconnection = 5
    client_disconnection = 6
    master_change = 7
    keep_alive = 8
    logs_request = 9
    live_logs = 10


class Packet(object):
    packet_header_length = 15
    protocol_version = 0
    packet_type_plugin_list = PacketTypes.plugin_list
    packet_type_plugin_connection = PacketTypes.plugin_connection
    packet_type_client_connection = PacketTypes.client_connection
    packet_type_message_to_plugin = PacketTypes.message_to_plugin
    packet_type_message_to_client = PacketTypes.message_to_client
    packet_type_plugin_disconnection = PacketTypes.plugin_disconnection
    packet_type_client_disconnection = PacketTypes.client_disconnection
    packet_type_master_change = PacketTypes.master_change
    packet_type_keep_alive = PacketTypes.keep_alive
    packet_type_logs_request = PacketTypes.logs_request
    packet_type_live_logs = PacketTypes.live_logs
    header_pack = struct.Struct('<HIBIi').pack
    header_unpack = struct.Struct('<HIBIi').unpack
    __compress_obj = zlib.compressobj(4, zlib.DEFLATED, -zlib.MAX_WBITS)

    def __repr__(self):
        packet_type = PacketTypes(self.packet_type).name
        return (
            "Packet(version={}, session_id={}, packet_type={}, plugin_id={}, payload_length={})"
        ).format(self.version, self.session_id, packet_type, self.plugin_id, self.payload_length)

    def __init__(self):
        self.version = Packet.protocol_version
        self.session_id = 0
        self.packet_type = Packet.packet_type_plugin_list
        self.plugin_id = 0
        self.payload_length = 0
        self.payload = bytearray()

    def write_string(self, str):
        encoded = str.encode('utf-8')
        self.payload_length += len(encoded)
        self.payload.extend(encoded)

    def write(self, data):
        self.payload_length += len(data)
        self.payload.extend(data)

    def pack(self):
        packed = Packet.header_pack(
            self.version, self.session_id, self.packet_type, self.plugin_id, self.payload_length)
        packed += self.payload
        return packed

    def compress(self):
        if sys.version_info.major == 2:
            # TODO: Figure out why/if this is needed.
            self.payload = str(self.payload)
        self.payload = Packet.__compress_obj.compress(self.payload) + Packet.__compress_obj.flush(zlib.Z_FULL_FLUSH)
        self.payload_length = len(self.payload)

    def decompress(self):
        self.payload = zlib.decompress(self.payload, -zlib.MAX_WBITS)
        self.payload_length = len(self.payload)

    def get_header(self, data):
        if data.has_enough(Packet.packet_header_length):
            bytes = data.read_bytes(Packet.packet_header_length)
            unpacked = Packet.header_unpack(bytes)
            self.version = unpacked[0]
            self.session_id = unpacked[1]
            self.packet_type = unpacked[2]
            self.plugin_id = unpacked[3]
            self.payload_length = unpacked[4]
            return True
        return False

    def get_payload(self, data):
        if data.has_enough(self.payload_length):
            received = data.read_bytes(self.payload_length)
            self.payload = received
            return True
        return False

    def set(self, session_id, type, plugin_id):
        self.session_id = session_id
        self.packet_type = type
        self.plugin_id = plugin_id

    @staticmethod
    def _compression_type():
        return 0

    def __len__(self):
        return self.payload_length + Packet.packet_header_length
