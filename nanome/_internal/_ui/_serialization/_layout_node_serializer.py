from nanome._internal._util._serializers import _ArraySerializer, _IntSerializer
from .. import _LayoutNode

from nanome._internal._util._serializers import _TypeSerializer

class _LayoutNodeSerializer(_TypeSerializer):
    def __init__(self):
        self.array = _ArraySerializer()
        self.array.set_type(_IntSerializer())

    def version(self):
        return 0

    def name(self):
        return "LayoutNode"
    
    def serialize(self, version, value, context):
        context.write_int(value._id)
        context.write_bool(value._enabled)
        context.write_int(value._layer)
        context.write_uint(value._layout_orientation)
        context.write_uint(value._sizing_type)
        context.write_float(value._sizing_value)
        context.write_float(value._forward_dist)
        context.write_uint(value._padding_type)
        context.write_float(value._padding[0])
        context.write_float(value._padding[1])
        context.write_float(value._padding[2])
        context.write_float(value._padding[3])
        child_ids = []
        for child in value._children:
            child_ids.append(child._id)
        context.write_using_serializer(self.array, child_ids)
        content_ids = []
        for content in value._content:
            content_ids.append(content._content_id)
        context.write_using_serializer(self.array, content_ids)

    def deserialize(self, version, context):
        layout_node = _LayoutNode._create()
        layout_node._id = context.read_int()
        layout_node._enabled = context.read_bool()
        layout_node._layer = context.read_int()
        layout_node._layout_orientation = _LayoutNode.LayoutTypes(context.read_uint())
        layout_node._sizing_type = _LayoutNode.SizingTypes(context.read_uint())
        layout_node._sizing_value = context.read_float()
        layout_node._forward_dist = context.read_float()
        layout_node._padding_type = _LayoutNode.PaddingTypes(context.read_uint())
        layout_node._padding = (context.read_float(), 
                                context.read_float(), 
                                context.read_float(), 
                                context.read_float())
        layout_node._child_ids = context.read_using_serializer(self.array)
        layout_node._content_ids = context.read_using_serializer(self.array)
        return layout_node