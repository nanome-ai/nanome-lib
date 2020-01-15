from .. import _Menu
from . import _layout_node_json
from nanome.util import Logs
import json

def parse_json(menu_json):
    new_menu = _Menu._create()
    assert(menu_json.read("is_menu", True))
    new_menu._title = menu_json.read("title", "menu")
    new_menu._width = menu_json.read("width", 0.0)
    new_menu._height = menu_json.read("height", 0.0)
    root = menu_json.read_child("effective_root")
    new_menu._root = _layout_node_json.parse_json(root)
    return new_menu

def write_json(helper, menu):
    helper.write("is_menu", True)
    helper.write("title", menu.title)
    helper.write("width", menu.width)
    helper.write("height", menu.height)
    helper.write("version", 0)
    child = helper.make_child()
    _layout_node_json.write_json(child, menu.root)
    helper.write("effective_root", child)