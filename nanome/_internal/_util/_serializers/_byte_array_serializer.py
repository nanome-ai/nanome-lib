from nanome._internal._util._serializers import _TypeSerializer


class _ByteArraySerializer(_TypeSerializer):
    def version(self):
        return 0

    def name(self):
        return "ByteArray"

    def serialize(self, version, value, context):
        context.write_byte_array(value)

    def deserialize(self, version, context):
        return context.read_byte_Array()
