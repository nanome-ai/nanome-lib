from nanome._internal._util._serializers import _StringSerializer, _ColorSerializer, _Vector3Serializer, _CachedImageSerializer
from nanome.util.enums import VertAlignOptions, HorizAlignOptions, ToolTipPositioning
from . import _UIBaseSerializer
from .. import _Button

from nanome._internal._util._serializers import _TypeSerializer

class _ButtonSerializer(_TypeSerializer):
    def __init__(self):
        self.string = _StringSerializer()
        self.color = _ColorSerializer()
        self.vector = _Vector3Serializer()
        self.cached_image = _CachedImageSerializer()

    def version(self):
        return 6

    def name(self):
        return "Button"

    def serialize(self, version, button, context):
        if version == 0:
            safe_id = (context._plugin_id << 24) & 0x7FFFFFFF
            safe_id |= button._content_id
        else:
            safe_id = button._content_id
        context.write_int(safe_id)
        if version >= 3:
            context.write_using_serializer(self.string, button._name)
        context.write_bool(button._selected)
        context.write_bool(button._unusable)
        if version >= 4:
            context.write_bool(button._disable_on_press)
        if version >= 5:
            context.write_bool(button._toggle_on_press)
        context.write_bool(button._text._active)
        context.write_using_serializer(self.string, button._text._value._idle)
        context.write_using_serializer(self.string, button._text._value._selected)
        context.write_using_serializer(self.string, button._text._value._highlighted)
        context.write_using_serializer(self.string, button._text._value._selected_highlighted)
        context.write_using_serializer(self.string, button._text._value._unusable)
        context.write_bool(button._text._auto_size)
        context.write_float(button._text._min_size)
        context.write_float(button._text._max_size)
        context.write_float(button._text._size)
        context.write_bool(button._text._underlined)
        if version >= 3:
            context.write_bool(button._text._ellipsis) #default on
            context.write_bool(button._text._bold._idle)
            context.write_bool(button._text._bold._selected)
            context.write_bool(button._text._bold._highlighted)
            context.write_bool(button._text._bold._selected_highlighted)
            context.write_bool(button._text._bold._unusable)
            context.write_using_serializer(self.color, button._text._color._idle)
            context.write_using_serializer(self.color, button._text._color._selected)
            context.write_using_serializer(self.color, button._text._color._highlighted)
            context.write_using_serializer(self.color, button._text._color._selected_highlighted)
            context.write_using_serializer(self.color, button._text._color._unusable)
            context.write_float(button._text._padding_top)
            context.write_float(button._text._padding_bottom)
            context.write_float(button._text._padding_left)
            context.write_float(button._text._padding_right)
            context.write_float(button._text._line_spacing)
        else:
            context.write_bool(button._text._bold._idle)
        context.write_uint((button._text._vertical_align))
        context.write_uint((button._text._horizontal_align))

        if version >= 2:
            context.write_bool(button._icon._active)
            if version >= 6:
                context.write_using_serializer(self.cached_image, button._icon._value._idle)
                context.write_using_serializer(self.cached_image, button._icon._value._selected)
                context.write_using_serializer(self.cached_image, button._icon._value._highlighted)
                context.write_using_serializer(self.cached_image, button._icon._value._selected_highlighted)
                context.write_using_serializer(self.cached_image, button._icon._value._unusable)
            else:
                context.write_using_serializer(self.string, button._icon._value._idle)
                context.write_using_serializer(self.string, button._icon._value._selected)
                context.write_using_serializer(self.string, button._icon._value._highlighted)
                context.write_using_serializer(self.string, button._icon._value._selected_highlighted)
                context.write_using_serializer(self.string, button._icon._value._unusable)
                data = []
                if (button._icon._value._idle != ""):
                    with open(button._icon._value._idle, "rb") as f:
                        data = f.read()
                context.write_byte_array(data)
                data = []
                if (button._icon._value._selected != ""):
                    with open(button._icon._value._selected, "rb") as f:
                        data = f.read()
                context.write_byte_array(data)
                data = []
                if (button._icon._value._highlighted != ""):
                    with open(button._icon._value._highlighted, "rb") as f:
                        data = f.read()
                context.write_byte_array(data)
                data = []
                if (button._icon._value._selected_highlighted != ""):
                    with open(button._icon._value._selected_highlighted, "rb") as f:
                        data = f.read()
                context.write_byte_array(data)
                data = []
                if (button._icon._value._unusable != ""):
                    with open(button._icon._value._unusable, "rb") as f:
                        data = f.read()
                context.write_byte_array(data)

            context.write_using_serializer(self.color, button._icon._color._idle)
            context.write_using_serializer(self.color, button._icon._color._selected)
            context.write_using_serializer(self.color, button._icon._color._highlighted)
            context.write_using_serializer(self.color, button._icon._color._selected_highlighted)
            context.write_using_serializer(self.color, button._icon._color._unusable)
            context.write_float(button._icon._sharpness)
            context.write_float(button._icon._size)
            context.write_float(button._icon._ratio)
            context.write_using_serializer(self.vector, button._icon._position)
            context.write_using_serializer(self.vector, button._icon._rotation)
        if version >= 3:
            context.write_bool(button._mesh._active)
            context.write_bool(button._mesh._enabled._idle)
            context.write_bool(button._mesh._enabled._selected)
            context.write_bool(button._mesh._enabled._highlighted)
            context.write_bool(button._mesh._enabled._selected_highlighted)
            context.write_bool(button._mesh._enabled._unusable)
            context.write_using_serializer(self.color, button._mesh._color._idle)
            context.write_using_serializer(self.color, button._mesh._color._selected)
            context.write_using_serializer(self.color, button._mesh._color._highlighted)
            context.write_using_serializer(self.color, button._mesh._color._selected_highlighted)
            context.write_using_serializer(self.color, button._mesh._color._unusable)
            context.write_bool(button._outline._active)
            context.write_float(button._outline._size._idle)
            context.write_float(button._outline._size._selected)
            context.write_float(button._outline._size._highlighted)
            context.write_float(button._outline._size._selected_highlighted)
            context.write_float(button._outline._size._unusable)
            context.write_using_serializer(self.color, button._outline._color._idle)
            context.write_using_serializer(self.color, button._outline._color._selected)
            context.write_using_serializer(self.color, button._outline._color._highlighted)
            context.write_using_serializer(self.color, button._outline._color._selected_highlighted)
            context.write_using_serializer(self.color, button._outline._color._unusable)
            context.write_using_serializer(self.string, button._tooltip._title)
            context.write_using_serializer(self.string, button._tooltip._content)
            context.write_using_serializer(self.vector, button._tooltip._bounds)
            context.write_uint(button._tooltip._positioning_target)
            context.write_uint(button._tooltip._positioning_origin)
        if version >= 5:
            context.write_bool(button._switch._active)
            context.write_using_serializer(self.color, button._switch._on_color)
            context.write_using_serializer(self.color, button._switch._off_color)

    def deserialize(self, version, context):
        value = _Button._create()
        value._content_id = context.read_int()
        if (version == 0):
            id_mask = 0x00FFFFFF
            value._content_id &= id_mask
        if version >= 3:
            value._name = context.read_using_serializer(self.string)
        value._selected = context.read_bool()
        value._unusable = context.read_bool()
        if version >= 4:
            value._disable_on_press = context.read_bool()
        if version >= 5:
            value._toggle_on_press = context.read_bool()
        value._text._active = context.read_bool()
        value._text._value._idle = context.read_using_serializer(self.string)
        value._text._value._selected = context.read_using_serializer(self.string)
        value._text._value._highlighted = context.read_using_serializer(self.string)
        value._text._value._selected_highlighted = context.read_using_serializer(self.string)
        value._text._value._unusable = context.read_using_serializer(self.string)
        value._text._auto_size = context.read_bool()
        value._text._min_size = context.read_float()
        value._text._max_size = context.read_float()
        value._text._size = context.read_float()
        value._text._underlined = context.read_bool()
        if version >= 3:
            value._text._ellipsis = context.read_bool() #default on
            value._text._bold._idle = context.read_bool()
            value._text._bold._selected = context.read_bool()
            value._text._bold._highlighted = context.read_bool()
            value._text._bold._selected_highlighted = context.read_bool()
            value._text._bold._unusable = context.read_bool()
            value._text._color._idle = context.read_using_serializer(self.color)
            value._text._color._selected = context.read_using_serializer(self.color)
            value._text._color._highlighted = context.read_using_serializer(self.color)
            value._text._color._selected_highlighted = context.read_using_serializer(self.color)
            value._text._color._unusable = context.read_using_serializer(self.color)
            value._text._padding_top = context.read_float()
            value._text._padding_bottom = context.read_float()
            value._text._padding_left = context.read_float()
            value._text._padding_right = context.read_float()
            value._text._line_spacing = context.read_float()
        else:
            bolded = context.read_bool()
            value._text._bold._set_all(bolded)
        vert = context.read_uint()
        horiz = context.read_uint()
        value._text._vertical_align = VertAlignOptions.safe_cast(vert)
        value._text._horizontal_align = HorizAlignOptions.safe_cast(horiz)

        if version >= 2:
            value._icon._active = context.read_bool()
            if version < 6:
                value._icon._value._idle = context.read_using_serializer(self.string)
                value._icon._value._selected = context.read_using_serializer(self.string)
                value._icon._value._highlighted = context.read_using_serializer(self.string)
                value._icon._value._selected_highlighted = context.read_using_serializer(self.string)
                value._icon._value._unusable = context.read_using_serializer(self.string)
                context.read_byte_array()
                context.read_byte_array()
                context.read_byte_array()
                context.read_byte_array()
                context.read_byte_array()
            else:
                context.read_using_serializer(self.cached_image)
                context.read_using_serializer(self.cached_image)
                context.read_using_serializer(self.cached_image)
                context.read_using_serializer(self.cached_image)
                context.read_using_serializer(self.cached_image)

            value._icon._color._idle = context.read_using_serializer(self.color)
            value._icon._color._selected = context.read_using_serializer(self.color)
            value._icon._color._highlighted = context.read_using_serializer(self.color)
            value._icon._color._selected_highlighted = context.read_using_serializer(self.color)
            value._icon._color._unusable = context.read_using_serializer(self.color)
            value._icon._sharpness = context.read_float()
            value._icon._size = context.read_float()
            value._icon._ratio = context.read_float()
            value._icon._position = context.read_using_serializer(self.vector)
            value._icon._rotation = context.read_using_serializer(self.vector)
        if version >= 3:
            value._mesh._active = context.read_bool()
            value._mesh._enabled._idle = context.read_bool()
            value._mesh._enabled._selected = context.read_bool()
            value._mesh._enabled._highlighted = context.read_bool()
            value._mesh._enabled._selected_highlighted = context.read_bool()
            value._mesh._enabled._unusable = context.read_bool()
            value._mesh._color._idle = context.read_using_serializer(self.color)
            value._mesh._color._selected = context.read_using_serializer(self.color)
            value._mesh._color._highlighted = context.read_using_serializer(self.color)
            value._mesh._color._selected_highlighted = context.read_using_serializer(self.color)
            value._mesh._color._unusable = context.read_using_serializer(self.color)
            value._outline._active = context.read_bool()
            value._outline._size._idle = context.read_float()
            value._outline._size._selected = context.read_float()
            value._outline._size._highlighted = context.read_float()
            value._outline._size._selected_highlighted = context.read_float()
            value._outline._size._unusable = context.read_float()
            value._outline._color._idle = context.read_using_serializer(self.color)
            value._outline._color._selected = context.read_using_serializer(self.color)
            value._outline._color._highlighted = context.read_using_serializer(self.color)
            value._outline._color._selected_highlighted = context.read_using_serializer(self.color)
            value._outline._color._unusable = context.read_using_serializer(self.color)
            value._tooltip._title = context.read_using_serializer(self.string)
            value._tooltip._content = context.read_using_serializer(self.string)
            value._tooltip._bounds = context.read_using_serializer(self.vector)
            value._tooltip._positioning_target = ToolTipPositioning.safe_cast(context.read_uint())
            value._tooltip._positioning_origin = ToolTipPositioning.safe_cast(context.read_uint())
        if version >= 5:
            value._switch._active = context.read_bool()
            value._switch._on_color = context.read_using_serializer(self.color)
            value._switch._off_color = context.read_using_serializer(self.color)
        return value

_UIBaseSerializer.register_type("Button", _UIBaseSerializer.ContentType.ebutton, _ButtonSerializer())