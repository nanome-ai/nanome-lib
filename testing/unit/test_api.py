import os
from nanome._internal import _ui, _structure
from nanome.api import ui, structure
from testing.unit.utilities import assert_equal

import unittest

test_assets = os.getcwd() + ("/testing/test_assets")
test_output_dir = os.getcwd() + ("/testing/test_outputs")


class ApiTestCase(unittest.TestCase):

    def test_ui_creates(self):
        assert_equal(ui.Menu().__class__, _ui._Menu._create().__class__)
        assert_equal(ui.LayoutNode().__class__, _ui._LayoutNode._create().__class__)
        assert_equal(ui.Button().__class__, _ui._Button._create().__class__)
        assert_equal(ui.Mesh().__class__, _ui._Mesh._create().__class__)
        assert_equal(ui.Slider().__class__, _ui._Slider._create().__class__)
        assert_equal(ui.Label().__class__, _ui._Label._create().__class__)
        assert_equal(ui.TextInput().__class__, _ui._TextInput._create().__class__)
        assert_equal(ui.UIList().__class__, _ui._UIList._create().__class__)

    def test_structure_creates(self):
        assert_equal(structure.Atom().__class__, _structure._Atom._create().__class__)
        assert_equal(structure.Bond().__class__, _structure._Bond._create().__class__)
        assert_equal(structure.Residue().__class__, _structure._Residue._create().__class__)
        assert_equal(structure.Chain().__class__, _structure._Chain._create().__class__)
        assert_equal(structure.Molecule().__class__, _structure._Molecule._create().__class__)
        assert_equal(structure.Complex().__class__, _structure._Complex._create().__class__)
        assert_equal(structure.Workspace().__class__, _structure._Workspace._create().__class__)
