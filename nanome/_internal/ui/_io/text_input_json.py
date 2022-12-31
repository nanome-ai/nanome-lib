from .. import _TextInput


def parse_json(content_json):
    text_input = _TextInput._create()
    text_input._max_length = content_json.read("max_length", text_input._max_length)
    text_input._placeholder_text = content_json.read("placeholder_text", text_input._placeholder_text)
    text_input._input_text = content_json.read("input_text", text_input._input_text)
    text_input._password = content_json.read("password", text_input._password)
    text_input._number = content_json.read("number", text_input._number)
    text_input._placeholder_text_color = content_json.read("placeholder_text_color", text_input._placeholder_text_color)
    text_input._text_color = content_json.read("text_color", text_input._text_color)
    text_input._background_color = content_json.read("background_color", text_input._background_color)
    # default value -1 for backwards compatability. -1 will trigger autosize
    text_input._text_size = content_json.read("text_size", -1.0)
    text_input._text_horizontal_align = content_json.read("text_horizontal_align", text_input._text_horizontal_align)
    text_input._multi_line = content_json.read("multi_line", text_input._multi_line)
    text_input._padding_left = content_json.read("padding_left", text_input._padding_left)
    text_input._padding_right = content_json.read("padding_right", text_input._padding_right)
    text_input._padding_top = content_json.read("padding_top", text_input._padding_top)
    text_input._padding_bottom = content_json.read("padding_bottom", text_input._padding_bottom)
    return text_input


def write_json(helper, text_input):
    helper.write("max_length", text_input._max_length)
    helper.write("placeholder_text", text_input._placeholder_text)
    helper.write("input_text", text_input._input_text)
    helper.write("password", text_input._password)
    helper.write("number", text_input._number)
    helper.write("placeholder_text_color", text_input._placeholder_text_color)
    helper.write("text_color", text_input._text_color)
    helper.write("background_color", text_input._background_color)
    helper.write("text_size", text_input._text_size)
    helper.write("text_horizontal_align", text_input._text_horizontal_align)
    helper.write("multi_line", text_input._multi_line)
    helper.write("padding_left", text_input._padding_left)
    helper.write("padding_right", text_input._padding_right)
    helper.write("padding_top", text_input._padding_top)
    helper.write("padding_bottom", text_input._padding_bottom)
