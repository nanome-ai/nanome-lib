from nanome._internal._util._serializers import _ArraySerializer, _IntSerializer, _EnumSerializer
from .. import _LayoutNode

from nanome._internal._util._serializers import _TypeSerializer

class _LayoutNodeSerializer(_TypeSerializer):
    def __init__(self):
        self.enum = _EnumSerializer()

    def version(self):
        return 1

    def name(self):
        return "LayoutNode"
    
    def serialize(self, version, value, context):
        context.write_int(value._id)
        context.write_bool(value._enabled)
        context.write_int(value._layer)
        self.enum.set_type(_LayoutNode.LayoutTypes)
        context.write_using_serializer(self.enum, value._layout_orientation)
        self.enum.set_type(_LayoutNode.SizingTypes)
        context.write_using_serializer(self.enum, value._sizing_type)
        context.write_float(value._sizing_value)
        context.write_float(value._forward_dist)
        self.enum.set_type(_LayoutNode.PaddingTypes)
        context.write_using_serializer(self.enum, value._padding_type)
        context.write_float(value._padding[0])
        context.write_float(value._padding[1])
        context.write_float(value._padding[2])
        context.write_float(value._padding[3])
        child_ids = []
        for child in value._children:
            child_ids.append(child._id)
        context.write_int_array(child_ids)
        has_content = value._content != None
        context.write_bool(has_content)
        if (has_content):
            content_id = value._content._content_id
            if (version == 0):
                content_id = (context._plugin_id << 24) & 0x7FFFFFFF
                content_id |= value._content._content_id
            context.write_int(content_id)

    def deserialize(self, version, context):
        layout_node = _LayoutNode._create()
        layout_node._id = context.read_int()
        layout_node._enabled = context.read_bool()
        layout_node._layer = context.read_int()
        self.enum.set_type(_LayoutNode.LayoutTypes)
        layout_node._layout_orientation = context.read_using_serializer(self.enum)
        self.enum.set_type(_LayoutNode.SizingTypes)
        layout_node._sizing_type = context.read_using_serializer(self.enum)
        layout_node._sizing_value = context.read_float()
        layout_node._forward_dist = context.read_float()
        self.enum.set_type(_LayoutNode.PaddingTypes)
        layout_node._padding_type = context.read_using_serializer(self.enum)
        layout_node._padding = (context.read_float(), 
                                context.read_float(), 
                                context.read_float(), 
                                context.read_float())
        layout_node._child_ids = context.read_int_array()
        has_content = context.read_bool()
        if (has_content):
            layout_node._content_id = context.read_int()
            if (version == 0):
                id_mask = 0x00FFFFFF
                layout_node._content_id &= id_mask
        else:
            layout_node._content_id = None
        return layout_node