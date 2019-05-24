from .. import _Label
from nanome._internal._util._serializers import _StringSerializer, _ColorSerializer
from nanome.util.enums import VertAlignOptions, HorizAlignOptions
from . import _UIBaseSerializer
from nanome._internal._util._serializers import _TypeSerializer

class _LabelSerializer(_TypeSerializer):
    def __init__(self):
        self.string = _StringSerializer()
        self.color = _ColorSerializer()

    def version(self):
        return 0

    def name(self):
        return "Label"

    def serialize(self, version, value, context):
        context.write_int(value._content_id)
        context.write_using_serializer(self.string, value._text_value)
        context.write_uint(value._text_vertical_align)
        context.write_uint(value._text_horizontal_align)
        context.write_bool(value._text_auto_size)
        context.write_float(value._text_max_size)
        context.write_float(value._text_min_size)
        context.write_float(value._text_size)
        context.write_using_serializer(self.color, value._text_color)
        context.write_bool(value._text_bold)
        context.write_bool(value._text_italic)
        context.write_bool(value._text_underlined)
        pass

    def deserialize(self, version, context):
        value = _Label._create()
        value._content_id = context.read_int()
        value._text_value = context.read_using_serializer(self.string)
        value._text_vertical_align = VertAlignOptions(context.read_uint())
        value._text_horizontal_align = HorizAlignOptions(context.read_uint())
        value._text_auto_size = context.read_bool()
        value._text_max_size = context.read_float()
        value._text_min_size = context.read_float()
        value._text_size = context.read_float()
        value._text_color = context.read_using_serializer(self.color)
        value._text_bold = context.read_bool()
        value._text_italic = context.read_bool()
        value._text_underlined = context.read_bool()
        return value

_UIBaseSerializer.register_type("Label", _UIBaseSerializer.ContentType.elabel, _LabelSerializer())