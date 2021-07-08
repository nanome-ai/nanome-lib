import os
import unittest

from nanome.api.structure import Complex
from nanome.util.complex_utils import ComplexUtils


BASE_DIR = os.path.join(os.path.dirname(__file__))


class CopmlexUtilsTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.complex1 = Complex.io.from_pdb(path=f'{BASE_DIR}/test_assets/pdb/1a9l.pdb')
        self.complex2 = Complex.io.from_pdb(path=f'{BASE_DIR}/test_assets/pdb/1fsv.pdb')

    def test_setup(self):
        assert isinstance(self.complex1, Complex)
        assert isinstance(self.complex2, Complex)

    def test_align_to(self):
        ComplexUtils.align_to(self.complex1, self.complex2)

    def test_combine_ligands(self):
        ComplexUtils.combine_ligands(self.complex1, [self.complex2])

    def test_convert_to_conformers(self):
        ComplexUtils.convert_to_conformers([self.complex1])

    def test_convert_to_frames(self):
        ComplexUtils.convert_to_frames([self.complex1])

    def test_reset_transform(self):
        ComplexUtils.align_to(self.complex1, self.complex2)
        ComplexUtils.reset_transform(self.complex1)
