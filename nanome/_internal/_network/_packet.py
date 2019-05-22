from nanome.util import ImportUtils
import struct

brotli_compression = ImportUtils.check_import_exists("brotli")
if brotli_compression == True:
    import brotli

class _Packet(object):
    packet_header_length = 15
    protocol_version = 0
    packet_type_plugin_list = 0
    packet_type_plugin_connection = 1
    packet_type_client_connection = 2
    packet_type_message_to_plugin = 3
    packet_type_message_to_client = 4
    packet_type_plugin_disconnection = 5
    packet_type_client_disconnection = 6
    packet_type_master_change = 7
    header_pack = struct.Struct('<HIBIi').pack
    header_unpack = struct.Struct('<HIBIi').unpack

    @staticmethod
    def _has_brotli_compression():
        return brotli_compression

    def write_string(self, str):
        self.payload_length += len(str)
        self.payload.extend(str.encode('utf-8'))

    def write(self, data):
        self.payload_length += len(data)
        self.payload.extend(data)

    def pack(self):
        packed = _Packet.header_pack(self.version, self.session_id, self.packet_type, self.plugin_id, self.payload_length)
        packed += self.payload
        return packed

    def compress(self):
        if brotli_compression == False:
            return
        self.payload = brotli.compress(self.payload)
        self.payload_length = len(self.payload)

    def decompress(self):
        if brotli_compression == False:
            return
        self.payload = brotli.decompress(self.payload)
        self.payload_length = len(self.payload)

    def get_header(self, data):
        if data.has_enough(_Packet.packet_header_length):
            bytes = data.read_bytes(_Packet.packet_header_length)
            unpacked = _Packet.header_unpack(bytes)
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

    def __len__(self):
        return self.payload_length + _Packet.packet_header_length

    def __init__(self):
        self.version = _Packet.protocol_version
        self.session_id = 0
        self.packet_type = _Packet.packet_type_plugin_list
        self.plugin_id = 0
        self.payload_length = 0
        self.payload = bytearray()
        pass