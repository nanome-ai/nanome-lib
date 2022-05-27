import os
import unittest

from nanome.api.structure import Complex

test_assets = os.getcwd() + ("/testing/test_assets")


class ComplexTestCase(unittest.TestCase):

    def setUp(self):
        input_dir = test_assets + ("/sdf/Thrombin_100cmpds (1).sdf")  # withbonds
        # input_dir = test_assets + ("/pdb/1fsv.pdb") # smallboy
        # input_dir = test_assets + ("/pdb/1a9l.pdb") # bigboy
        self.complex = Complex.io.from_sdf(path=input_dir)

    def test_boxed(self):
        self.assertTrue(isinstance(self.complex.boxed, bool))

    def test_box_label(self):
        box_label = "Box Label"
        self.complex.box_label = box_label
        self.assertEqual(self.complex.box_label, box_label)

    def test_locked(self):
        self.assertFalse(self.complex.locked)
        self.complex.locked = True
        self.assertTrue(self.complex.locked)

    def test_visible(self):
        self.assertTrue(self.complex.visible)
        self.complex.visible = False
        self.assertFalse(self.complex.locked)

    def test_computing(self):
        self.assertFalse(self.complex.computing)
        self.complex.computing = True
        self.assertTrue(self.complex.computing)

    def test_current_frame(self):
        self.assertEqual(self.complex.current_frame, 0)

    def test_get_all_selected(self):
        self.complex.set_all_selected(False)
        self.assertFalse(self.complex.get_all_selected())
        self.complex.set_all_selected(True)
        self.assertTrue(self.complex.get_all_selected())

    def test_get_selected(self):
        self.assertFalse(self.complex.get_selected())

    def test_set_surface_needs_redraw(self):
        self.complex.set_surface_needs_redraw()
        self.assertTrue(self.complex._surface_dirty)

    def test_get_workspace_to_complex_matrix(self):
        self.complex.get_workspace_to_complex_matrix()

    def test_get_complex_to_workspace_matrix(self):
        self.complex.get_workspace_to_complex_matrix()

    def test_full_name(self):
        comp_name = 'Test Complex'
        self.complex.full_name = comp_name
        self.assertEqual(self.complex.full_name, comp_name)

        new_comp_name = 'New complex name'
        self.complex.full_name = new_comp_name

        # Test full name using index and split tags.
        index_tag = 1
        split_tag = 'a'
        self.complex._index_tag = index_tag
        self.complex._split_tag = split_tag
        expected_name = "{} {{{}-{}}}".format(new_comp_name, index_tag, split_tag)
        self.assertEqual(self.complex.full_name, expected_name)

        # Test just a split tag
        self.complex._index_tag = 0
        expected_name = "{} {{{}}}".format(new_comp_name, split_tag)
        self.assertEqual(self.complex.full_name, expected_name)

    def test_name(self):
        comp_name = 'Test Complex'
        self.complex.name = comp_name
        self.assertEqual(self.complex.name, comp_name)
