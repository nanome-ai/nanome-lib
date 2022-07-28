import os
from nanome.api.ui import Menu
from nanome.api.ui import LayoutNode
from testing.unit.utilities import *
import unittest
import tempfile

test_assets = os.getcwd() + ("/testing/test_assets")
test_output_dir = os.getcwd() + ("/testing/test_outputs")


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

    def test_layoutnode_clone_enabled(self):
        """Tests that bug is resolved where enabled field not copied during clone."""
        test_path = test_assets + "/test_menu.json"
        output_path = tempfile.NamedTemporaryFile(suffix='.json').name
        menu = Menu.io.from_json(test_path)
        root = menu.root
        root.io.to_json(output_path)
        layoutnode = LayoutNode.io.from_json(output_path)
        child_node = layoutnode.get_children()[0]
        self.assertEqual(child_node.enabled, True)
        # Clone the layoutnode, and make sure the enabled field stays false
        child_node.enabled = False
        new_layoutnode = layoutnode.clone()
        new_child_node = new_layoutnode.get_children()[0]
        self.assertEqual(new_child_node.enabled, False)
