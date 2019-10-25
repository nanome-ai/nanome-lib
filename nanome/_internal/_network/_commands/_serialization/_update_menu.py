from nanome._internal._util._serializers import _ArraySerializer
from nanome._internal._ui._serialization import _LayoutNodeSerializer, _UIBaseSerializer, _MenuSerializer

from nanome._internal._util._serializers import _TypeSerializer

class _UpdateMenu(_TypeSerializer):
    def __init__(self):
        self.menu = _MenuSerializer()
        self.array = _ArraySerializer()
        self.layout = _LayoutNodeSerializer()
        self.content = _UIBaseSerializer()

    def version(self):
        return 1

    def name(self):
        return "UpdateMenu"

    def serialize(self, version, value, context):
        if version >= 1:
            context.write_byte(value.index)
        context.write_using_serializer(self.menu, value)
        self.array.set_type(self.layout)
        context.write_using_serializer(self.array, value._get_all_nodes())
        self.array.set_type(self.content)
        context.write_using_serializer(self.array, value._get_all_content())

    def deserialize(self, version, context):
        return None