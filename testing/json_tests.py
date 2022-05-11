import os
import unittest

from nanome.api.ui import Menu, LayoutNode
import tempfile

from testing.utilities import *


test_assets = os.getcwd() + ("/testing/test_assets")
test_output_dir = "/tmp/testing/test_outputs"

BASE_DIR = os.path.join(os.path.dirname(__file__))

class JsonTestCase(unittest.TestCase):

    def test_menu_json(self):
        test_path = test_assets + "/test_menu.json"
        output_path = tempfile.NamedTemporaryFile(suffix='.json').name

        menu = Menu.io.from_json(test_path)
        menu.io.to_json(output_path)
        menu2 = Menu.io.from_json(output_path)
        for node in menu.get_all_nodes():
            node._id = 0
        for node in menu2.get_all_nodes():
            node._id = 0
        for content in menu.get_all_content():
            content._content_id = 0
        for content in menu2.get_all_content():
            content._content_id = 0
        assert_equal(menu, menu2)

    def test_text_layout_node_json(self):
        test_path = test_assets + "/test_menu.json"
        output_path = tempfile.NamedTemporaryFile(suffix='.json').name
        menu = Menu.io.from_json(test_path)
        root = menu.root
        root.io.to_json(output_path)
        root2 = LayoutNode.io.from_json(output_path)

        menu = Menu()
        menu2 = Menu()
        menu.root = root
        menu2.root = root2
        for node in menu.get_all_nodes():
            node._id = 0
        for node in menu2.get_all_nodes():
            node._id = 0
        for content in menu.get_all_content():
            content._content_id = 0
        for content in menu2.get_all_content():
            content._content_id = 0
        assert_equal(menu, menu2)
