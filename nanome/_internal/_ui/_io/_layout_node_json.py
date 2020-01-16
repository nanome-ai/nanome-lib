from .. import _LayoutNode
from . import _ui_base_json
from nanome.util import Logs
import json

def parse_json(node_json):
    node = _LayoutNode._create()
    node._name = node_json.read("name", node._name)
    node._enabled = node_json.read("enabled", node._enabled)
    node._layer = node_json.read("layer", node._layer)
    node._layout_orientation = node_json.read("layout_orientation", node._layout_orientation)
    node._sizing_type = node_json.read("sizing_type", node._sizing_type)
    node._sizing_value = node_json.read("sizing_value", node._sizing_value)
    node._forward_dist = node_json.read("forward_dist", node._forward_dist)
    node._padding_type = node_json.read("padding_type", node._padding_type)
    node._padding = (node_json.read("padding_x", node._padding[0]),
                     node_json.read("padding_y", node._padding[1]),
                     node_json.read("padding_z", node._padding[2]),
                     node_json.read("padding_w", node._padding[3]))
    content_json = node_json.read_object("content")
    if content_json is not None:
        content_obj = _ui_base_json.parse_json(content_json)
        node._set_content(content_obj)
    child_list = node_json.read_objects("children")
    for child_obj in child_list:
        node._add_child(parse_json(child_obj))
    return node

def write_json(helper, node):
    helper.write("name", node._name)
    helper.write("enabled", node._enabled)
    helper.write("layer", node._layer)
    helper.write("layout_orientation", node._layout_orientation)
    helper.write("sizing_type", node._sizing_type)
    helper.write("sizing_value", node._sizing_value)
    helper.write("forward_dist", node._forward_dist)
    helper.write("padding_type", node._padding_type)
    helper.write("padding_type", node._padding_type)
    helper.write("padding_x", node._padding[0])
    helper.write("padding_y", node._padding[1])
    helper.write("padding_z", node._padding[2])
    helper.write("padding_w", node._padding[3])
    #convert all children
    children = []
    for child in node._get_children():
        c_helper = helper.make_instance()
        write_json(c_helper, child)
        children.append(c_helper.get_dict())
    helper.write("children", children)
    #convert all contents
    content = helper.make_instance()
    _ui_base_json.write_json(content, node._get_content())
    helper.write("content", content)