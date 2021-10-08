from nanome.util.enums import HorizAlignOptions, VertAlignOptions
from nanome._internal._ui import _Label
from nanome.util.color import Color


def parse_json(content_json):
    label = _Label._create()
    label._text_value = content_json.read("text", label._text_value)
    label._text_vertical_align = content_json.read("text_vertical_align", label._text_vertical_align)
    label._text_horizontal_align = content_json.read("text_horizontal_align", label._text_horizontal_align)
    label._text_auto_size = content_json.read("text_auto_size", label._text_auto_size)
    label._text_min_size = content_json.read("text_min_size", label._text_min_size)
    label._text_max_size = content_json.read("text_max_size", label._text_max_size)
    label._text_size = content_json.read("text_size", label._text_size)
    label._text_color = content_json.read("text_color", label._text_color)
    label._text_bold = content_json.read("text_bold", label._text_bold)
    label._text_italic = content_json.read("text_italics", label._text_italic)
    label._text_underlined = content_json.read("text_underlined", label._text_underlined)
    return label


def write_json(helper, label):
    helper.write("text", label._text_value)
    helper.write("text_vertical_align", label._text_vertical_align)
    helper.write("text_horizontal_align", label._text_horizontal_align)
    helper.write("text_auto_size", label._text_auto_size)
    helper.write("text_min_size", label._text_min_size)
    helper.write("text_max_size", label._text_max_size)
    helper.write("text_size", label._text_size)
    helper.write("text_color", label._text_color._color)
    helper.write("text_bold", label._text_bold)
    helper.write("text_italics", label._text_italic)
    helper.write("text_underlined", label._text_underlined)
