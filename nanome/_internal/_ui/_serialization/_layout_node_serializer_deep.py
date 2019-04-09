from nanome._internal._util._serializers import _ArraySerializer
from .. import _LayoutNode
from . import _UIBaseSerializer

from nanome._internal._util._serializers import _TypeSerializer

class _LayoutNodeSerializerDeep(_TypeSerializer):
    def __init__(self):
        self._layout_array = _ArraySerializer()
        self._content_array = _ArraySerializer()
        self._inited = False

    def version(self):
        return 0

    def name(self):
        return "LayoutNodeDeep"

    def _init_serializers(self):
        if (self._inited == False):
            self._inited = True
            self._layout_array.set_type(_LayoutNodeSerializerDeep())
            self._content_array.set_type(_UIBaseSerializer())

    def serialize(self, version, value, context):
        self._init_serializers()

        context.write_int(value._id)
        context.write_bool(value._enabled)
        context.write_int(value._layer)
        context.write_int(value._layout_orientation)
        context.write_int(value._sizing_type)
        context.write_float(value._sizing_value)
        context.write_float(value._forward_dist)
        context.write_int(value._padding_type)
        context.write_float(value._padding[0])
        context.write_float(value._padding[1])
        context.write_float(value._padding[2])
        context.write_float(value._padding[3])
        context.write_using_serializer(self._layout_array, value._children)
        context.write_using_serializer(self._content_array, value._content)

    def deserialize(self, version, context):
        self._init_serializers()

        result = _LayoutNode._create()
        result._id = context.read_int()
        result._enabled = context.read_bool()
        result._layer = context.read_int()
        result._layout_orientation = _LayoutNode.LayoutTypes(context.read_int())
        result._sizing_type = _LayoutNode.SizingTypes(context.read_int())
        result._sizing_value = context.read_float()
        result._forward_dist = context.read_float()
        result._padding_type = _LayoutNode.PaddingTypes(context.read_int())
        result._padding = (context.read_float(),
                           context.read_float(),
                           context.read_float(),
                           context.read_float())
        result._children = context.read_using_serializer(self._layout_array)
        result._contents = context.read_using_serializer(self._content_array)
        return result