from nanome._internal._util._serializers import _TypeSerializer

import sys

if sys.version_info >= (3, 0):
    def to_bytes(value, encoding):
        return bytes(value, 'utf-8')

else:
    def to_bytes(value, encoding):
        return bytearray(value, 'utf-8')

class _StringSerializer(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "string"

    def serialize(self, version, value, context):
        to_write = to_bytes(value, 'utf-8')
        context.write_uint(len(to_write))
        context.write_bytes(to_write)

    def deserialize(self, version, context):
        count = context.read_uint()
        bytes = context.read_bytes(count)
        str = bytes.decode("utf-8")
        return str