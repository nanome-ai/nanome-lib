from nanome._internal._util._serializers import _StringSerializer, _ColorSerializer, _Vector3Serializer
from nanome.util.enums import VertAlignOptions, HorizAlignOptions, ToolTipPositioning
from . import _UIBaseSerializer
from .. import _Button

from nanome._internal._util._serializers import _TypeSerializer

class _ButtonSerializer(_TypeSerializer):
    def __init__(self):
        self.string = _StringSerializer()
        self.color = _ColorSerializer()
        self.vector = _Vector3Serializer()

    def version(self):
        return 2

    def name(self):
        return "Button"

    def serialize(self, version, value, context):
        if (version == 0 ):
            safe_id = (context._plugin_id << 24) & 0x7FFFFFFF
            safe_id |= value._content_id
        else:
            safe_id = value._content_id
        context.write_int(safe_id)

        context.write_bool(value._selected)
        context.write_bool(value._unusable)
        context.write_bool(value._text._active)
        context.write_using_serializer(self.string, value._text._value_idle)
        context.write_using_serializer(self.string, value._text._value_selected)
        context.write_using_serializer(self.string, value._text._value_highlighted)
        context.write_using_serializer(self.string, value._text._value_selected_highlighted)
        context.write_using_serializer(self.string, value._text._value_unusable)
        context.write_bool(value._text._auto_size)
        context.write_float(value._text._min_size)
        context.write_float(value._text._max_size)
        context.write_float(value._text._size)
        context.write_bool(value._text._underlined)
        if version >= 3:
            context.write_bool(value._TextEllipsis) #default on
            context.write_bool(value._TextBoldIdle)
            context.write_bool(value._TextBoldSelected)
            context.write_bool(value._TextBoldHighlighted)
            context.write_bool(value._TextBoldSelectedHighlighted)
            context.write_bool(value._TextBoldUnusable)
            context.write_using_serializer(self.color, value._TextColorIdle)
            context.write_using_serializer(self.color, value._TextColorSelected)
            context.write_using_serializer(self.color, value._TextColorHighlighted)
            context.write_using_serializer(self.color, value._TextColorSelectedHighlighted)
            context.write_using_serializer(self.color, value._TextColorUnusable)
            context.write_float(value._TextPaddingTop)
            context.write_float(value._TextPaddingBottom)
            context.write_float(value._TextPaddingLeft)
            context.write_float(value._TextPaddingRight)
            context.write_float(value._TextLineSpacing)
        else:
            context.write_bool(value._TextBoldIdle)
        context.write_uint((value._text._vertical_align))
        context.write_uint((value._text._horizontal_align))

        if version >= 2:
            context.write_bool(value._icon._active)
            context.write_using_serializer(self.string, value._icon._value_idle)
            context.write_using_serializer(self.string, value._icon._value_selected)
            context.write_using_serializer(self.string, value._icon._value_highlighted)
            context.write_using_serializer(self.string, value._icon._value_selected_highlighted)
            context.write_using_serializer(self.string, value._icon._value_unusable)
            data = []
            if (value._icon._value_idle != ""):
                with open(value._icon._value_idle, "rb") as f:
                    data = f.read()
            context.write_byte_array(data)
            data = []
            if (value._icon._value_selected != ""):
                with open(value._icon._value_selected, "rb") as f:
                    data = f.read()
            context.write_byte_array(data)
            data = []
            if (value._icon._value_highlighted != ""):
                with open(value._icon._value_highlighted, "rb") as f:
                    data = f.read()
            context.write_byte_array(data)
            data = []
            if (value._icon._value_selected_highlighted != ""):
                with open(value._icon._value_selected_highlighted, "rb") as f:
                    data = f.read()
            context.write_byte_array(data)
            data = []
            if (value._icon._value_unusable != ""):
                with open(value._icon._value_unusable, "rb") as f:
                    data = f.read()
            context.write_byte_array(data)
            context.write_using_serializer(self.color, value._icon._color_idle)
            context.write_using_serializer(self.color, value._icon._color_selected)
            context.write_using_serializer(self.color, value._icon._color_highlighted)
            context.write_using_serializer(self.color, value._icon._color_selected_highlighted)
            context.write_using_serializer(self.color, value._icon._color_unusable)
            context.write_float(value._icon._sharpness)
            context.write_float(value._icon._size)
            context.write_float(value._icon._ratio)
            context.write_using_serializer(self.vector, value._icon._position)
            context.write_using_serializer(self.vector, value._icon._rotation)
            if version >= 3:
                context.write_bool(value._MeshActive)
                context.write_bool(value._MeshActiveIdle)
                context.write_bool(value._MeshActiveSelected)
                context.write_bool(value._MeshActiveHighlighted)
                context.write_bool(value._MeshActiveSelectedHighlighted)
                context.write_bool(value._MeshActiveUnusable)
                context.write_using_serializer(self.color, value._MeshColorIdle)
                context.write_using_serializer(self.color, value._MeshColorSelected)
                context.write_using_serializer(self.color, value._MeshColorHighlighted)
                context.write_using_serializer(self.color, value._MeshColorSelectedHighlighted)
                context.write_using_serializer(self.color, value._MeshColorUnusable)
                context.write_bool(value._OutlineActive)
                context.write_float(value._OutlineSizeIdle)
                context.write_float(value._OutlineSizeSelected)
                context.write_float(value._OutlineSizeHighlighted)
                context.write_float(value._OutlineSizeSelectedHighlighted)
                context.write_float(value._OutlineSizeUnusable)
                context.write_using_serializer(self.color, value._OutlineColorIdle)
                context.write_using_serializer(self.color, value._OutlineColorSelected)
                context.write_using_serializer(self.color, value._OutlineColorHighlighted)
                context.write_using_serializer(self.color, value._OutlineColorSelectedHighlighted)
                context.write_using_serializer(self.color, value._OutlineColorUnusable)
                context.write_using_serializer(self.string, value._TooltipTitleValue)
                context.write_using_serializer(self.string, value._TooltipContentValue)
                context.write_using_serializer(self.vector, value._TooltipBoundSize)
                context.write_uint(value._TooltipPositioningTarget)
                context.write_uint(value._TooltipPositioningOrigin)

    def deserialize(self, version, context):
        value = _Button._create()
        value._content_id = context.read_int()
        if (version == 0):
            id_mask = 0x00FFFFFF
            value._content_id &= id_mask

        value._selected = context.read_bool()
        value._unusable = context.read_bool()
        value._text._active = context.read_bool()
        value._text._value_idle = context.read_using_serializer(self.string)
        value._text._value_selected = context.read_using_serializer(self.string)
        value._text._value_highlighted = context.read_using_serializer(self.string)
        value._text._value_selected_highlighted = context.read_using_serializer(self.string)
        value._text._value_unusable = context.read_using_serializer(self.string)
        value._text._auto_size = context.read_bool()
        value._text._min_size = context.read_float()
        value._text._max_size = context.read_float()
        value._text._size = context.read_float()
        value._text._underlined = context.read_bool()
        if version >= 3:
            value._TextEllipsis = context.read_bool() #default on
            value._TextBoldIdle = context.read_bool()
            value._TextBoldSelected = context.read_bool()
            value._TextBoldHighlighted = context.read_bool()
            value._TextBoldSelectedHighlighted = context.read_bool()
            value._TextBoldUnusable = context.read_bool()
            value._TextColorIdle = context.read_using_serializer(self.color)
            value._TextColorSelected = context.read_using_serializer(self.color)
            value._TextColorHighlighted = context.read_using_serializer(self.color)
            value._TextColorSelectedHighlighted = context.read_using_serializer(self.color)
            value._TextColorUnusable = context.read_using_serializer(self.color)
            value._TextPaddingTop = context.read_float()
            value._TextPaddingBottom = context.read_float()
            value._TextPaddingLeft = context.read_float()
            value._TextPaddingRight = context.read_float()
            value._TextLineSpacing = context.read_float()
        else:
            bolded = context.read_bool()
            value._TextBoldIdle = bolded
            value._TextBoldSelected = bolded
            value._TextBoldHighlighted = bolded
            value._TextBoldSelectedHighlighted = bolded
        vert = context.read_uint()
        horiz = context.read_uint()
        value._text._vertical_align = VertAlignOptions(vert)
        value._text._horizontal_align = HorizAlignOptions(horiz)

        if version >= 2:
            value._icon._active = context.read_bool()
            value._icon._value_idle = context.read_using_serializer(self.string)
            value._icon._value_selected = context.read_using_serializer(self.string)
            value._icon._value_highlighted = context.read_using_serializer(self.string)
            value._icon._value_selected_highlighted = context.read_using_serializer(self.string)
            value._icon._value_unusable = context.read_using_serializer(self.string)
            context.read_byte_array()
            context.read_byte_array()
            context.read_byte_array()
            context.read_byte_array()
            context.read_byte_array()
            value._icon._color_idle = context.read_using_serializer(self.color)
            value._icon._color_selected = context.read_using_serializer(self.color)
            value._icon._color_highlighted = context.read_using_serializer(self.color)
            value._icon._color_selected_highlighted = context.read_using_serializer(self.color)
            value._icon._color_unusable = context.read_using_serializer(self.color)
            value._icon._sharpness = context.read_float()
            value._icon._size = context.read_float()
            value._icon._ratio = context.read_float()
            value._icon._position = context.read_using_serializer(self.vector)
            value._icon._rotation = context.read_using_serializer(self.vector)
            if version >= 3:
                value._MeshActive = context.read_bool()
                value._MeshActiveIdle = context.read_bool()
                value._MeshActiveSelected = context.read_bool()
                value._MeshActiveHighlighted = context.read_bool()
                value._MeshActiveSelectedHighlighted = context.read_bool()
                value._MeshActiveUnusable = context.read_bool()
                value._MeshColorIdle = context.read_using_serializer(self.color)
                value._MeshColorSelected = context.read_using_serializer(self.color)
                value._MeshColorHighlighted = context.read_using_serializer(self.color)
                value._MeshColorSelectedHighlighted = context.read_using_serializer(self.color)
                value._MeshColorUnusable = context.read_using_serializer(self.color)
                value._OutlineActive = context.read_bool()
                value._OutlineSizeIdle = context.read_float()
                value._OutlineSizeSelected = context.read_float()
                value._OutlineSizeHighlighted = context.read_float()
                value._OutlineSizeSelectedHighlighted = context.read_float()
                value._OutlineSizeUnusable = context.read_float()
                value._OutlineColorIdle = context.read_using_serializer(self.color)
                value._OutlineColorSelected = context.read_using_serializer(self.color)
                value._OutlineColorHighlighted = context.read_using_serializer(self.color)
                value._OutlineColorSelectedHighlighted = context.read_using_serializer(self.color)
                value._OutlineColorUnusable = context.read_using_serializer(self.color)
                value._TooltipTitleValue = context.read_using_serializer(self.string)
                value._TooltipContentValue = context.read_using_serializer(self.string)
                value._TooltipBoundSize = context.read_using_serializer(self.vector)
                value._TooltipPositioningTarget = ToolTipPositioning(context.read_uint())
                value._TooltipPositioningOrigin = ToolTipPositioning(context.read_uint())
        return value

_UIBaseSerializer.register_type("Button", _UIBaseSerializer.ContentType.ebutton, _ButtonSerializer())