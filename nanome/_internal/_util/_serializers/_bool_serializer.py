from nanome._internal._util._serializers import _TypeSerializer

class _BoolSerializer(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "bool"

    def serialize(self, version, value, context):
        context.write_bool(value)

    def deserialize(self, version, context):
        return context.read_bool()