from .. import _LayoutNode
from . import _ui_base_json
import json

def parse_json(node_json):
    node = _LayoutNode._create()
    node.name = str(node_json["name"])
    node._enabled = bool(node_json["enabled"])
    node._layer = int(float(node_json["layer"]))
    node._layout_orientation = _LayoutNode.LayoutTypes(int(float(node_json["layout_orientation"])))
    node._sizing_type = _LayoutNode.SizingTypes(int(float(node_json["sizing_type"])))
    node._sizing_value = float(node_json["sizing_value"])
    node._forward_dist = float(node_json["forward_dist"])
    node._padding_type = _LayoutNode.PaddingTypes(int(float(node_json["padding_type"])))
    node._padding = (float(node_json["padding_x"]),
                    float(node_json["padding_y"]),
                    float(node_json["padding_z"]),
                    float(node_json["padding_w"]))
    child_list = node_json["children"]
    for child_obj in child_list:
        node._add_child(parse_json(child_obj))

    content_json = node_json["content"]
    if (content_json != None):
        content_obj = _ui_base_json.parse_json(content_json)
        node._set_content(content_obj)
    return node

def write_json(node):
    node_json = {}
    node_json["name"] = node._name
    node_json["enabled"] = node._enabled
    node_json["layer"] = node._layer
    node_json["layout_orientation"] = node._layout_orientation
    node_json["sizing_type"] = node._sizing_type
    node_json["sizing_value"] = node._sizing_value
    node_json["forward_dist"] = node._forward_dist
    node_json["padding_type"] = int(node._padding_type)
    node_json["padding_type"] = int(node._padding_type)
    node_json["padding_x"] = node._padding[0]
    node_json["padding_y"] = node._padding[1]
    node_json["padding_z"] = node._padding[2]
    node_json["padding_w"] = node._padding[3]
    #convert all children
    node_json["children"] = []
    for child in node.get_children():
        node_json["children"].append(write_json(child))
    #convert all contents
    node_json["content"] = _ui_base_json.write_json(node._get_content())
    return node_json