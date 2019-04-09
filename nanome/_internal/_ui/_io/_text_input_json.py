from .. import _TextInput

def parse_json(content_json):
    text_input = _TextInput._create()
    text_input._max_length = int(float(content_json["max_length"]))
    text_input._placeholder_text = str(content_json["placeholder_text"])
    text_input._input_text = str(content_json["input_text"])
    return text_input

def write_json(text_input):
    content_json = {}
    content_json["max_length"] = text_input._max_length
    content_json["placeholder_text"] = text_input._placeholder_text
    content_json["input_text"] = text_input._input_text
    return content_json
