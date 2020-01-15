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
    button = _Button._create()
    button._selected = content_json.read("selected", False)
    button._unusable = content_json.read("unusable", False)
    button._text._active = content_json.read("text_active", False)
    button._text._value._idle = content_json.read("text_value_idle", "idle")
    button._text._value._selected = content_json.read("text_value_selected", "selected")
    button._text._value._highlighted = content_json.read("text_value_highlighted", "highlighted")
    button._text._value._selected_highlighted = content_json.read("text_value_selected_highlighted", "both")
    button._text._value._unusable = content_json.read("text_value_unusable", "unusable")
    button._text._auto_size = content_json.read("text_auto_size", True)
    button._text._min_size = content_json.read("text_min_size", 0.0)
    button._text._max_size = content_json.read("text_max_size", 0.0)
    button._text._size = content_json.read("text_size", 0.0)
    button._text._underlined = content_json.read("text_underlined", False)
    button._text._bold._set_all(content_json.read("text_bolded", False)) #deprecated
    button._text._vertical_align = VertAlignOptions(content_json.read("text_vertical_align", 0))
    button._text._horizontal_align = HorizAlignOptions(content_json.read("text_horizontal_align", 0))
    button._icon._active = content_json.read( "icon_active", False)
    button._icon._value._idle = content_json.read( "icon_value_idle", '')
    button._icon._value._selected = content_json.read( "icon_value_selected", '')
    button._icon._value._highlighted = content_json.read( "icon_value_highlighted", '')
    button._icon._value._selected_highlighted = content_json.read( "icon_value_selected_highlighted", '')
    button._icon._value._unusable = content_json.read( "icon_value_unusable", '')
    button._icon._color._idle = content_json.read( "icon_color_idle", Color.from_int(4294967295))
    button._icon._color._selected = content_json.read( "icon_color_selected", Color.from_int(4294967295))
    button._icon._color._highlighted = content_json.read( "icon_color_highlighted", Color.from_int(4294967295))
    button._icon._color._selected_highlighted = content_json.read( "icon_color_selected_highlighted", Color.from_int(4294967295))
    button._icon._color._unusable = content_json.read( "icon_color_unusable", Color.from_int(4294967295))
    button._icon._sharpness = content_json.read( "icon_sharpness", 0.5)
    button._icon._size = content_json.read( "icon_size", 1.0)
    button._icon._ratio = content_json.read( "icon_ratio", 0.5)
    button._icon._position = Vector3(content_json.read( "icon_position_x", 0.0),
        content_json.read( "icon_position_y", 0.0),
        content_json.read( "icon_position_z", 0.0))
    button._icon._rotation = Vector3(content_json.read( "icon_rotation_x", 0.0),
        content_json.read( "icon_rotation_y", 0.0),
        content_json.read( "icon_rotation_z", 0.0))
    return button

def write_json(helper, button):
    # type: (_Button) -> dict
    helper.write("selected", button._selected)
    helper.write("unusable", button._unusable)
    #region text
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
    helper.write("text_bold_idle", button.text._bold._idle)
    helper.write("text_bold_selected", button.text._bold._selected)
    helper.write("text_bold_highlighted", button.text._bold._highlighted)
    helper.write("text_bold_selected_highlighted", button.text._bold._selected_highlighted)
    helper.write("text_bold_unusable", button.text._bold._unusable)
    helper.write("text_color_idle", button.text._color._idle)
    helper.write("text_color_selected", button.text._color._selected)
    helper.write("text_color_highlighted", button.text._color._highlighted)
    helper.write("text_color_selected_highlighted", button.text._color._selected_highlighted)
    helper.write("text_color_unusable", button.text._color._unusable)
    helper.write("text_padding_top", button.text._padding_top)
    helper.write("text_padding_bottom", button.text._padding_bottom)
    helper.write("text_padding_left", button.text._padding_left)
    helper.write("text_padding_right", button.text._padding_right)
    helper.write("text_line_spacing", button.text._line_spacing)
    helper.write("text_vertical_align", int(button._text._vertical_align))
    helper.write("text_horizontal_align", int(button._text._horizontal_align))
    #endregion
    #region icon
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
    #endregion
    #region mesh
    helper.write("mesh_active", button.mesh._active)
    helper.write("mesh_enabled_idle", button.mesh._enabled._idle)
    helper.write("mesh_enabled_selected", button.mesh._enabled._selected)
    helper.write("mesh_enabled_highlighted", button.mesh._enabled._highlighted)
    helper.write("mesh_enabled_selected_highlighted", button.mesh._enabled._selected_highlighted)
    helper.write("mesh_enabled_unusable", button.mesh._enabled._unusable)
    helper.write("mesh_color_idle", button.mesh._color._idle)
    helper.write("mesh_color_selected", button.mesh._color._selected)
    helper.write("mesh_color_highlighted", button.mesh._color._highlighted)
    helper.write("mesh_color_selected_highlighted", button.mesh._color._selected_highlighted)
    helper.write("mesh_color_unusable", button.mesh._color._unusable)
    #endregion
    #region outline

    #endregion