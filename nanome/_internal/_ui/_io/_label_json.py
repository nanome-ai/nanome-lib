from nanome.util.text_settings import HorizAlignOptions, VertAlignOptions
from nanome._internal._ui import _Label
from nanome.util.color import Color

def parse_json(content_json):
    label = _Label._create()
    label._text_value = str(content_json["text"])
    label._text_vertical_align = VertAlignOptions(int(float(content_json["text_vertical_align"])))
    label._text_horizontal_align = HorizAlignOptions(int(float(content_json["text_horizontal_align"])))
    label._text_auto_size = bool(content_json["text_auto_size"])
    label._text_min_size = float(content_json["text_min_size"])
    label._text_max_size = float(content_json["text_max_size"])
    label._text_size = float(content_json["text_size"])
    label._text_color = Color.from_int(int(float(content_json["text_color"])))
    label._text_bold = bool(content_json["text_bold"])
    label._text_italic = bool(content_json["text_italics"])
    label._text_underlined = bool(content_json["text_underlined"])
    return label

def write_json(label):
    content_json = {}
    content_json["text"] = label._text_value
    content_json["text_vertical_align"] = int(label._text_vertical_align)
    content_json["text_horizontal_align"] = int(label._text_horizontal_align)
    content_json["text_auto_size"] = label._text_auto_size
    content_json["text_min_size"] = label._text_min_size
    content_json["text_max_size"] = label._text_max_size
    content_json["text_size"] = label._text_size
    content_json["text_color"] = label._text_color._color
    content_json["text_bold"] = label._text_bold
    content_json["text_italics"] = label._text_italic
    content_json["text_underlined"] = label._text_underlined
    return content_json