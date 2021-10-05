import os
import unittest
import pickle

from nanome.api.structure import Complex
from nanome.util import ComplexUtils


BASE_DIR = os.path.join(os.path.dirname(__file__))


class ComplexUtilsTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        with open(f"{BASE_DIR}/test_assets/pickles/1a9l.pickle", "rb") as f:
            self.complex1 = pickle.load(f)

        with open(f"{BASE_DIR}/test_assets/pickles/1fsv.pickle", "rb") as f:
            self.complex2 = pickle.load(f)

    def test_align_to(self):
        ComplexUtils.align_to(self.complex1, self.complex2)

    def test_combine_ligands(self):
        complex1_mol_count = len(list(self.complex1.molecules))
        complex2_mol_count = len(list(self.complex2.molecules))
        combined_ligands = ComplexUtils.combine_ligands(self.complex1, [self.complex1, self.complex2])
        combined_ligands_mol_count = len(list(combined_ligands.molecules))
        self.assertEqual(combined_ligands_mol_count, complex1_mol_count + complex2_mol_count)

    def test_convert_to_conformers(self):
        ComplexUtils.convert_to_conformers([self.complex1])

    def test_convert_to_frames(self):
        ComplexUtils.convert_to_frames([self.complex1])

    def test_reset_transform(self):
        ComplexUtils.align_to(self.complex1, self.complex2)
        ComplexUtils.reset_transform(self.complex1)
