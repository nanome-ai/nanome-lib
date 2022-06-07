import json
import os
import sys
import tempfile
import unittest

from nanome.api import structure, ui, shapes, streams
from nanome.util import Vector3, enums, Color

if sys.version_info.major >= 3:
    from unittest.mock import MagicMock, patch
else:
    # Python 2.7 way of getting magicmock. Requires pip install mock
    from mock import MagicMock, patch

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
smina_menu_json = os.path.join(test_assets, "test_menu_smina.json")
test_menu_json = os.path.join(test_assets, "test_menu.json")


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

    def test_structure_schema_dump(self):
        """Make sure StructureSchema can parse the correct structure type."""
        with open(workspace_json, 'r') as f:
            workspace_data = json.load(f)
        workspace = schemas.WorkspaceSchema().load(workspace_data)
        comp = workspace.complexes[0]
        mol = next(comp.molecules)
        chain = next(comp.chains)
        residue = next(comp.residues)
        atom = next(comp.atoms)
        bond = next(comp.bonds)
        schema = schemas.StructureSchema()

        comp_data = schema.dump(comp)
        self.assertTrue(isinstance(comp_data, dict))
        reloaded_comp = schema.load(comp_data)
        self.assertTrue(isinstance(reloaded_comp, structure.Complex))

        mol_data = schema.dump(mol)
        self.assertTrue(isinstance(mol_data, dict))
        reloaded_mol = schema.load(mol_data)
        self.assertTrue(isinstance(reloaded_mol, structure.Molecule))

        chain_data = schema.dump(chain)
        self.assertTrue(isinstance(chain_data, dict))
        reloaded_chain = schema.load(chain_data)
        self.assertTrue(isinstance(reloaded_chain, structure.Chain))

        residue_data = schema.dump(residue)
        self.assertTrue(isinstance(residue_data, dict))
        reloaded_residue = schema.load(residue_data)
        self.assertTrue(isinstance(reloaded_residue, structure.Residue))

        bond_data = schema.dump(bond)
        self.assertTrue(isinstance(bond_data, dict))
        reloaded_bond = schema.load(bond_data)
        self.assertTrue(isinstance(reloaded_bond, structure.Bond))

        atom_data = schema.dump(atom)
        self.assertTrue(isinstance(atom_data, dict))
        reloaded_atom = schema.load(atom_data)
        self.assertTrue(isinstance(reloaded_atom, structure.Atom))

    def test_structure_schema_load(self):
        """Make sure StructureSchema can parse the correct structure type."""
        with open(workspace_json, 'r') as f:
            workspace_data = json.load(f)
        struct_schema = schemas.StructureSchema()

        comp_data = workspace_data['complexes'][0]
        comp = struct_schema.load(comp_data)
        self.assertTrue(isinstance(comp, structure.Complex))

        mol_data = comp_data['molecules'][0]
        mol = struct_schema.load(mol_data)
        self.assertTrue(isinstance(mol, structure.Molecule))

        chain_data = mol_data['chains'][0]
        chain = struct_schema.load(chain_data)
        self.assertTrue(isinstance(chain, structure.Chain))

        residue_data = chain_data['residues'][0]
        residue = struct_schema.load(residue_data)
        self.assertTrue(isinstance(residue, structure.Residue))

        bond_data = residue_data['bonds'][0]
        bond = struct_schema.load(bond_data)
        self.assertTrue(isinstance(bond, structure.Bond))

        atom_data = residue_data['atoms'][0]
        atom = struct_schema.load(atom_data)
        self.assertTrue(isinstance(atom, structure.Atom))


@unittest.skipIf(not reqs_installed, "Marshmallow not installed")
class UISchemaTestCase(unittest.TestCase):

    def test_load_menu(self):
        """Ensure loading menu with serializers equivalent to Menu.io.from_json."""
        reference_menu = ui.Menu.io.from_json(path=smina_menu_json)
        with open(smina_menu_json, 'r') as f:
            menu_dict = json.load(f)
        menu = schemas.MenuSchema().load(menu_dict)
        self.assertTrue(isinstance(menu, ui.Menu))
        self.assertTrue(isinstance(menu.root, ui.LayoutNode))

        # Make sure menu can be serialized back to json.
        test_export = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        menu.io.to_json(test_export.name)
        with open(test_export.name, 'r') as f:
            exported_data = json.loads(f.read())
            self.assertTrue(isinstance(exported_data, dict))
        test_export.close()

        # Make sure all content in reference menu was loaded
        menu_content_types = [
            content.__class__ for content in menu.get_all_content()]
        self.assertTrue(menu_content_types)
        reference_menu_content_types = [content.__class__ for content in reference_menu.get_all_content()]
        self.assertEqual(menu_content_types, reference_menu_content_types)

        # Check that Button values match the reference menu
        reference_menu_btn = next(content for content in reference_menu.get_all_content() if isinstance(content, ui.Button))
        menu_btn = next(content for content in menu.get_all_content() if isinstance(content, ui.Button))
        # ButtonText fields
        self.assertEqual(menu_btn.text.value.idle, reference_menu_btn.text.value.idle)
        self.assertEqual(menu_btn.text.value.highlighted, reference_menu_btn.text.value.highlighted)
        self.assertEqual(menu_btn.text.value.selected, reference_menu_btn.text.value.selected)
        self.assertEqual(menu_btn.text.value.unusable, reference_menu_btn.text.value.unusable)
        self.assertEqual(menu_btn.text.bold.idle, reference_menu_btn.text.bold.idle)
        self.assertEqual(menu_btn.text.bold.highlighted, reference_menu_btn.text.bold.highlighted)
        self.assertEqual(menu_btn.text.bold.selected, reference_menu_btn.text.bold.selected)
        self.assertEqual(menu_btn.text.bold.unusable, reference_menu_btn.text.bold.unusable)
        self.assertEqual(menu_btn.text.color.idle.hex, reference_menu_btn.text.color.idle.hex)
        self.assertEqual(menu_btn.text.color.highlighted.hex, reference_menu_btn.text.color.highlighted.hex)
        self.assertEqual(menu_btn.text.color.selected.hex, reference_menu_btn.text.color.selected.hex)
        self.assertEqual(menu_btn.text.color.unusable.hex, reference_menu_btn.text.color.unusable.hex)
        # Test outline values
        self.assertEqual(menu_btn.outline.color.idle.hex, reference_menu_btn.outline.color.idle.hex)
        self.assertEqual(menu_btn.outline.color.highlighted.hex, reference_menu_btn.outline.color.highlighted.hex)
        self.assertEqual(menu_btn.outline.color.selected.hex, reference_menu_btn.outline.color.selected.hex)
        self.assertEqual(menu_btn.outline.color.unusable.hex, reference_menu_btn.outline.color.unusable.hex)
        self.assertEqual(menu_btn.outline.size.idle, reference_menu_btn.outline.size.idle)
        self.assertEqual(menu_btn.outline.size.highlighted, reference_menu_btn.outline.size.highlighted)
        self.assertEqual(menu_btn.outline.size.selected, reference_menu_btn.outline.size.selected)
        self.assertEqual(menu_btn.outline.size.unusable, reference_menu_btn.outline.size.unusable)
        # assert mesh colors
        self.assertEqual(menu_btn.mesh.active, reference_menu_btn.mesh.active)
        self.assertEqual(menu_btn.mesh.color.idle.hex, reference_menu_btn.mesh.color.idle.hex)
        self.assertEqual(menu_btn.mesh.color.highlighted.hex, reference_menu_btn.mesh.color.highlighted.hex)
        self.assertEqual(menu_btn.mesh.color.selected.hex, reference_menu_btn.mesh.color.selected.hex)
        self.assertEqual(menu_btn.mesh.color.unusable.hex, reference_menu_btn.mesh.color.unusable.hex)
        # tooltip
        self.assertEqual(menu_btn.tooltip.title, reference_menu_btn.tooltip.title)
        self.assertEqual(menu_btn.tooltip.content, reference_menu_btn.tooltip.content)
        self.assertEqual(menu_btn.tooltip.bounds, reference_menu_btn.tooltip.bounds)
        self.assertEqual(menu_btn.tooltip.positioning_target, reference_menu_btn.tooltip.positioning_target)
        self.assertEqual(menu_btn.tooltip.positioning_origin, reference_menu_btn.tooltip.positioning_origin)
        # icons
        self.assertEqual(menu_btn.icon.active, reference_menu_btn.icon.active)
        self.assertEqual(menu_btn.icon.color.idle.hex, reference_menu_btn.icon.color.idle.hex)
        self.assertEqual(menu_btn.icon.color.highlighted.hex, reference_menu_btn.icon.color.highlighted.hex)
        self.assertEqual(menu_btn.icon.color.selected.hex, reference_menu_btn.icon.color.selected.hex)
        self.assertEqual(menu_btn.icon.color.unusable.hex, reference_menu_btn.icon.color.unusable.hex)
        self.assertEqual(menu_btn.icon.value.idle, reference_menu_btn.icon.value.idle)
        self.assertEqual(menu_btn.icon.value.highlighted, reference_menu_btn.icon.value.highlighted)
        self.assertEqual(menu_btn.icon.value.selected, reference_menu_btn.icon.value.selected)
        self.assertEqual(menu_btn.icon.value.unusable, reference_menu_btn.icon.value.unusable)

    def test_button_dump(self):
        """Test that all the nested values of a Button are dumped correctly."""
        menu = ui.Menu.io.from_json(test_menu_json)
        menu_dump = schemas.MenuSchema().dump(menu)
        menu_btn = next(
            content for content in menu.get_all_content()
            if isinstance(content, ui.Button))
        btn_data = menu_dump['effective_root']['children'][0]['children'][0]['content']
        # Test outline data
        self.assertEqual(round(btn_data['outline_size_idle'], 2), round(menu_btn.outline.size.idle, 2))
        self.assertEqual(round(btn_data['outline_size_selected'], 2), round(menu_btn.outline.size.selected, 2))
        self.assertEqual(round(btn_data['outline_size_highlighted'], 2), round(menu_btn.outline.size.highlighted, 2))
        self.assertEqual(round(btn_data['outline_size_selected_highlighted'], 2), round(menu_btn.outline.size.selected_highlighted, 2))
        self.assertEqual(round(btn_data['outline_size_unusable'], 2), round(menu_btn.outline.size.unusable, 2))
        # ButtonText data
        self.assertEqual(btn_data['text_value_idle'], menu_btn.text.value.idle)
        self.assertEqual(btn_data['text_value_highlighted'], menu_btn.text.value.highlighted)
        self.assertEqual(btn_data['text_value_selected'], menu_btn.text.value.selected)
        self.assertEqual(btn_data['text_value_selected_highlighted'], menu_btn.text.value.selected_highlighted)
        self.assertEqual(btn_data['text_value_unusable'], menu_btn.text.value.unusable)
        self.assertEqual(btn_data['text_bold_idle'], menu_btn.text.bold.idle)
        self.assertEqual(btn_data['text_bold_highlighted'], menu_btn.text.bold.highlighted)
        self.assertEqual(btn_data['text_bold_selected'], menu_btn.text.bold.selected)
        self.assertEqual(btn_data['text_bold_unusable'], menu_btn.text.bold.unusable)
        self.assertEqual(btn_data['text_color_idle'], menu_btn.text.color.idle._color)
        self.assertEqual(btn_data['text_color_highlighted'], menu_btn.text.color.highlighted._color)
        self.assertEqual(btn_data['text_color_selected'], menu_btn.text.color.selected._color)
        self.assertEqual(btn_data['text_color_unusable'], menu_btn.text.color.unusable._color)
        self.assertEqual(btn_data['text_min_size'], menu_btn.text.min_size)
        self.assertEqual(btn_data['text_max_size'], menu_btn.text.max_size)
        self.assertEqual(btn_data['text_size'], menu_btn.text_size)
        self.assertEqual(btn_data['text_underlined'], menu_btn.text_underlined)
        self.assertEqual(btn_data['text_vertical_align'], menu_btn.text_vertical_align)
        self.assertEqual(btn_data['text_horizontal_align'], menu_btn.text_horizontal_align)
        self.assertEqual(btn_data['text_ellipsis'], menu_btn.text.ellipsis)
        self.assertEqual(btn_data['text_padding_top'], menu_btn.text_padding_top)
        self.assertEqual(btn_data['text_padding_bottom'], menu_btn.text_padding_bottom)
        self.assertEqual(btn_data['text_padding_left'], menu_btn.text_padding_left)
        self.assertEqual(btn_data['text_padding_right'], menu_btn.text_padding_right)
        self.assertEqual(btn_data['text_line_spacing'], menu_btn.text.line_spacing)
        # Icons
        self.assertEqual(btn_data['icon_active'], menu_btn.icon.active)
        self.assertEqual(btn_data['icon_color_idle'], menu_btn.icon.color.idle._color)
        self.assertEqual(btn_data['icon_color_highlighted'], menu_btn.icon.color.highlighted._color)
        self.assertEqual(btn_data['icon_color_selected'], menu_btn.icon.color.selected._color)
        self.assertEqual(btn_data['icon_color_unusable'], menu_btn.icon.color.unusable._color)
        self.assertEqual(btn_data['icon_value_idle'], menu_btn.icon.value.idle)
        self.assertEqual(btn_data['icon_value_highlighted'], menu_btn.icon.value.highlighted)
        self.assertEqual(btn_data['icon_value_selected'], menu_btn.icon.value.selected)
        self.assertEqual(btn_data['icon_value_unusable'], menu_btn.icon.value.unusable)
        # Meshes
        self.assertEqual(btn_data['mesh_active'], menu_btn.mesh.active)
        self.assertEqual(btn_data['mesh_enabled_idle'], menu_btn.mesh.enabled.idle)
        self.assertEqual(btn_data['mesh_enabled_selected'], menu_btn.mesh.enabled.selected)
        self.assertEqual(btn_data['mesh_enabled_highlighted'], menu_btn.mesh.enabled.highlighted)
        self.assertEqual(btn_data['mesh_enabled_selected_highlighted'], menu_btn.mesh.enabled.selected_highlighted)
        self.assertEqual(btn_data['mesh_enabled_unusable'], menu_btn.mesh.enabled.unusable)
        self.assertEqual(btn_data['mesh_color_idle'], menu_btn.mesh.color.idle._color)
        self.assertEqual(btn_data['mesh_color_selected'], menu_btn.mesh.color.selected._color)
        self.assertEqual(btn_data['mesh_color_highlighted'], menu_btn.mesh.color.highlighted._color)
        self.assertEqual(btn_data['mesh_color_selected_highlighted'], menu_btn.mesh.color.selected_highlighted._color)
        self.assertEqual(btn_data['mesh_color_unusable'], menu_btn.mesh.color.unusable._color)
        # Tooltips
        self.assertEqual(btn_data['tooltip_title'], menu_btn.tooltip.title)
        self.assertEqual(btn_data['tooltip_content'], menu_btn.tooltip.content)
        self.assertEqual(round(btn_data['tooltip_bounds']['x'], 2), round(menu_btn.tooltip.bounds.x, 2))
        self.assertEqual(round(btn_data['tooltip_bounds']['y'], 2), round(menu_btn.tooltip.bounds.y, 2))
        self.assertEqual(round(btn_data['tooltip_bounds']['z'], 2), round(menu_btn.tooltip.bounds.z, 2))
        self.assertEqual(btn_data['tooltip_positioning_target'], menu_btn.tooltip.positioning_target)
        self.assertEqual(btn_data['tooltip_positioning_origin'], menu_btn.tooltip.positioning_origin)

    def test_dump_menu_idempotent(self):
        """Ensure that dumping menu from serializers returns same input json."""
        with open(smina_menu_json, 'r') as f:
            input_dict = json.load(f)
        menu = schemas.MenuSchema().load(input_dict)
        menu_dump = schemas.MenuSchema().dump(menu)
        second_menu = schemas.MenuSchema().load(menu_dump)
        second_menu_dump = schemas.MenuSchema().dump(second_menu)
        self.assertEqual(menu_dump, second_menu_dump)

    def test_btn_switch_fields(self):
        """Test btn switch values that are not included in StackStudio exports."""
        with open(test_menu_json, 'r') as f:
            input_dict = json.load(f)
        menu = schemas.MenuSchema().load(input_dict)
        menu_btn = next(
            content for content in menu.get_all_content()
            if isinstance(content, ui.Button))
        menu_btn.switch.active = True
        menu_btn.switch.on_color = Color.Red()
        menu_btn.switch.off_color = Color.Blue()
        menu_dump = schemas.MenuSchema().dump(menu)
        btn_data = menu_dump['effective_root']['children'][0]['children'][0]['content']
        self.assertEqual(btn_data.get('switch_active'), menu_btn.switch.active)
        self.assertEqual(btn_data.get('switch_on_color'), menu_btn.switch.on_color._color)
        self.assertEqual(btn_data.get('switch_off_color'), menu_btn.switch.off_color._color)

    def test_btn_icon_value_fields(self):
        """Test icon values that are not included in StackStudio exports, but we actually want."""
        with open(test_menu_json, 'r') as f:
            input_dict = json.load(f)
        menu = schemas.MenuSchema().load(input_dict)
        menu_btn = next(
            content for content in menu.get_all_content()
            if isinstance(content, ui.Button))
        menu_btn.icon.value.set_all("/path/to/icon.png")
        menu_dump = schemas.MenuSchema().dump(menu)
        btn_data = menu_dump['effective_root']['children'][0]['children'][0]['content']
        self.assertEqual(btn_data.get('icon_value_idle'), menu_btn.icon.value.idle)
        self.assertEqual(btn_data.get('icon_value_selected'), menu_btn.icon.value.selected)
        self.assertEqual(btn_data.get('icon_value_highlighted'), menu_btn.icon.value.highlighted)
        self.assertEqual(btn_data.get('icon_value_selected_highlighted'), menu_btn.icon.value.selected_highlighted)
        self.assertEqual(btn_data.get('icon_value_unusable'), menu_btn.icon.value.unusable)


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


@unittest.skipIf(not reqs_installed, "Marshmallow not installed")
class StreamSchemaTestCase(unittest.TestCase):

    def test_stream_dump(self):
        network = MagicMock()
        stream_id = 5
        data_type = enums.StreamDataType.string
        direction = enums.StreamDirection.writing
        stream = streams.Stream(network, stream_id, data_type, direction)
        stream_dump = schemas.StreamSchema().dump(stream)
        self.assertEqual(stream_dump['id'], stream_id)
        self.assertEqual(stream_dump['data_type'], data_type.value)
        self.assertEqual(stream_dump['direction'], direction.value)
