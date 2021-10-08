from nanome._internal._util._serializers import _TypeSerializer


class _CharSerializer(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "char"

    def serialize(self, version, value, context):
        context.write_byte(ord(value[0]))

    def deserialize(self, version, context):
        return chr(context.read_byte())
