import os
import unittest

from nanome.api.structure import Complex
from nanome.api.structure.schemas import ComplexSchema

from testing.utilities import *

test_assets = os.getcwd() + ("/testing/test_assets")
test_output_dir = "/tmp/testing/test_outputs"

BASE_DIR = os.path.join(os.path.dirname(__file__))


class ComplexSchemaTestCase(unittest.TestCase):

    def setUp(self):
        super(ComplexSchemaTestCase, self).setUp()
        pdb_comp_1 = f'{BASE_DIR}/test_assets/pdb/1a9l.pdb'
        pdb_comp_2 = f'{BASE_DIR}/test_assets/pdb/1tyl.pdb'
        self.complex1 = Complex.io.from_pdb(path=pdb_comp_1)
        self.complex2 = Complex.io.from_pdb(path=pdb_comp_2)

    def test_complex_load(self):
        atom1_dict = {
            'index': 1234,
        }
        atom2_dict = {
            'index': 1235,
        }
        bond_dict = {
            'index': 720,
            'atom1': 1234,
            'atom2': 1235,
        }
        residue_dict = {
            'index': 678765,
            'atoms': [atom1_dict, atom2_dict],
            'bonds': [bond_dict],
        }
        chain_dict = {
            'index': 64356,
            'name': 'A',
            'residues': [residue_dict],
        }
        molecule_dict = {
            'index': 23434567,
            'current_conformer': 0,
            'chains': [chain_dict]
        }
        comp_data = {
            'index': 123,
            'current_frame': 1,
            'boxed': True,
            'locked': True,
            'visible': True,
            'computing': False,
            'box_label': 'iambox',
            'name': 'Complex 1',
            'position': [14.2, 23.2, 3.3],
            'rotation': [54.2, 43.2, 3.4, 9.3],
            'molecules': [
                molecule_dict
            ],
        }
        new_comp = ComplexSchema().load(comp_data)
        self.assertEqual(new_comp.index, comp_data['index'])
        
        mol = next(new_comp.molecules)
        self.assertEqual(mol.index, molecule_dict['index'])

        chain = next(mol.chains)
        self.assertEqual(chain.index, chain_dict['index'])

        residue = next(chain.residues)
        self.assertEqual(residue.index, residue_dict['index'])

        atom = next(residue.atoms)
        self.assertEqual(atom.index, atom1_dict['index'])

        bond = next(residue.bonds)
        self.assertEqual(bond.atom1.index, bond_dict['atom1'])
        self.assertEqual(bond.atom2.index, bond_dict['atom2'])
        

