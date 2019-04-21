from nanome.util import Logs
from .. import _Button, _Mesh, _Slider, _Label, _TextInput, _UIBase, _UIList, _Image, _LoadingBar
from . import _button_json, _mesh_json, _slider_json, _text_input_json, _label_json, _ui_list_json, _image_json, _loading_bar_json
#this line shouldnt't be needed ^^^

def parse_json(content_json):
    type_name = content_json["type_name"]
    if type_name == "Button":
        return _button_json.parse_json(content_json)
    elif type_name == "Mesh":
        return _mesh_json.parse_json(content_json)
    elif type_name == "Slider":
        return _slider_json.parse_json(content_json)
    elif type_name == "Text Input":
        return _text_input_json.parse_json(content_json)
    elif type_name == "Label":
        return _label_json.parse_json(content_json)
    elif type_name == "List":
        return _ui_list_json.parse_json(content_json)
    elif type_name == "Image":
        return _image_json.parse_json(content_json)
    elif type_name == "LoadingBar":
        return _loading_bar_json.parse_json(content_json)
    else:
        Logs.error("unknown content type: " + type_name)
        return _UIBase()

def write_json(content):
    if(content is None):
        return None
    elif(isinstance(content, _Button)):
        type_name = "Button"
        content_json = _button_json.write_json(content)
    elif(isinstance(content, _Mesh)):
        type_name = "Mesh"
        content_json = _mesh_json.write_json(content)
    elif(isinstance(content, _Slider)):
        type_name = "Slider"
        content_json = _slider_json.write_json(content)
    elif(isinstance(content, _TextInput)):
        type_name = "Text Input"
        content_json = _text_input_json.write_json(content)
    elif(isinstance(content, _Label)):
        type_name = "Label"
        content_json = _label_json.write_json(content)
    elif(isinstance(content, _UIList)):
        type_name = "List"
        content_json = _ui_list_json.write_json(content)
    elif(isinstance(content, _Image)):
        type_name = "Image"
        content_json = _image_json.write_json(content)
    elif(isinstance(content, _LoadingBar)):
        type_name = "LoadingBar"
        content_json = _loading_bar_json.write_json(content)
    else:
        Logs.error("unknown content type: " + str(type(content)))
        content_json = {}
        return None
    content_json["type_name"] = type_name
    return content_json