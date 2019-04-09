from nanome._internal._ui._serialization import _MenuSerializer, _LayoutNodeSerializer, _UIBaseSerializer
from nanome._internal._util._serializers import _ArraySerializer

from nanome._internal._util._serializers import _TypeSerializer

class _ReceiveMenu(_TypeSerializer):
    def __init__(self):
        self.menu = _MenuSerializer()
        self.array = _ArraySerializer()
        self.layout = _LayoutNodeSerializer()
        self.content = _UIBaseSerializer()

    def version(self):
        return 0

    def name(self):
        return "ReceiveMenu"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        temp_menu = context.read_using_serializer(self.menu)
        self.array.set_type(self.layout)
        temp_nodes = context.read_using_serializer(self.array)
        self.array.set_type(self.content)
        temp_contents = context.read_using_serializer(self.array)
        #returns 3 params as a tuple.
        return temp_menu, temp_nodes, temp_contents