import json
import os
import unittest
import difflib
import pprint

from nanome.api import structure, ui

# Schemas requirements are optional, so don't run tests if they are not installed.
reqs_installed = True
try:
    from nanome.api import schemas
except ModuleNotFoundError:
    reqs_installed = False

test_assets = os.path.join(os.getcwd(), "testing/test_assets")
workspace_json = os.path.join(test_assets, "serialized_data/benzene_workspace.json")
pdb_file = os.path.join(test_assets, "pdb/1tyl.pdb")
test_menu_json = os.path.join(test_assets, "test_menu_smina.json")


@unittest.skipIf(not reqs_installed, "Marshmallow not installed")
class StructureSchemaTestCase(unittest.TestCase):

    def test_load_workspace(self):
        with open(workspace_json, 'r') as f:
            """Deserialize a workspace from JSON."""
            workspace_data = json.load(f)
            workspace = schemas.WorkspaceSchema().load(workspace_data)
            self.assertTrue(isinstance(workspace, structure.Workspace))

    def test_dump_complex(self):
        # Serialize a complex into JSON.
        comp = structure.Complex.io.from_pdb(path=pdb_file)
        self.assertTrue(isinstance(comp, structure.Complex))
        comp_json = schemas.ComplexSchema().dump(comp)
        self.assertTrue(isinstance(comp_json, dict))


@unittest.skipIf(not reqs_installed, "Marshmallow not installed")
class UISchemaTestCase(unittest.TestCase):

    def test_load_menu(self):
        """Ensure loading menu with serializers equivalent to Menu.io.from_json."""
        test_menu = ui.Menu.io.from_json(path=test_menu_json)
        with open(test_menu_json, 'r') as f:
            menu_dict = json.load(f)
        menu = schemas.MenuSchema().load(menu_dict)
        self.assertTrue(isinstance(menu, ui.Menu))
        self.assertTrue(isinstance(menu.root, ui.LayoutNode))

        # Make sure all content was loaded.
        menu_content_types = [
            content.__class__ for content in menu.get_all_content()]
        self.assertTrue(menu_content_types)
        test_menu_content_types = [content.__class__ for content in test_menu.get_all_content()]
        self.assertEqual(menu_content_types, test_menu_content_types)

        # Test that multi state variables loaded correctly.
        test_menu_btn = next(content for content in test_menu.get_all_content() if isinstance(content, ui.Button))
        menu_btn = next(content for content in menu.get_all_content() if isinstance(content, ui.Button))
        self.assertEqual(menu_btn.text.value.idle, test_menu_btn.text.value.idle)
        self.assertEqual(menu_btn.text.value.highlighted, test_menu_btn.text.value.highlighted)
        self.assertEqual(menu_btn.text.value.selected, test_menu_btn.text.value.selected)
        self.assertEqual(menu_btn.text.value.unusable, test_menu_btn.text.value.unusable)
        # Test outline values
        self.assertEqual(menu_btn.outline.color.idle.hex, test_menu_btn.outline.color.idle.hex)
        self.assertEqual(menu_btn.outline.color.highlighted.hex, test_menu_btn.outline.color.highlighted.hex)
        self.assertEqual(menu_btn.outline.color.selected.hex, test_menu_btn.outline.color.selected.hex)
        self.assertEqual(menu_btn.outline.color.unusable.hex, test_menu_btn.outline.color.unusable.hex)
        self.assertEqual(menu_btn.outline.size.idle, test_menu_btn.outline.size.idle)
        self.assertEqual(menu_btn.outline.size.highlighted, test_menu_btn.outline.size.highlighted)
        self.assertEqual(menu_btn.outline.size.selected, test_menu_btn.outline.size.selected)
        self.assertEqual(menu_btn.outline.size.unusable, test_menu_btn.outline.size.unusable)

    def test_dump_menu(self):
        """Ensure that dumping menu from serializers returns same input json."""
        # self.maxDiff = None
        with open(test_menu_json, 'r') as f:
            input_dict = json.load(f)
        menu = schemas.MenuSchema().load(input_dict)
        menu_dump = schemas.MenuSchema().dump(menu)
        second_menu = schemas.MenuSchema().load(menu_dump)
        second_menu_dump = schemas.MenuSchema().dump(second_menu)
        self.assertEqual(menu_dump, second_menu_dump)
