import asyncio
import nanome
import unittest
from nanome._internal.process import _Bonding
from nanome.api import structure
import os
from unittest.mock import MagicMock


test_assets = os.getcwd() + ("/testing/test_assets")


def run_awaitable(awaitable, *args, **kwargs):
    loop = asyncio.get_event_loop()
    if loop.is_running:
        loop = asyncio.new_event_loop()
    loop.run_until_complete(awaitable(*args, **kwargs))
    loop.close()


class BondingTestCase(unittest.TestCase):

    def setUp(self):
        nanome.PluginInstance._instance = MagicMock()

    def test_bonding(self):
        pdb_file = os.path.join(test_assets, 'pdb', '3mcf.pdb')
        comp = structure.Complex.io.from_pdb(path=pdb_file)
        bond_count = sum(1 for _ in comp.bonds)
        self.assertEqual(bond_count, 0)

        complex_list = [comp]
        callback = None
        fast_mode = False
        plugin = MagicMock()
        bonding = _Bonding(plugin, complex_list, callback, fast_mode)
        bonding._start()
        expected_bond_count = 2134
        bond_count = sum(1 for _ in comp.bonds)
        self.assertEqual(bond_count, expected_bond_count)

    def test_bonding_conformer(self):
        pdb_file = os.path.join(test_assets, 'pdb', 'thrombine_conformer.pdb')
        expected_conformer_count = 5
        expected_atom_counts = [71, 71, 54, 54, 54]
        expected_bond_counts = [72, 72, 56, 56, 56]
        comp = structure.Complex.io.from_pdb(path=pdb_file)
        mol = next(comp.molecules)
        self.assertEqual(mol._conformer_count, expected_conformer_count)
        bond_count = sum(1 for _ in comp.bonds)
        self.assertEqual(bond_count, 0)

        complex_list = [comp]
        callback = None
        fast_mode = False
        plugin = MagicMock()
        bonding = _Bonding(plugin, complex_list, callback, fast_mode)
        bonding._start()
        # Make sure conformer count hasn't changed
        mol = next(comp.molecules)
        self.assertEqual(mol._conformer_count, expected_conformer_count)

        # Assert Bond count on all conformers
        mol = next(comp.molecules)
        for i in range(0, mol._conformer_count):
            mol.set_current_conformer(i)
            self.assertEqual(mol.current_conformer, i)
            conformer_atom_count = sum(1 for atm in mol.atoms if atm.in_conformer[i])
            conformer_bond_count = sum(1 for bnd in mol.bonds if bnd.in_conformer[i])
            expected_conf_atom_count = expected_atom_counts[i]
            expected_conf_bond_count = expected_bond_counts[i]
            self.assertEqual(conformer_atom_count, expected_conf_atom_count)
            self.assertEqual(conformer_bond_count, expected_conf_bond_count)

    def test_bonding_multiple_comps(self):
        pdb_file1 = os.path.join(test_assets, 'pdb', 'thrombine_conformer.pdb')
        pdb_file2 = os.path.join(test_assets, 'pdb', '1tyl.pdb')

        # Expected values for pdb_file1
        pdb1_expected_conformer_count = 5
        pdb1_expected_atom_counts = [71, 71, 54, 54, 54]
        pdb1_expected_bond_counts = [72, 72, 56, 56, 56]
        pdb1_comp = structure.Complex.io.from_pdb(path=pdb_file1)
        pdb1_mol = next(pdb1_comp.molecules)
        self.assertEqual(pdb1_mol._conformer_count, pdb1_expected_conformer_count)
        pdb1_bond_count = sum(1 for _ in pdb1_comp.bonds)
        self.assertEqual(pdb1_bond_count, 0)

        # Expected values for pdb_file2
        pdb2_expected_conformer_count = 1
        pdb2_expected_atom_counts = [915]
        pdb2_expected_bond_counts = [830]
        pdb2_comp = structure.Complex.io.from_pdb(path=pdb_file2)
        pdb2_mol = next(pdb2_comp.molecules)
        self.assertEqual(pdb2_mol._conformer_count, pdb2_expected_conformer_count)
        pdb2_bond_count = sum(1 for _ in pdb2_comp.bonds)
        self.assertEqual(pdb2_bond_count, 0)

        complex_list = [pdb1_comp, pdb2_comp]
        callback = None
        fast_mode = False
        plugin = MagicMock()
        bonding = _Bonding(plugin, complex_list, callback, fast_mode)
        bonding._start()
        # Make sure conformer count hasn't changed
        pdb1_mol = next(pdb1_comp.molecules)
        self.assertEqual(pdb1_mol._conformer_count, pdb1_expected_conformer_count)
        pdb2_mol = next(pdb2_comp.molecules)
        self.assertEqual(pdb2_mol._conformer_count, pdb2_expected_conformer_count)

        # PDB1 Assert Bond count on all conformers
        mol = next(pdb1_comp.molecules)
        for i in range(0, mol._conformer_count):
            mol.set_current_conformer(i)
            self.assertEqual(mol.current_conformer, i)
            conformer_atom_count = sum(1 for atm in mol.atoms if atm.in_conformer[i])
            conformer_bond_count = sum(1 for bnd in mol.bonds if bnd.in_conformer[i])
            expected_conf_atom_count = pdb1_expected_atom_counts[i]
            expected_conf_bond_count = pdb1_expected_bond_counts[i]
            self.assertEqual(conformer_atom_count, expected_conf_atom_count)
            self.assertEqual(conformer_bond_count, expected_conf_bond_count)

        # PDB2 Assert Bond count on all conformers
        mol = next(pdb2_comp.molecules)
        for i in range(0, mol._conformer_count):
            mol.set_current_conformer(i)
            self.assertEqual(mol.current_conformer, i)
            conformer_atom_count = sum(1 for atm in mol.atoms if atm.in_conformer[i])
            conformer_bond_count = sum(1 for bnd in mol.bonds if bnd.in_conformer[i])
            expected_conf_atom_count = pdb2_expected_atom_counts[i]
            expected_conf_bond_count = pdb2_expected_bond_counts[i]
            self.assertEqual(conformer_atom_count, expected_conf_atom_count)
            self.assertEqual(conformer_bond_count, expected_conf_bond_count)
