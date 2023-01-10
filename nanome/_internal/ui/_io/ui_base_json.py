from .. import _Button, _Mesh, _Slider, _Label, _TextInput, _UIBase, _UIList, _Image, _LoadingBar, _Dropdown
from . import button_json, mesh_json, slider_json, text_input_json, label_json, ui_list_json, image_json, loading_bar_json, dropdown_json
# this line shouldnt't be needed ^^^
import logging

logger = logging.getLogger(__name__)


def parse_json(content_json):
    type_name = content_json.read("type_name", "Unknown")
    if type_name == "Button":
        return button_json.parse_json(content_json)
    elif type_name == "Mesh":
        return mesh_json.parse_json(content_json)
    elif type_name == "Slider":
        return slider_json.parse_json(content_json)
    elif type_name == "TextInput" or type_name == "Text Input":
        return text_input_json.parse_json(content_json)
    elif type_name == "Label":
        return label_json.parse_json(content_json)
    elif type_name == "List":
        return ui_list_json.parse_json(content_json)
    elif type_name == "Image":
        return image_json.parse_json(content_json)
    elif type_name == "LoadingBar":
        return loading_bar_json.parse_json(content_json)
    elif type_name == "Dropdown":
        return dropdown_json.parse_json(content_json)
    else:
        logger.error("unknown content type: " + type_name)
        return _UIBase()


def write_json(helper, content):
    if(content is None):
        return None
    elif(isinstance(content, _Button)):
        type_name = "Button"
        button_json.write_json(helper, content)
    elif(isinstance(content, _Mesh)):
        type_name = "Mesh"
        mesh_json.write_json(helper, content)
    elif(isinstance(content, _Slider)):
        type_name = "Slider"
        slider_json.write_json(helper, content)
    elif(isinstance(content, _TextInput)):
        type_name = "TextInput"
        text_input_json.write_json(helper, content)
    elif(isinstance(content, _Label)):
        type_name = "Label"
        label_json.write_json(helper, content)
    elif(isinstance(content, _UIList)):
        type_name = "List"
        ui_list_json.write_json(helper, content)
    elif(isinstance(content, _Image)):
        type_name = "Image"
        image_json.write_json(helper, content)
    elif(isinstance(content, _LoadingBar)):
        type_name = "LoadingBar"
        loading_bar_json.write_json(helper, content)
    elif(isinstance(content, _Dropdown)):
        type_name = "Dropdown"
        dropdown_json.write_json(helper, content)
    else:
        logger.error("unknown content type: " + str(type(content)))
        return None
    helper.write("type_name", type_name)
