import os
import json
from nanome.api.ui import Menu
from testing.utilities import *

test_assets = os.getcwd() + ("\\testing\\test_assets")
test_output_dir = os.getcwd() + ("\\testing\\test_outputs")

def run(counter):
    run_test(test_menu_json, counter)

def test_menu_json():
    test_path = test_assets + "\\test_menu.json"
    output_path = test_output_dir + "\\test_menu.json"
    menu = Menu.io.from_json(test_path)
    menu.io.to_json(output_path)
    menu2 = Menu.io.from_json(output_path)
    for node in menu.get_all_nodes():
        node._id = 0
    for node in menu2.get_all_nodes():
        node._id = 0
    assert_equal(menu, menu2)
    pass