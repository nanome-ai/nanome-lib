from nanome.util.enums import HorizAlignOptions, VertAlignOptions
from nanome.util import Vector3, Color
from nanome._internal._ui import _Button


def read_attribute_safe(content_json, name, default):
    try:
        value = content_json[name]
    except:
        value = default
    return value


def parse_json(content_json):
    # type: () -> Button
    # region text
    button = _Button._create()
    button._name = content_json.read("name", button._name)
    button._selected = content_json.read("selected", button._selected)
    button._unusable = content_json.read("unusable", button._unusable)
    button._disable_on_press = content_json.read("disable_on_press", button._disable_on_press)
    button._text._active = content_json.read("text_active", button._text._active)
    button._text._value._idle = content_json.read("text_value_idle", button._text._value._idle)
    button._text._value._selected = content_json.read("text_value_selected", button._text._value._selected)
    button._text._value._highlighted = content_json.read("text_value_highlighted", button._text._value._highlighted)
    button._text._value._selected_highlighted = content_json.read("text_value_selected_highlighted", button._text._value._selected_highlighted)
    button._text._value._unusable = content_json.read("text_value_unusable", button._text._value._unusable)
    button._text._auto_size = content_json.read("text_auto_size", button._text._auto_size)
    button._text._min_size = content_json.read("text_min_size", button._text._min_size)
    button._text._max_size = content_json.read("text_max_size", button._text._max_size)
    button._text._size = content_json.read("text_size", button._text._size)
    button._text._underlined = content_json.read("text_underlined", button._text._underlined)
    button._text._bold._set_all(content_json.read("text_bolded", False))  # deprecated
    button._text._bold._idle = content_json.read("text_bold_idle", button._text._bold._idle)
    button._text._bold._selected = content_json.read("text_bold_selected", button._text._bold._selected)
    button._text._bold._highlighted = content_json.read("text_bold_highlighted", button._text._bold._highlighted)
    button._text._bold._selected_highlighted = content_json.read("text_bold_selected_highlighted", button._text._bold._selected_highlighted)
    button._text._bold._unusable = content_json.read("text_bold_unusable", button._text._bold._unusable)
    button._text._color._idle = content_json.read("text_color_idle", button._text._color._idle)
    button._text._color._selected = content_json.read("text_color_selected", button._text._color._selected)
    button._text._color._highlighted = content_json.read("text_color_highlighted", button._text._color._highlighted)
    button._text._color._selected_highlighted = content_json.read("text_color_selected_highlighted", button._text._color._selected_highlighted)
    button._text._color._unusable = content_json.read("text_color_unusable", button._text._color._unusable)
    button._text._padding_top = content_json.read("text_padding_top", button._text._padding_top)
    button._text._padding_bottom = content_json.read("text_padding_bottom", button._text._padding_bottom)
    button._text._padding_left = content_json.read("text_padding_left", button._text._padding_left)
    button._text._padding_right = content_json.read("text_padding_right", button._text._padding_right)
    button._text._line_spacing = content_json.read("text_line_spacing", button._text._line_spacing)
    button._text._vertical_align = VertAlignOptions(content_json.read("text_vertical_align", button._text._vertical_align))
    button._text._horizontal_align = HorizAlignOptions(content_json.read("text_horizontal_align", button._text._horizontal_align))
    # endregion
    # region icon
    button._icon._active = content_json.read("icon_active", button._icon._active)
    button._icon._value._idle = content_json.read("icon_value_idle", button._icon._value._idle)
    button._icon._value._selected = content_json.read("icon_value_selected", button._icon._value._selected)
    button._icon._value._highlighted = content_json.read("icon_value_highlighted", button._icon._value._highlighted)
    button._icon._value._selected_highlighted = content_json.read("icon_value_selected_highlighted", button._icon._value._selected_highlighted)
    button._icon._value._unusable = content_json.read("icon_value_unusable", button._icon._value._unusable)
    button._icon._color._idle = content_json.read("icon_color_idle", button._icon._color._idle)
    button._icon._color._selected = content_json.read("icon_color_selected", button._icon._color._selected)
    button._icon._color._highlighted = content_json.read("icon_color_highlighted", button._icon._color._highlighted)
    button._icon._color._selected_highlighted = content_json.read("icon_color_selected_highlighted", button._icon._color._selected_highlighted)
    button._icon._color._unusable = content_json.read("icon_color_unusable", button._icon._color._unusable)
    button._icon._sharpness = content_json.read("icon_sharpness", button._icon._sharpness)
    button._icon._size = content_json.read("icon_size", button._icon._size)
    button._icon._ratio = content_json.read("icon_ratio", button._icon._ratio)
    button._icon._position = content_json.read("icon_position", button._icon._position)
    button._icon._rotation = content_json.read("icon_rotation", button._icon._rotation)
    # endregion
    # region mesh
    button._mesh._active = content_json.read("mesh_active", button._mesh._active)
    button._mesh._enabled._idle = content_json.read("mesh_enabled_idle", button._mesh._enabled._idle)
    button._mesh._enabled._selected = content_json.read("mesh_enabled_selected", button._mesh._enabled._selected)
    button._mesh._enabled._highlighted = content_json.read("mesh_enabled_highlighted", button._mesh._enabled._highlighted)
    button._mesh._enabled._selected_highlighted = content_json.read("mesh_enabled_selected_highlighted", button._mesh._enabled._selected_highlighted)
    button._mesh._enabled._unusable = content_json.read("mesh_enabled_unusable", button._mesh._enabled._unusable)
    button._mesh._color._idle = content_json.read("mesh_color_idle", button._mesh._color._idle)
    button._mesh._color._selected = content_json.read("mesh_color_selected", button._mesh._color._selected)
    button._mesh._color._highlighted = content_json.read("mesh_color_highlighted", button._mesh._color._highlighted)
    button._mesh._color._selected_highlighted = content_json.read("mesh_color_selected_highlighted", button._mesh._color._selected_highlighted)
    button._mesh._color._unusable = content_json.read("mesh_color_unusable", button._mesh._color._unusable)
    # endregion
    # region outline
    button._outline._active = content_json.read("outline_active", button._outline._active)
    button._outline._size._idle = content_json.read("outline_size_idle", button._outline._size._idle)
    button._outline._size._selected = content_json.read("outline_size_selected", button._outline._size._selected)
    button._outline._size._highlighted = content_json.read("outline_size_highlighted", button._outline._size._highlighted)
    button._outline._size._selected_highlighted = content_json.read("outline_size_selected_highlighted", button._outline._size._selected_highlighted)
    button._outline._size._unusable = content_json.read("outline_size_unusable", button._outline._size._unusable)
    button._outline._color._idle = content_json.read("outline_color_idle", button._outline._color._idle)
    button._outline._color._selected = content_json.read("outline_color_selected", button._outline._color._selected)
    button._outline._color._highlighted = content_json.read("outline_color_highlighted", button._outline._color._highlighted)
    button._outline._color._selected_highlighted = content_json.read("outline_color_selected_highlighted", button._outline._color._selected_highlighted)
    button._outline._color._unusable = content_json.read("outline_color_unusable", button._outline._color._unusable)
    # endregion
    # region tooltip
    button._tooltip._title = content_json.read("tooltip_title", button._tooltip._title)
    button._tooltip._content = content_json.read("tooltip_content", button._tooltip._content)
    button._tooltip._bounds = content_json.read("tooltip_bounds", button._tooltip._bounds)
    button._tooltip._positioning_target = content_json.read("tooltip_positioning_target", button._tooltip._positioning_target)
    button._tooltip._positioning_origin = content_json.read("tooltip_positioning_origin", button._tooltip._positioning_origin)
    # endregion
    return button


def write_json(helper, button):
    # type: (_Button) -> dict
    helper.write("name", button._name)
    helper.write("selected", button._selected)
    helper.write("unusable", button._unusable)
    helper.write("disable_on_press", button._disable_on_press)

    # region text
    helper.write("text_active", button._text._active)
    helper.write("text_value_idle", button._text._value._idle)
    helper.write("text_value_selected", button._text._value._selected)
    helper.write("text_value_highlighted", button._text._value._highlighted)
    helper.write("text_value_selected_highlighted", button._text._value._selected_highlighted)
    helper.write("text_value_unusable", button._text._value._unusable)
    helper.write("text_auto_size", button._text._auto_size)
    helper.write("text_min_size", button._text._min_size)
    helper.write("text_max_size", button._text._max_size)
    helper.write("text_size", button._text._size)
    helper.write("text_underlined", button._text._underlined)
    helper.write("text_bold_idle", button._text._bold._idle)
    helper.write("text_bold_selected", button._text._bold._selected)
    helper.write("text_bold_highlighted", button._text._bold._highlighted)
    helper.write("text_bold_selected_highlighted", button._text._bold._selected_highlighted)
    helper.write("text_bold_unusable", button._text._bold._unusable)
    helper.write("text_color_idle", button._text._color._idle)
    helper.write("text_color_selected", button._text._color._selected)
    helper.write("text_color_highlighted", button._text._color._highlighted)
    helper.write("text_color_selected_highlighted", button._text._color._selected_highlighted)
    helper.write("text_color_unusable", button._text._color._unusable)
    helper.write("text_padding_top", button._text._padding_top)
    helper.write("text_padding_bottom", button._text._padding_bottom)
    helper.write("text_padding_left", button._text._padding_left)
    helper.write("text_padding_right", button._text._padding_right)
    helper.write("text_line_spacing", button._text._line_spacing)
    helper.write("text_vertical_align", int(button._text._vertical_align))
    helper.write("text_horizontal_align", int(button._text._horizontal_align))
    # endregion
    # region icon
    helper.write("icon_active", button._icon._active)
    helper.write("icon_value_idle", button._icon._value._idle)
    helper.write("icon_value_selected", button._icon._value._selected)
    helper.write("icon_value_highlighted", button._icon._value._highlighted)
    helper.write("icon_value_selected_highlighted", button._icon._value._selected_highlighted)
    helper.write("icon_value_unusable", button._icon._value._unusable)
    helper.write("icon_color_idle", button._icon._color._idle._color)
    helper.write("icon_color_selected", button._icon._color._selected._color)
    helper.write("icon_color_highlighted", button._icon._color._highlighted._color)
    helper.write("icon_color_selected_highlighted", button._icon._color._selected_highlighted._color)
    helper.write("icon_color_unusable", button._icon._color._unusable._color)
    helper.write("icon_sharpness", button._icon._sharpness)
    helper.write("icon_size", button._icon._size)
    helper.write("icon_ratio", button._icon._ratio)
    helper.write("icon_position", button._icon._position)
    helper.write("icon_rotation", button._icon._rotation)
    # endregion
    # region mesh
    helper.write("mesh_active", button._mesh._active)
    helper.write("mesh_enabled_idle", button._mesh._enabled._idle)
    helper.write("mesh_enabled_selected", button._mesh._enabled._selected)
    helper.write("mesh_enabled_highlighted", button._mesh._enabled._highlighted)
    helper.write("mesh_enabled_selected_highlighted", button._mesh._enabled._selected_highlighted)
    helper.write("mesh_enabled_unusable", button._mesh._enabled._unusable)
    helper.write("mesh_color_idle", button._mesh._color._idle)
    helper.write("mesh_color_selected", button._mesh._color._selected)
    helper.write("mesh_color_highlighted", button._mesh._color._highlighted)
    helper.write("mesh_color_selected_highlighted", button._mesh._color._selected_highlighted)
    helper.write("mesh_color_unusable", button._mesh._color._unusable)
    # endregion
    # region outline
    helper.write("outline_active", button._outline._active)
    helper.write("outline_size_idle", button._outline._size._idle)
    helper.write("outline_size_selected", button._outline._size._selected)
    helper.write("outline_size_highlighted", button._outline._size._highlighted)
    helper.write("outline_size_selected_highlighted", button._outline._size._selected_highlighted)
    helper.write("outline_size_unusable", button._outline._size._unusable)
    helper.write("outline_color_idle", button._outline._color._idle)
    helper.write("outline_color_selected", button._outline._color._selected)
    helper.write("outline_color_highlighted", button._outline._color._highlighted)
    helper.write("outline_color_selected_highlighted", button._outline._color._selected_highlighted)
    helper.write("outline_color_unusable", button._outline._color._unusable)
    # endregion
    # region tooltip
    helper.write("tooltip_title", button._tooltip._title)
    helper.write("tooltip_content", button._tooltip._content)
    helper.write("tooltip_bounds", button._tooltip._bounds)
    helper.write("tooltip_positioning_target", button._tooltip._positioning_target)
    helper.write("tooltip_positioning_origin", button._tooltip._positioning_origin)
    # endregion
