from ..._internal.ui import _Button, _Dropdown, _DropdownItem, _Image, _Label, _LayoutNode, _LoadingBar, _Menu, _Mesh, _Slider, _TextInput, _UIList
from nanome._internal.enum_utils import IntEnum
from nanome._internal.serializer_fields import ArrayField, TypeSerializer, ColorField, ByteField, CachedImageField, StringField, Vector3Field
import logging
logger = logging.getLogger(__name__)


class UIBaseSerializer(TypeSerializer):
    class ContentType(IntEnum):
        ebutton = 0
        emesh = 1
        eslider = 2
        etextInput = 3
        elabel = 4
        elist = 5
        eimage = 6
        eloadingBar = 7
        edropdown = 8

    registered_classes = dict()
    registered_serializers = dict()

    @classmethod
    def register_type(cls, classname, enum_value, serializer):
        cls.registered_classes[classname] = enum_value
        cls.registered_serializers[enum_value] = serializer

    def version(self):
        return 0

    def name(self):
        return "UIContent"

    def serialize(self, version, value, context):
        if value == None:
            return
        try:
            ui_type = UIBaseSerializer.registered_classes[type(
                value).__name__]
            serializer = UIBaseSerializer.registered_serializers[ui_type]
        except:
            logger.error("Trying to serialize unknown UI type: {}".format(type(value).__name__))
            return
        context.write_uint(ui_type)
        context.write_using_serializer(serializer, value)

    def deserialize(self, version, context):
        ui_type = UIBaseSerializer.ContentType(context.read_uint())
        try:
            serializer = UIBaseSerializer.registered_serializers[ui_type]
        except:
            logger.error("Trying to deserialize unknown UI type: {}".format(ui_type))
            return
        return context.read_using_serializer(serializer)


class ButtonSerializer(TypeSerializer):
    def __init__(self):
        self.string = StringField()
        self.color = ColorField()
        self.vector = Vector3Field()
        self.cached_image = CachedImageField()

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
        context.write_using_serializer(
            self.string, button._text._value._selected)
        context.write_using_serializer(
            self.string, button._text._value._highlighted)
        context.write_using_serializer(
            self.string, button._text._value._selected_highlighted)
        context.write_using_serializer(
            self.string, button._text._value._unusable)
        context.write_bool(button._text._auto_size)
        context.write_float(button._text._min_size)
        context.write_float(button._text._max_size)
        context.write_float(button._text._size)
        context.write_bool(button._text._underlined)
        if version >= 3:
            context.write_bool(button._text._ellipsis)  # default on
            context.write_bool(button._text._bold._idle)
            context.write_bool(button._text._bold._selected)
            context.write_bool(button._text._bold._highlighted)
            context.write_bool(button._text._bold._selected_highlighted)
            context.write_bool(button._text._bold._unusable)
            context.write_using_serializer(
                self.color, button._text._color._idle)
            context.write_using_serializer(
                self.color, button._text._color._selected)
            context.write_using_serializer(
                self.color, button._text._color._highlighted)
            context.write_using_serializer(
                self.color, button._text._color._selected_highlighted)
            context.write_using_serializer(
                self.color, button._text._color._unusable)
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
                context.write_using_serializer(
                    self.cached_image, button._icon._value._idle)
                context.write_using_serializer(
                    self.cached_image, button._icon._value._selected)
                context.write_using_serializer(
                    self.cached_image, button._icon._value._highlighted)
                context.write_using_serializer(
                    self.cached_image, button._icon._value._selected_highlighted)
                context.write_using_serializer(
                    self.cached_image, button._icon._value._unusable)
            else:
                context.write_using_serializer(
                    self.string, button._icon._value._idle)
                context.write_using_serializer(
                    self.string, button._icon._value._selected)
                context.write_using_serializer(
                    self.string, button._icon._value._highlighted)
                context.write_using_serializer(
                    self.string, button._icon._value._selected_highlighted)
                context.write_using_serializer(
                    self.string, button._icon._value._unusable)
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

            context.write_using_serializer(
                self.color, button._icon._color._idle)
            context.write_using_serializer(
                self.color, button._icon._color._selected)
            context.write_using_serializer(
                self.color, button._icon._color._highlighted)
            context.write_using_serializer(
                self.color, button._icon._color._selected_highlighted)
            context.write_using_serializer(
                self.color, button._icon._color._unusable)
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
            context.write_using_serializer(
                self.color, button._mesh._color._idle)
            context.write_using_serializer(
                self.color, button._mesh._color._selected)
            context.write_using_serializer(
                self.color, button._mesh._color._highlighted)
            context.write_using_serializer(
                self.color, button._mesh._color._selected_highlighted)
            context.write_using_serializer(
                self.color, button._mesh._color._unusable)
            context.write_bool(button._outline._active)
            context.write_float(button._outline._size._idle)
            context.write_float(button._outline._size._selected)
            context.write_float(button._outline._size._highlighted)
            context.write_float(button._outline._size._selected_highlighted)
            context.write_float(button._outline._size._unusable)
            context.write_using_serializer(
                self.color, button._outline._color._idle)
            context.write_using_serializer(
                self.color, button._outline._color._selected)
            context.write_using_serializer(
                self.color, button._outline._color._highlighted)
            context.write_using_serializer(
                self.color, button._outline._color._selected_highlighted)
            context.write_using_serializer(
                self.color, button._outline._color._unusable)
            context.write_using_serializer(self.string, button._tooltip._title)
            context.write_using_serializer(
                self.string, button._tooltip._content)
            context.write_using_serializer(
                self.vector, button._tooltip._bounds)
            context.write_uint(button._tooltip._positioning_target)
            context.write_uint(button._tooltip._positioning_origin)
        if version >= 5:
            context.write_bool(button._switch._active)
            context.write_using_serializer(
                self.color, button._switch._on_color)
            context.write_using_serializer(
                self.color, button._switch._off_color)

    def deserialize(self, version, context):
        from nanome.util.enums import VertAlignOptions, HorizAlignOptions, ToolTipPositioning
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
        value._text._value._selected = context.read_using_serializer(
            self.string)
        value._text._value._highlighted = context.read_using_serializer(
            self.string)
        value._text._value._selected_highlighted = context.read_using_serializer(
            self.string)
        value._text._value._unusable = context.read_using_serializer(
            self.string)
        value._text._auto_size = context.read_bool()
        value._text._min_size = context.read_float()
        value._text._max_size = context.read_float()
        value._text._size = context.read_float()
        value._text._underlined = context.read_bool()
        if version >= 3:
            value._text._ellipsis = context.read_bool()  # default on
            value._text._bold._idle = context.read_bool()
            value._text._bold._selected = context.read_bool()
            value._text._bold._highlighted = context.read_bool()
            value._text._bold._selected_highlighted = context.read_bool()
            value._text._bold._unusable = context.read_bool()
            value._text._color._idle = context.read_using_serializer(
                self.color)
            value._text._color._selected = context.read_using_serializer(
                self.color)
            value._text._color._highlighted = context.read_using_serializer(
                self.color)
            value._text._color._selected_highlighted = context.read_using_serializer(
                self.color)
            value._text._color._unusable = context.read_using_serializer(
                self.color)
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
                value._icon._value._idle = context.read_using_serializer(
                    self.string)
                value._icon._value._selected = context.read_using_serializer(
                    self.string)
                value._icon._value._highlighted = context.read_using_serializer(
                    self.string)
                value._icon._value._selected_highlighted = context.read_using_serializer(
                    self.string)
                value._icon._value._unusable = context.read_using_serializer(
                    self.string)
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

            value._icon._color._idle = context.read_using_serializer(
                self.color)
            value._icon._color._selected = context.read_using_serializer(
                self.color)
            value._icon._color._highlighted = context.read_using_serializer(
                self.color)
            value._icon._color._selected_highlighted = context.read_using_serializer(
                self.color)
            value._icon._color._unusable = context.read_using_serializer(
                self.color)
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
            value._mesh._color._idle = context.read_using_serializer(
                self.color)
            value._mesh._color._selected = context.read_using_serializer(
                self.color)
            value._mesh._color._highlighted = context.read_using_serializer(
                self.color)
            value._mesh._color._selected_highlighted = context.read_using_serializer(
                self.color)
            value._mesh._color._unusable = context.read_using_serializer(
                self.color)
            value._outline._active = context.read_bool()
            value._outline._size._idle = context.read_float()
            value._outline._size._selected = context.read_float()
            value._outline._size._highlighted = context.read_float()
            value._outline._size._selected_highlighted = context.read_float()
            value._outline._size._unusable = context.read_float()
            value._outline._color._idle = context.read_using_serializer(
                self.color)
            value._outline._color._selected = context.read_using_serializer(
                self.color)
            value._outline._color._highlighted = context.read_using_serializer(
                self.color)
            value._outline._color._selected_highlighted = context.read_using_serializer(
                self.color)
            value._outline._color._unusable = context.read_using_serializer(
                self.color)
            value._tooltip._title = context.read_using_serializer(self.string)
            value._tooltip._content = context.read_using_serializer(
                self.string)
            value._tooltip._bounds = context.read_using_serializer(self.vector)
            value._tooltip._positioning_target = ToolTipPositioning.safe_cast(
                context.read_uint())
            value._tooltip._positioning_origin = ToolTipPositioning.safe_cast(
                context.read_uint())
        if version >= 5:
            value._switch._active = context.read_bool()
            value._switch._on_color = context.read_using_serializer(self.color)
            value._switch._off_color = context.read_using_serializer(
                self.color)
        return value


UIBaseSerializer.register_type(
    "Button", UIBaseSerializer.ContentType.ebutton, ButtonSerializer())


class DropdownItemSerializer(TypeSerializer):
    def __init__(self):
        self.string = StringField()

    def version(self):
        return 0

    def name(self):
        return "DropdownItem"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.string, value._name)
        context.write_bool(value._selected)
        context.write_bool(value._close_on_selected)
        context.write_byte(1)

    def deserialize(self, version, context):
        value = _DropdownItem._create()
        value._name = context.read_using_serializer(self.string)
        value._selected = context.read_bool()
        value._close_on_selected = context.read_bool()
        context.read_byte()  # eat the type for now, since it isn't supported quite yet
        return value


class DropdownSerializer(TypeSerializer):
    def __init__(self):
        self.string = StringField()
        self.items = ArrayField()
        self.items.set_type(DropdownItemSerializer())

    def version(self):
        return 0

    def name(self):
        return "Dropdown"

    def serialize(self, version, value, context):
        context.write_int(value._content_id)
        context.write_bool(value._use_permanent_title)
        context.write_using_serializer(self.string, value._permanent_title)
        context.write_int(value._max_displayed_items)
        context.write_using_serializer(self.items, value._items)

    def deserialize(self, version, context):
        value = _Dropdown._create()
        value._content_id = context.read_int()
        value._use_permanent_title = context.read_bool()
        value._permanent_title = context.read_using_serializer(self.string)
        value._max_displayed_items = context.read_int()
        value._items = context.read_using_serializer(self.items)
        return value


UIBaseSerializer.register_type(
    "Dropdown", UIBaseSerializer.ContentType.edropdown, DropdownSerializer())


class ImageSerializer(TypeSerializer):
    def __init__(self):
        self.data = ArrayField()
        self.data.set_type(ByteField())
        self.color = ColorField()
        self.string = StringField()
        self.cached_image = CachedImageField()

    def version(self):
        return 2

    def name(self):
        return "Image"

    def serialize(self, version, value, context):
        if (version == 0):
            safe_id = (context._plugin_id << 24) & 0x7FFFFFFF
            safe_id |= value._content_id
        else:
            safe_id = value._content_id
        context.write_int(safe_id)
        if version < 2:
            context.write_using_serializer(self.string, value._file_path)
        context.write_using_serializer(self.color, value._color)
        context.write_uint(value._scaling_option)
        if version >= 2:
            context.write_using_serializer(self.cached_image, value._file_path)
        else:
            data = []
            if (value._file_path != ""):
                with open(value._file_path, "rb") as f:
                    data = f.read()
            context.write_using_serializer(self.data, data)

    def deserialize(self, version, context):
        value = _Image._create()
        value._content_id = context.read_int()
        if (version == 0):
            id_mask = 0x00FFFFFF
            value._content_id &= id_mask
        if version < 2:
            value._file_path = context.read_using_serializer(self.string)
        value._color = context.read_using_serializer(self.color)
        value._scaling_option = context.read_uint()
        if version < 2:
            context.read_using_serializer(self.data)  # skipping data.
        else:
            context.read_using_serializer(self.cached_image)

        return value


UIBaseSerializer.register_type(
    "Image", UIBaseSerializer.ContentType.eimage, ImageSerializer())


class LabelSerializer(TypeSerializer):
    def __init__(self):
        self.string = StringField()
        self.color = ColorField()

    def version(self):
        return 1

    def name(self):
        return "Label"

    def serialize(self, version, value, context):
        if (version == 0):
            safe_id = (context._plugin_id << 24) & 0x7FFFFFFF
            safe_id |= value._content_id
        else:
            safe_id = value._content_id
        context.write_int(safe_id)
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
        from nanome.util.enums import VertAlignOptions, HorizAlignOptions
        value = _Label._create()
        value._content_id = context.read_int()
        if (version == 0):
            id_mask = 0x00FFFFFF
            value._content_id &= id_mask
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


UIBaseSerializer.register_type(
    "Label", UIBaseSerializer.ContentType.elabel, LabelSerializer())


class LayoutNodeSerializer(TypeSerializer):

    def version(self):
        return 1

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
        from nanome.util import enums
        layout_node = _LayoutNode._create()
        layout_node._id = context.read_int()
        layout_node._enabled = context.read_bool()
        layout_node._layer = context.read_int()
        layout_node._layout_orientation = enums.LayoutTypes(
            context.read_uint())
        layout_node._sizing_type = enums.SizingTypes(context.read_uint())
        layout_node._sizing_value = context.read_float()
        layout_node._forward_dist = context.read_float()
        layout_node._padding_type = enums.PaddingTypes(context.read_uint())
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


class LayoutNodeSerializerDeep(TypeSerializer):
    def __init__(self):
        self._layout_array = ArrayField()
        self._layout_array.set_type(self)
        self._content_serializer = UIBaseSerializer()
        self._inited = False

    def version(self):
        return 0

    def name(self):
        return "LayoutNodeDeep"

    def serialize(self, version, value, context):
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
        has_content = value._content != None
        context.write_bool(has_content)
        if (has_content):
            context.write_using_serializer(
                self._content_serializer, value._content)

    def deserialize(self, version, context):
        from nanome.util import enums
        result = _LayoutNode._create()
        result._id = context.read_int()
        result._enabled = context.read_bool()
        result._layer = context.read_int()
        result._layout_orientation = enums.LayoutTypes(context.read_int())
        result._sizing_type = enums.SizingTypes(context.read_int())
        result._sizing_value = context.read_float()
        result._forward_dist = context.read_float()
        result._padding_type = enums.PaddingTypes(context.read_int())
        result._padding = (context.read_float(),
                           context.read_float(),
                           context.read_float(),
                           context.read_float())
        result._children = context.read_using_serializer(self._layout_array)
        has_content = context.read_bool()
        if (has_content):
            result._content = context.read_using_serializer(
                self._content_serializer)
        return result


class LoadingBarSerializer(TypeSerializer):
    def __init__(self):
        self.string = StringField()

    def version(self):
        return 1

    def name(self):
        return "LoadingBar"

    def serialize(self, version, value, context):
        if (version == 0):
            safe_id = (context._plugin_id << 24) & 0x7FFFFFFF
            safe_id |= value._content_id
        else:
            safe_id = value._content_id
        context.write_int(safe_id)
        context.write_float(value._percentage)
        context.write_using_serializer(self.string, value._title)
        context.write_using_serializer(self.string, value._description)
        context.write_bool(value._failure)

    def deserialize(self, version, context):
        value = _LoadingBar._create()
        value._content_id = context.read_int()
        if (version == 0):
            id_mask = 0x00FFFFFF
            value._content_id &= id_mask
        value._percentage = context.read_float()
        value._title = context.read_using_serializer(self.string)
        value._description = context.read_using_serializer(self.string)
        value._failure = context.read_bool()
        return value


UIBaseSerializer.register_type(
    "LoadingBar", UIBaseSerializer.ContentType.eloadingBar, LoadingBarSerializer())


class MenuSerializer(TypeSerializer):
    def __init__(self):
        self.string = StringField()

    def version(self):
        return 0

    def name(self):
        return "Menu"

    def serialize(self, version, value, context):
        context.write_bool(value._enabled)
        context.write_int(value._index)
        context.write_using_serializer(self.string, value._title)
        context.write_bool(value._locked)
        context.write_float(value._width)
        context.write_float(value._height)
        context.write_int(value.root._id)

    def deserialize(self, version, context):
        menu = _Menu._create()
        menu._enabled = context.read_bool()
        menu._index = context.read_int()
        menu._title = context.read_using_serializer(self.string)
        menu._locked = context.read_bool()
        menu._width = context.read_float()
        menu._height = context.read_float()
        menu._root_id = context.read_int()
        return menu


class MeshSerializer(TypeSerializer):
    def __init__(self):
        self.color = ColorField()

    def version(self):
        return 1

    def name(self):
        return "Mesh"

    def serialize(self, version, value, context):
        if (version == 0):
            safe_id = (context._plugin_id << 24) & 0x7FFFFFFF
            safe_id |= value._content_id
        else:
            safe_id = value._content_id
        context.write_int(safe_id)
        context.write_using_serializer(self.color, value._mesh_color)

    def deserialize(self, version, context):
        value = _Mesh._create()
        value._content_id = context.read_int()
        if (version == 0):
            id_mask = 0x00FFFFFF
            value._content_id &= id_mask
        value._mesh_color = context.read_using_serializer(self.color)
        return value


UIBaseSerializer.register_type(
    "Mesh", UIBaseSerializer.ContentType.emesh, MeshSerializer())


class SliderSerializer(TypeSerializer):

    def version(self):
        return 1

    def name(self):
        return "Slider"

    def serialize(self, version, value, context):
        if (version == 0):
            safe_id = (context._plugin_id << 24) & 0x7FFFFFFF
            safe_id |= value._content_id
        else:
            safe_id = value._content_id
        context.write_int(safe_id)
        context.write_float(value._current_value)
        context.write_float(value._min_value)
        context.write_float(value._max_value)
        pass

    def deserialize(self, version, context):
        value = _Slider._create()
        value._content_id = context.read_int()
        if (version == 0):
            id_mask = 0x00FFFFFF
            value._content_id &= id_mask
        value._current_value = context.read_float()
        value._min_value = context.read_float()
        value._max_value = context.read_float()
        return value


UIBaseSerializer.register_type(
    "Slider", UIBaseSerializer.ContentType.eslider, SliderSerializer())


class TextInputSerializer(TypeSerializer):
    def __init__(self):
        self.string = StringField()
        self.color = ColorField()

    def version(self):
        return 3

    def name(self):
        return "TextInput"

    def serialize(self, version, value, context):
        if (version == 0):
            safe_id = (context._plugin_id << 24) & 0x7FFFFFFF
            safe_id |= value._content_id
        else:
            safe_id = value._content_id
        context.write_int(safe_id)
        context.write_int(value._max_length)
        context.write_using_serializer(self.string, value._placeholder_text)
        context.write_using_serializer(self.string, value._input_text)
        if version >= 2:
            context.write_bool(value._password)
            context.write_bool(value._number)
        if version >= 3:
            context.write_using_serializer(
                self.color, value._placeholder_text_color)
            context.write_using_serializer(self.color, value._text_color)
            context.write_using_serializer(self.color, value._background_color)
            context.write_float(value._text_size)
            context.write_uint(value._text_horizontal_align)
            context.write_bool(value._multi_line)
            context.write_float(value._padding_left)
            context.write_float(value._padding_right)
            context.write_float(value._padding_top)
            context.write_float(value._padding_bottom)

    def deserialize(self, version, context):
        value = _TextInput._create()
        value._content_id = context.read_int()
        if (version == 0):
            id_mask = 0x00FFFFFF
            value._content_id &= id_mask
        value._max_length = context.read_int()
        value._placeholder_text = context.read_using_serializer(self.string)
        value._input_text = context.read_using_serializer(self.string)
        if version >= 2:
            value._password = context.read_bool()
            value._number = context.read_bool()
        if version >= 3:
            value._placeholder_text_color = context.read_using_serializer(
                self.color)
            value._text_color = context.read_using_serializer(self.color)
            value._background_color = context.read_using_serializer(self.color)
            value._text_size = context.read_float()
            value._text_horizontal_align = context.read_uint()
            value._multi_line = context.read_bool()
            value._padding_left = context.read_float()
            value._padding_right = context.read_float()
            value._padding_top = context.read_float()
            value._padding_bottom = context.read_float()
        return value


UIBaseSerializer.register_type(
    "TextInput", UIBaseSerializer.ContentType.etextInput, TextInputSerializer())


class UIListSerializer(TypeSerializer):
    def __init__(self):
        self._array = ArrayField()
        self._array.set_type(LayoutNodeSerializerDeep())

    def version(self):
        return 1

    def name(self):
        return "List"

    def serialize(self, version, value, context):
        if (version == 0):
            safe_id = (context._plugin_id << 24) & 0x7FFFFFFF
            safe_id |= value._content_id
        else:
            safe_id = value._content_id
        context.write_int(safe_id)
        context.write_using_serializer(self._array, value._items)
        context.write_int(value._display_columns)
        context.write_int(value._display_rows)
        context.write_int(value._total_columns)
        context.write_bool(value._unusable)

    def deserialize(self, version, context):
        value = _UIList._create()
        value._content_id = context.read_int()
        if (version == 0):
            id_mask = 0x00FFFFFF
            value._content_id &= id_mask
        value._items = context.read_using_serializer(self._array)
        value._display_columns = context.read_int()
        value._display_rows = context.read_int()
        value._total_columns = context.read_int()
        value._unusable = context.read_bool()
        return value


UIBaseSerializer.register_type(
    "UIList", UIBaseSerializer.ContentType.elist, UIListSerializer())
