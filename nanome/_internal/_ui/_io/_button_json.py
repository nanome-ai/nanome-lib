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
    button._selected = bool(content_json["selected"])
    button._unusable = bool(content_json["unusable"])
    button._text._active = bool(content_json["text_active"])
    button._text._value_idle = str(content_json["text_value_idle"])
    button._text._value_selected = str(content_json["text_value_selected"])
    button._text._value_highlighted = str(content_json["text_value_highlighted"])
    button._text._value_selected_highlighted = str(content_json["text_value_selected_highlighted"])
    button._text._value_unusable = str(content_json["text_value_unusable"])
    button._text._auto_size = bool(content_json["text_auto_size"])
    button._text._min_size = float(content_json["text_min_size"])
    button._text._max_size = float(content_json["text_max_size"])
    button._text._size = float(content_json["text_size"])
    button._text._underlined = bool(content_json["text_underlined"])
    button._text._bolded = bool(content_json["text_bolded"])
    button._text._vertical_align = VertAlignOptions(int(float(content_json["text_vertical_align"])))
    button._text._horizontal_align = HorizAlignOptions(int(float(content_json["text_horizontal_align"])))
    button._icon._active = bool(content_json["icon_active"])
    button._icon._value_idle = str(content_json["icon_value_idle"])
    button._icon._value_selected = str(content_json["icon_value_selected"])
    button._icon._value_highlighted = str(content_json["icon_value_highlighted"])
    button._icon._value_selected_highlighted = str(content_json["icon_value_selected_highlighted"])
    button._icon._value_unusable = str(content_json["icon_value_unusable"])
    button._icon._color_idle = Color.from_int(int(float(content_json["icon_color_idle"])))
    button._icon._color_selected = Color.from_int(int(float(content_json["icon_color_selected"])))
    button._icon._color_highlighted = Color.from_int(int(float(content_json["icon_color_highlighted"])))
    button._icon._color_selected_highlighted = Color.from_int(int(float(content_json["icon_color_selected_highlighted"])))
    button._icon._color_unusable = Color.from_int(int(float(content_json["icon_color_unusable"])))
    button._icon._sharpness = float(content_json["icon_sharpness"])
    button._icon._size = float(content_json["icon_size"])
    button._icon._ratio = float(content_json["icon_ratio"])
    button._icon._position = Vector3(float(content_json["icon_position_x"]), float(content_json["icon_position_y"]), float(content_json["icon_position_z"]))
    button._icon._rotation = Vector3(float(content_json["icon_rotation_x"]), float(content_json["icon_rotation_y"]), float(content_json["icon_rotation_z"]))
    return button

def write_json(button):
    # type: (_Button) -> dict
    content_json = {}
    content_json["selected"] = button._selected
    content_json["unusable"] = button._unusable
    content_json["text_active"] = button._text._active
    content_json["text_value_idle"] = button._text._value_idle
    content_json["text_value_selected"] = button._text._value_selected
    content_json["text_value_highlighted"] = button._text._value_highlighted
    content_json["text_value_selected_highlighted"] = button._text._value_selected_highlighted
    content_json["text_value_unusable"] = button._text._value_unusable
    content_json["text_auto_size"] = button._text._auto_size
    content_json["text_min_size"] = button._text._min_size
    content_json["text_max_size"] = button._text._max_size
    content_json["text_size"] = button._text._size
    content_json["text_underlined"] = button._text._underlined
    content_json["text_bolded"] = button._text._bolded
    content_json["text_vertical_align"] = int(button._text._vertical_align)
    content_json["text_horizontal_align"] = int(button._text._horizontal_align)
    content_json["icon_active"] = button._icon._active
    content_json["icon_value_idle"] = button._icon._value_idle
    content_json["icon_value_selected"] = button._icon._value_selected
    content_json["icon_value_highlighted"] = button._icon._value_highlighted
    content_json["icon_value_selected_highlighted"] = button._icon._value_selected_highlighted
    content_json["icon_value_unusable"] = button._icon._value_unusable
    content_json["icon_color_idle"] = button._icon._color_idle
    content_json["icon_color_selected"] = button._icon._color_selected
    content_json["icon_color_highlighted"] = button._icon._color_highlighted
    content_json["icon_color_selected_highlighted"] = button._icon._color_selected_highlighted
    content_json["icon_color_unusable"] = button._icon._color_unusable
    content_json["icon_sharpness"] = button._icon._sharpness
    content_json["icon_size"] = button._icon._size
    content_json["icon_ratio"] = button._icon._ratio
    content_json["icon_position_x"] = button._icon._position.x
    content_json["icon_position_y"] = button._icon._position.y
    content_json["icon_position_z"] = button._icon._position.z
    content_json["icon_rotation_x"] = button._icon._rotation.x
    content_json["icon_rotation_y"] = button._icon._rotation.y
    content_json["icon_rotation_z"] = button._icon._rotation.z
    return content_json
