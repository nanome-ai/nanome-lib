import os
import types
import unittest

from nanome.api import structure as struct
from nanome import util


test_assets = os.path.join(os.getcwd(), 'testing', 'test_assets')


class CopyTestCase(unittest.TestCase):
    """Validate Structure shallow and deep copy functions."""

    @classmethod
    def setUpClass(cls):
        pdb_path = os.path.join(test_assets, 'pdb', 'thrombine_conformer.pdb')
        cls.complex = struct.Complex.io.from_pdb(path=pdb_path)
        # Add a random bond to test with.
        atom1 = next(cls.complex.atoms)
        atom2 = next(cls.complex.atoms)
        residue = next(cls.complex.residues)
        bond = struct.Bond()
        bond.atom1 = atom1
        bond.atom2 = atom2
        bond.kind = util.enums.Kind.CovalentSingle
        residue.add_bond(bond)
        # These are the fields we want to validate are copied between structs.
        cls.atom_fields = [
            'index', 'selected', 'labeled', 'atom_rendering', 'surface_rendering',
            'exists', 'is_het', 'occupancy', 'bfactor', 'acceptor', 'donor', 'polar_hydrogen',
            'atom_mode', 'serial', 'current_conformer', 'positions', 'label_text', 'atom_color',
            'atom_scale', 'surface_color', 'surface_opacity', 'symbol', 'name', 'position',
            'formal_charge', 'partial_charge', 'vdw_radius', 'alt_loc', 'is_het',
            'in_conformer', 'het_surfaced', '_display_mode',
        ]
        cls.residue_fields = [
            'index', 'atoms', 'bonds', 'ribboned', 'ribbon_size', 'ribbon_mode',
            'ribbon_color', 'labeled', 'label_text', 'type', 'serial', 'name',
            'secondary_structure', 'ignored_alt_locs',
        ]
        cls.bond_fields = [
            'index', 'atom1', 'atom2', 'kind', 'in_conformer', 'kinds',
        ]

        cls.chain_fields = [
            'index', 'name', 'residues'
        ]
        cls.molecule_fields = [
            'index', 'chains', 'name', 'associated', 'conformer_count',
            'current_conformer', 'names', 'associateds',
        ]
        cls.complex_fields = [
            'index', 'boxed', 'locked', 'visible', 'computing', 'box_label',
            'name', 'index_tag', 'split_tag', 'position', 'rotation', 'molecules',
            'current_frame', 'remarks',
        ]

    def test_shallow_copy_atom(self):
        atom = next(self.complex.atoms)
        atom_copy = atom._shallow_copy()
        # Assert copy is a different object in memory
        self.assertTrue(atom_copy is not atom)
        self.validate_fields(atom, atom_copy, self.atom_fields)
        # Assert no residue copied
        self.assertTrue(atom.residue is not None)
        self.assertTrue(atom_copy.residue is None)

    def test_shallow_copy_residue(self):
        struc = next(self.complex.residues)
        field_list = self.residue_fields
        struc_copy = struc._shallow_copy()
        # Assert copy is a different object in memory
        self.assertTrue(struc_copy is not struc)
        self.validate_fields(struc, struc_copy, field_list)
        # Validate no atoms or bonds copied
        self.assertTrue(len(list(struc.atoms)) > 0)
        self.assertTrue(len(list(struc_copy.atoms)) == 0)
        self.assertTrue(len(list(struc.bonds)) > 0)
        self.assertTrue(len(list(struc_copy.bonds)) == 0)

    def test_shallow_copy_bonds(self):
        struc = next(self.complex.bonds)
        field_list = self.bond_fields
        struc_copy = struc._shallow_copy()
        self.assertTrue(struc_copy is not struc)
        self.validate_fields(struc, struc_copy, field_list)

    def test_shallow_copy_chain(self):
        struc = next(self.complex.chains)
        field_list = self.chain_fields
        struc_copy = struc._shallow_copy()
        self.assertTrue(struc_copy is not struc)
        self.validate_fields(struc, struc_copy, field_list)
        # Validate no residues copied
        self.assertTrue(len(list(struc.residues)) > 0)
        self.assertTrue(len(list(struc_copy.residues)) == 0)

    def test_shallow_copy_molecule(self):
        struc = next(self.complex.molecules)
        field_list = self.molecule_fields
        struc_copy = struc._shallow_copy()
        self.assertTrue(struc_copy is not struc)
        self.validate_fields(struc, struc_copy, field_list)
        # Validate no chains copied
        self.assertTrue(len(list(struc.chains)) > 0)
        self.assertTrue(len(list(struc_copy.chains)) == 0)

    def test_shallow_copy_complex(self):
        struc = self.complex
        field_list = self.complex_fields
        struc_copy = struc._shallow_copy()
        self.assertTrue(struc_copy is not struc)
        self.validate_fields(struc, struc_copy, field_list)
        # Validate no molecules copied
        self.assertTrue(len(list(struc_copy.molecules)) == 0)

    def test_deep_copy_complex(self):
        comp = self.complex
        comp_copy = comp._deep_copy()
        self.validate_deep_copy(comp, comp_copy)

    def test_deep_copy_conformer_complex(self):
        """Validate deep copy of complex that has multiple conformations."""
        pdb_path = os.path.join(test_assets, 'sdf', 'Thrombin_100cmpds (1).sdf')
        comp = struct.Complex.io.from_sdf(path=pdb_path)
        # Add a random bond to test with.
        atom1 = next(comp.atoms)
        atom2 = next(comp.atoms)
        residue = next(comp.residues)
        bond = struct.Bond()
        bond.atom1 = atom1
        bond.atom2 = atom2
        bond.kind = util.enums.Kind.CovalentSingle
        residue.add_bond(bond)
        comp_copy = comp._deep_copy()
        self.validate_deep_copy(comp, comp_copy)

    def validate_fields(self, struct_orig, struct_copy, field_list):
        for field in field_list:
            orig_val = getattr(struct_orig, field)
            copy_val = getattr(struct_copy, field)
            # Skip struct classes, because they will not be equal (different memory)
            if isinstance(orig_val, struct.Base) or isinstance(orig_val, types.GeneratorType):
                continue
            elif isinstance(orig_val, util.Color):
                self.assertEqual(orig_val.rgba, copy_val.rgba)
            elif isinstance(orig_val, util.Vector3):
                self.assertEqual(orig_val.unpack(), copy_val.unpack())
            elif isinstance(orig_val, util.Quaternion):
                self.assertEqual(str(orig_val), str(copy_val))
            else:
                # Assert copy has the same values as the original
                err_msg = "{field}: {orig_val} != {copy_val}".format(
                    field=field, orig_val=orig_val, copy_val=copy_val)
                self.assertTrue(orig_val == copy_val, err_msg)

    def validate_deep_copy(self, comp_original, comp_copy):
        """Traverse Complex data and make sure all fields were copied."""
        # Validate Complex fields
        self.assertTrue(comp_copy is not comp_original)
        self.validate_fields(comp_original, comp_copy, self.complex_fields)
        for mol, mol_copy in zip(comp_original.molecules, comp_copy.molecules):
            self.assertTrue(mol is not mol_copy)
            self.validate_fields(mol, mol_copy, self.molecule_fields)
            # Validate chains copied
            self.assertTrue(sum(1 for _ in mol.chains) == sum(1 for _ in mol_copy.chains))
            for chain, chain_copy in zip(mol.chains, mol_copy.chains):
                self.assertTrue(chain is not chain_copy)
                self.validate_fields(chain, chain_copy, self.chain_fields)
                # Validate residues copied
                self.assertEqual(sum(1 for _ in chain.residues), sum(1 for _ in chain_copy.residues))
                for residue, residue_copy in zip(chain.residues, chain_copy.residues):
                    self.assertTrue(residue is not residue_copy)
                    self.validate_fields(residue, residue_copy, self.residue_fields)
                    self.assertTrue(sum(1 for _ in residue.atoms) > 0)
                    # Validate atoms copied
                    self.assertEqual(sum(1 for _ in residue.atoms), sum(1 for _ in residue_copy.atoms))
                    for atom, atom_copy in zip(residue.atoms, residue_copy.atoms):
                        self.assertTrue(atom is not atom_copy)
                        self.validate_fields(atom, atom_copy, self.atom_fields)
                    # Validate bonds copied
                    self.assertEqual(sum(1 for _ in residue.bonds), sum(1 for _ in residue_copy.bonds))
                    for bond, bond_copy in zip(residue.bonds, residue_copy.bonds):
                        self.assertTrue(bond is not bond_copy)
                        self.validate_fields(bond, bond_copy, self.bond_fields)
