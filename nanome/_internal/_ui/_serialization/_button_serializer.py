from nanome._internal._util._serializers import _StringSerializer
from nanome.util.enums import VertAlignOptions, HorizAlignOptions
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
        context.write_bool(value._text._bolded)
        context.write_uint((value._text._vertical_align))
        context.write_uint((value._text._horizontal_align))
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
        value._text._bolded = context.read_bool()
        vert = context.read_uint()
        horiz = context.read_uint()
        value._text._vertical_align = VertAlignOptions(vert)
        value._text._horizontal_align = HorizAlignOptions(horiz)
        value._icon._active = context.read_bool()
        value._icon._value_idle = context.read_using_serializer(self.string)
        value._icon._value_selected = context.read_using_serializer(self.string)
        value._icon._value_highlighted = context.read_using_serializer(self.string)
        value._icon._value_selected_highlighted = context.read_using_serializer(self.string)
        value._icon._value_unusable = context.read_using_serializer(self.string)
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
        return value

_UIBaseSerializer.register_type("Button", _UIBaseSerializer.ContentType.ebutton, _ButtonSerializer())