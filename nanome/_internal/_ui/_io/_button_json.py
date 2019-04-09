from nanome.util.text_settings import HorizAlignOptions, VertAlignOptions
from nanome._internal._ui import _Button

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
    content_json["text_vertical_align"] = button._text._vertical_align
    content_json["text_horizontal_align"] = button._text._horizontal_align
    return content_json
    