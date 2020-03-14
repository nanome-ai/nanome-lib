from nanome._internal._util._serializers import _TypeSerializer

class _GetMenuTransform(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "GetMenuTransform"

    def serialize(self, version, value, context):
        context.write_byte(value)

    def deserialize(self, version, context):
        return None