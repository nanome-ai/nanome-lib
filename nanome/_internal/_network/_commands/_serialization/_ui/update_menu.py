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
        return 2

    def name(self):
        return "UpdateMenu"

    def serialize(self, version, value, context):
        (menu, shallow) = value
        if version >= 1:
            context.write_byte(menu.index)
        if version >= 2:
            context.write_bool(shallow)

        context.write_using_serializer(self.menu, menu)
        nodes = []
        content = []
        if not shallow:
            nodes = menu._get_all_nodes()
            content = menu._get_all_content()
        self.array.set_type(self.layout)
        context.write_using_serializer(self.array, nodes)
        self.array.set_type(self.content)
        context.write_using_serializer(self.array, content)

    def deserialize(self, version, context):
        return None
