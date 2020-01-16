from .. import _TextInput

def parse_json(content_json):
    text_input = _TextInput._create()
    text_input._max_length = content_json.read("max_length", text_input._max_length)
    text_input._placeholder_text = content_json.read("placeholder_text", text_input._placeholder_text)
    text_input._input_text = content_json.read("input_text", text_input._input_text)
    return text_input

def write_json(helper, text_input):
    helper.write("max_length", text_input._max_length)
    helper.write("placeholder_text", text_input._placeholder_text)
    helper.write("input_text", text_input._input_text)
