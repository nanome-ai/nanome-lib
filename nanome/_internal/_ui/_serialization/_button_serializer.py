from nanome._internal._util._serializers import _StringSerializer
from nanome.util.text_settings import VertAlignOptions, HorizAlignOptions
from . import _UIBaseSerializer
from .. import _Button

from nanome._internal._util._serializers import _TypeSerializer

class _ButtonSerializer(_TypeSerializer):
    def __init__(self):
        self.string = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "Button"

    def serialize(self, version, value, context):
        context.write_int(value._content_id)

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

    def deserialize(self, version, context):
        value = _Button._create()
        value._content_id = context.read_int()

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
        return value

_UIBaseSerializer.register_type("Button", _UIBaseSerializer.ContentType.ebutton, _ButtonSerializer())