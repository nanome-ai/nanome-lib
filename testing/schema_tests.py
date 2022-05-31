import json
import os
import unittest

from nanome.api import structure, ui, shapes
from nanome.util import Vector3, enums, Color

# Schemas requirements are optional, so don't run tests if they are not installed.
reqs_installed = True
try:
    from nanome.api import schemas
except ModuleNotFoundError:
    reqs_installed = False

test_assets = os.path.join(os.getcwd(), "testing/test_assets")
workspace_json = os.path.join(test_assets, "serialized_data/benzene_workspace.json")
pdb_file = os.path.join(test_assets, "pdb/1tyl.pdb")
conformer_pdb = os.path.join(test_assets, "pdb/thrombine_conformer.pdb")
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

    def test_load_conformer_complex(self):
        comp = structure.Complex.io.from_pdb(path=conformer_pdb)
        mol = next(comp.molecules)
        conformer_count = mol.conformer_count
        self.assertEqual(conformer_count, 5)
        comp_json = schemas.ComplexSchema().dump(comp)
        loaded_comp = schemas.ComplexSchema().load(comp_json)
        loaded_mol = next(loaded_comp.molecules)
        self.assertEqual(loaded_mol.conformer_count, 5)


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
        with open(test_menu_json, 'r') as f:
            input_dict = json.load(f)
        menu = schemas.MenuSchema().load(input_dict)
        menu_dump = schemas.MenuSchema().dump(menu)
        second_menu = schemas.MenuSchema().load(menu_dump)
        second_menu_dump = schemas.MenuSchema().dump(second_menu)
        self.assertEqual(menu_dump, second_menu_dump)


@unittest.skipIf(not reqs_installed, "Marshmallow not installed")
class ShapeSchemaTestCase(unittest.TestCase):

    def test_dump_sphere(self):
        radius = 5
        color = Color.Blue()
        sphere1_position = Vector3(25, 100, 50)
        # Serialize sphere anchored to point in Workspace
        sphere1 = shapes.Sphere()
        sphere1.radius = radius
        sphere1.color = color
        anchor1 = sphere1.anchors[0]
        anchor1.anchor_type == enums.ShapeAnchorType.Workspace
        anchor1.local_offset = sphere1_position
        schema = schemas.SphereSchema()
        sphere1_dict = schema.dump(sphere1)
        self.assertEqual(sphere1_dict['radius'], radius)
        self.assertEqual(sphere1_dict['color'], list(color.rgba))
        anchor_dict = sphere1_dict['anchors'][0]
        anchor1.anchor_type == enums.ShapeAnchorType.Workspace
        self.assertEqual(
            anchor_dict['local_offset'],
            list(sphere1_position.unpack()))

    def test_dump_label(self):
        # Lets add a label that's centered on the line.
        label = shapes.Label()
        label.text = 'Label'
        anchor = label.anchors[0]
        for anchor in label.anchors:
            anchor.viewer_offset = Vector3(0, 0, -.1)
        label_dict = schemas.LabelSchema().dump(label)
        self.assertEqual(label_dict['text'], label.text)

    def test_dump_mesh(self):
        mesh = shapes.Mesh()
        # Create a cube
        mesh.vertices = [
            0.0, 20.0, 20.0, 0.0, 0.0, 20.0, 20.0, 0.0, 20.0, 20.0, 20.0, 20.0,
            0.0, 20.0, 0.0, 0.0, 0.0, 0.0, 20.0, 0.0, 0.0, 20.0, 20.0, 0.0]
        mesh.normals = [
            -0.408, 0.408, 0.817, -0.667, -0.667, 0.333, 0.408, -0.408, 0.817,
            0.667, 0.667, 0.333, -0.667, 0.667, -0.333, -0.408, -0.408, -0.817,
            0.667, -0.667, -0.333, 0.408, 0.408, -0.817]
        mesh.triangles = [
            0, 1, 2, 0, 2, 3, 7, 6, 5, 7, 5, 4, 3, 2, 6, 3, 6, 7, 4, 0, 3, 4, 3, 7, 4, 5, 1,
            4, 1, 0, 1, 5, 6, 1, 6, 2]

        mesh.anchors[0].anchor_type = enums.ShapeAnchorType.Workspace
        mesh.anchors[0].position = Vector3(0, 0, 0)
        mesh.color = Color(255, 255, 255, 255)
        mesh.colors = [
            1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0,
            0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0,
            0.0, 0.0, 1.0, 1.0]
        mesh_dict = schemas.MeshSchema().dump(mesh)
        self.assertEqual(mesh_dict['vertices'], mesh.vertices)
        self.assertEqual(mesh_dict['normals'], mesh.normals)
        self.assertEqual(mesh_dict['triangles'], mesh.triangles)
        self.assertEqual(mesh_dict['colors'], mesh.colors)
