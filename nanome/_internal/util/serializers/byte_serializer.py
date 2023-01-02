from nanome._internal.util.serializers import TypeSerializer


class _ByteSerializer(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "byte"

    def serialize(self, version, value, context):
        context.write_byte(value)

    def deserialize(self, version, context):
        byte = context.read_byte()
        return byte
