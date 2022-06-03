import os
import unittest

from nanome.api.structure import Complex
from nanome.util import ComplexUtils


test_assets = os.path.join(os.getcwd(), 'testing', 'test_assets')


class ComplexUtilsTestCase(unittest.TestCase):
    def setUp(self):
        super(ComplexUtilsTestCase, self).setUp()
        complex_1_pdb = os.path.join(test_assets, 'pdb', '1a9l.pdb')
        complex_2_pdb = os.path.join(test_assets, 'pdb', '1fsv.pdb')
        self.complex1 = Complex.io.from_pdb(path=complex_1_pdb)
        self.complex2 = Complex.io.from_pdb(path=complex_2_pdb)

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
