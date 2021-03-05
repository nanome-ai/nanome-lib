from nanome._internal._ui._serialization import _LayoutNodeSerializerDeep
from nanome._internal._util._serializers import _ArraySerializer
from nanome._internal._util._serializers import _TypeSerializer


class _UpdateNode(_TypeSerializer):
    def __init__(self):
        self._array = _ArraySerializer()
        self._node_serializer = _LayoutNodeSerializerDeep()
        self._array.set_type(self._node_serializer)

    def version(self):
        return 1

    def name(self):
        return "SendLayoutNode"

    def serialize(self, version, value, context):
        if version == 0:
            context.write_using_serializer(self._node_serializer, value[0])
        else:
            context.write_using_serializer(self._array, value)

    def deserialize(self, version, context):
        return None
