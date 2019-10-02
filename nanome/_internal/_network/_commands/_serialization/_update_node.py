from nanome._internal._ui._serialization import _LayoutNodeSerializerDeep

from nanome._internal._util._serializers import _TypeSerializer

class _UpdateNode(_TypeSerializer):
    def __init__(self):
        self.node_serializer = _LayoutNodeSerializerDeep()

    def version(self):
        return 0

    def name(self):
        return "SendLayoutNode"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.node_serializer, value)

    def deserialize(self, version, context):
        return None