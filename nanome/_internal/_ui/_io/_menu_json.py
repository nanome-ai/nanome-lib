from .. import _Menu
from . import _layout_node_json
import json

def parse_json(menu_json):
    new_menu = _Menu._create()

    assert(menu_json["is_menu"] == True)
    new_menu.title = menu_json["title"]
    new_menu.width = menu_json["width"]
    new_menu.height = menu_json["height"]
    new_menu.root = _layout_node_json.parse_json(dict(menu_json["effective_root"]))
    return new_menu

def write_json(menu):
    menu_dict = {}
    menu_dict["is_menu"] = True
    menu_dict["title"] = menu.title
    menu_dict["width"] = menu.width
    menu_dict["height"] = menu.height
    menu_dict["effective_root"] = _layout_node_json.write_json(menu.root)
    return menu_dict