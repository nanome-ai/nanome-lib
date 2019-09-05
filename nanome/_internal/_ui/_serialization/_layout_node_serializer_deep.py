from nanome._internal._util._serializers import _ArraySerializer, _EnumSerializer
from .. import _LayoutNode
from . import _UIBaseSerializer

from nanome._internal._util._serializers import _TypeSerializer

class _LayoutNodeSerializerDeep(_TypeSerializer):
    def __init__(self):
        self._layout_array = _ArraySerializer()
        self._layout_array.set_type(self)
        self._content_serializer = _UIBaseSerializer()
        self._inited = False
        self.padding = _EnumSerializer()
        self.padding.set_type(_LayoutNode.PaddingTypes)
        self.sizing = _EnumSerializer()
        self.sizing.set_type(_LayoutNode.SizingTypes)
        self.layout = _EnumSerializer()
        self.layout.set_type(_LayoutNode.LayoutTypes)

    def version(self):
        return 0

    def name(self):
        return "LayoutNodeDeep"

    def serialize(self, version, value, context):
        context.write_int(value._id)
        context.write_bool(value._enabled)
        context.write_int(value._layer)
        context.write_using_serializer(self.layout, value._layout_orientation)
        context.write_using_serializer(self.sizing, value._sizing_type)
        context.write_float(value._sizing_value)
        context.write_float(value._forward_dist)
        context.write_using_serializer(self.padding, value._padding_type)
        context.write_float(value._padding[0])
        context.write_float(value._padding[1])
        context.write_float(value._padding[2])
        context.write_float(value._padding[3])
        context.write_using_serializer(self._layout_array, value._children)
        has_content = value._content != None
        context.write_bool(has_content)
        if (has_content):
            context.write_using_serializer(self._content_serializer, value._content)

    def deserialize(self, version, context):
        result = _LayoutNode._create()
        result._id = context.read_int()
        result._enabled = context.read_bool()
        result._layer = context.read_int()
        result._layout_orientation = context.read_using_serializer(self.layout)
        result._sizing_type = context.read_using_serializer(self.sizing)
        result._sizing_value = context.read_float()
        result._forward_dist = context.read_float()
        result._padding_type = context.read_using_serializer(self.padding)
        result._padding = (context.read_float(),
                           context.read_float(),
                           context.read_float(),
                           context.read_float())
        result._children = context.read_using_serializer(self._layout_array)
        has_content = context.read_bool()
        if (has_content):
            result._content = context.read_using_serializer(self._content_serializer)
        return result