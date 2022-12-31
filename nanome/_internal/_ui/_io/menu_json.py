from .. import _Menu
from . import _layout_node_json


def parse_json(menu_json):
    new_menu = _Menu._create()
    assert(menu_json.read("is_menu", True))
    new_menu._title = menu_json.read("title", new_menu._title)
    new_menu._width = menu_json.read("width", new_menu._width)
    new_menu._height = menu_json.read("height", new_menu._height)
    root = menu_json.read_object("effective_root")
    new_menu._root = _layout_node_json.parse_json(root)
    return new_menu


def write_json(helper, menu):
    helper.write("is_menu", True)
    helper.write("title", menu.title)
    helper.write("width", menu.width)
    helper.write("height", menu.height)
    helper.write("version", 1)
    child = helper.make_instance()
    _layout_node_json.write_json(child, menu.root)
    helper.write("effective_root", child)
