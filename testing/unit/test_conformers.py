import nanome
import os

from nanome.api import structure as struct
from nanome._internal._structure._helpers import _conformer_helper as conformer
from testing.unit.utilities import TestOptions, create_full_tree, assert_equal
import unittest
from nanome.util import Logs, Vector3

test_assets = os.getcwd() + ("/testing/test_assets")
options = TestOptions(ignore_vars=["_unique_identifier", "_serial", "_index", "_alt_loc"])
conformer_blind = TestOptions(ignore_vars=["_Molecule__conformer_count", "_positions", "_molecules", "_kinds", "_in_conformer", "_names", "_associateds", "_unique_identifier", "_serial", "_index", "_alt_loc"])


def alter_object(x):
    return x


def get_bond_hash(bond):  # StringBuilder, Data.Bond, int, int -> int
    line = ""
    line += (bond._atom1.name)
    line += (":")
    line += (bond._atom2.name)
    line += (":")
    line += str(bond._residue._serial)
    line += (":")
    line += str(bond._residue._name)
    line += (":")
    line += str(bond._chain._name)
    return (line)


def sort_bonds(complex):
    for atom in complex.atoms:
        atom._bonds.sort(key=lambda x: x._atom1._unique_identifier << 32 + x._atom2._unique_identifier)


def unique_names(complex):
    molecule_count = 0
    for molecule in complex.molecules:
        molecule.name = "m" + str(molecule_count)
        molecule_count += 1
        chain_count = 0
        for chain in molecule.chains:
            chain.name = "c" + str(chain_count)
            chain_count += 1
            res_count = 0
            for residue in chain.residues:
                residue.name = "r" + str(res_count) + chain.name
                res_count += 1
                atom_count = 0
                for atom in residue.atoms:
                    atom.name = "a" + str(atom_count) + residue.name
                    atom_count += 1


def create_conformer_tree(molecule_count):
    complex = alter_object(struct.Complex())
    for molecule in create_frames(molecule_count):
        complex.add_molecule(molecule)
    return complex


def create_mixed_tree():
    complex = create_full_tree(5)
    chain = create_full_tree(3)
    for residue1, residue2 in zip(complex.residues, chain.residues):
        for atom in residue2.atoms:
            residue1._add_atom(atom)
        for bond in residue2.bonds:
            residue1._add_bond(bond)
    return complex


def create_frames(num):
    molecules = []
    for i in range(num):
        molecules.append(create_full_tree(4))
    return molecules


def count_structures(complex):
    molecule_counter = sum(1 for i in complex.molecules)
    chain_counter = sum(1 for i in complex.chains)
    residue_counter = sum(1 for i in complex.residues)
    bond_counter = sum(1 for i in complex.bonds)
    atom_counter = sum(1 for i in complex.atoms)
    return molecule_counter, chain_counter, residue_counter, bond_counter, atom_counter
    Logs.debug("molecule_counter:", molecule_counter)
    Logs.debug("chain_counter:", chain_counter)
    Logs.debug("residue_counter:", residue_counter)
    Logs.debug("bond_counter:", bond_counter)
    Logs.debug("atom_counter:", atom_counter)


def deep_copy_tester(height):
    """This is required for Conformer Tests to work when run in isolation."""
    original = create_full_tree(height)
    alter_object(original)
    copy = original._deep_copy()
    assert_equal(original, copy, options)


class ConformerTestCase(unittest.TestCase):

    def test_conformer_api(self):
        # test molecule
        deep_copy_tester(4)

        test = create_frames(1)[0]
        # conformer_count
        molecule = test._deep_copy()
        atom = next(molecule.atoms)
        bond = next(molecule.bonds)
        molecule.set_current_conformer(1)
        assert(molecule.current_conformer == 1)
        assert(atom.current_conformer == 1)
        assert(bond.current_conformer == 1)
        assert(molecule.conformer_count == 1)
        assert(atom.conformer_count == 1)
        assert(bond.conformer_count == 1)
        molecule.set_conformer_count(2)
        assert(molecule.current_conformer == 1)
        assert(atom.current_conformer == 1)
        assert(bond.current_conformer == 1)
        assert(molecule.conformer_count == 2)
        assert(atom.conformer_count == 2)
        assert(bond.conformer_count == 2)
        molecule.set_conformer_count(1)
        assert(molecule.current_conformer == 0)
        assert(atom.current_conformer == 0)
        assert(bond.current_conformer == 0)
        assert(molecule.conformer_count == 1)
        assert(atom.conformer_count == 1)
        assert(bond.conformer_count == 1)

        # list_resizing
        molecule = test._deep_copy()
        atom = next(molecule.atoms)
        bond = next(molecule.bonds)
        molecule.set_conformer_count(2)
        assert(len(molecule.names) == 2)
        assert(len(molecule.associateds) == 2)
        assert(molecule.names[1] == molecule.names[0])
        assert(molecule.associateds[1] == molecule.associateds[0])
        assert(len(atom.positions) == 2)
        assert(len(atom.in_conformer) == 2)
        assert(atom.positions[1].equals(atom.positions[0]))
        assert(atom.in_conformer[1] == atom.in_conformer[0])
        assert(len(bond.kinds) == 2)
        assert(len(bond.in_conformer) == 2)
        assert(bond.kinds[1] == bond.kinds[0])
        assert(bond.in_conformer[1] == bond.in_conformer[0])

        # convenience functions
        reference = test._deep_copy()
        atom = next(reference.atoms)
        bond = next(reference.bonds)
        reference.set_conformer_count(3)
        atom.positions = [Vector3(0, 0, 0), Vector3(1, 1, 1), Vector3(2, 2, 2)]
        bond.kinds = [nanome.util.enums.Kind.CovalentSingle, nanome.util.enums.Kind.CovalentDouble, nanome.util.enums.Kind.CovalentTriple]

        molecule = reference._deep_copy()
        atom = next(molecule.atoms)
        molecule.create_conformer(1)
        assert(molecule.conformer_count == 4)
        assert(len(molecule.names) == 4)
        assert(len(atom.positions) == 4)
        assert(atom.positions[0] == atom.positions[1])
        assert(atom.positions[0] is not atom.positions[1])
        molecule.create_conformer(4)
        molecule.create_conformer(0)

        molecule = reference._deep_copy()
        bond = next(molecule.bonds)
        molecule.copy_conformer(2, 0)
        assert(molecule.conformer_count == 4)
        assert(len(molecule.names) == 4)
        assert(len(bond.kinds) == 4)
        assert(bond.kinds[0] == bond.kinds[3])
        molecule.copy_conformer(3)
        molecule.copy_conformer(0)

        molecule = reference._deep_copy()
        bond = next(molecule.bonds)
        atom = next(molecule.atoms)
        position = atom.positions[2]
        molecule.move_conformer(2, 0)
        assert(molecule.conformer_count == 3)
        assert(len(molecule.names) == 3)
        assert(len(atom.positions) == 3)
        assert(atom.positions[2] != position)
        assert(position == atom.positions[0])
        molecule.move_conformer(2, 2)
        molecule.move_conformer(0, 0)
        molecule.move_conformer(0, 3)

        molecule = reference._deep_copy()
        bond = next(molecule.bonds)
        atom = next(molecule.atoms)
        molecule.set_current_conformer(2)
        position = atom.positions[2]
        deleted = atom.positions[0]
        molecule.delete_conformer(0)
        assert(molecule.current_conformer == 1)
        assert(molecule.conformer_count == 2)
        assert(len(molecule.names) == 2)
        assert(len(atom.positions) == 2)
        assert(atom.positions[1] == position)
        assert(atom.positions[0] != deleted)
        molecule.delete_conformer(1)
        molecule.delete_conformer(0)

    def test_error_conditions(self):
        sample_kinds = [nanome.util.enums.Kind.CovalentSingle, nanome.util.enums.Kind.CovalentDouble, nanome.util.enums.Kind.CovalentTriple]
        sample_positions = [Vector3(0, 0, 0), Vector3(1, 1, 1), Vector3(2, 2, 2)]
        sample_exists = [True, False, True]
        molecule = create_frames(1)[0]
        atom = next(molecule.atoms)
        bond = next(molecule.bonds)
        failed = False
        try:
            atom.positions = sample_positions
        except ValueError:
            failed = True
        assert(failed)

        failed = False
        try:
            atom.in_conformer = sample_exists
        except ValueError:
            failed = True
        assert(failed)

        failed = False
        try:
            bond.in_conformer = sample_exists
        except ValueError:
            failed = True
        assert(failed)

        failed = False
        try:
            bond.kinds = sample_kinds
        except ValueError:
            failed = True
        assert(failed)

        failed = False
        try:
            molecule.associateds = [{}, {}, {}]
        except ValueError:
            failed = True
        assert(failed)

        failed = False
        try:
            molecule.names = ["", "", ""]
        except ValueError:
            failed = True
        assert(failed)

        new_atom = struct.Atom()
        new_atom.in_conformer = sample_exists
        failed = False
        try:
            next(molecule.residues).add_atom(new_atom)
        except ValueError:
            failed = True
        assert(failed)

        new_atom = struct.Atom()
        new_atom.positions = sample_positions
        failed = False
        try:
            next(molecule.residues).add_atom(new_atom)
        except ValueError:
            failed = True
        assert(failed)

        new_atom = struct.Atom()
        new_atom.in_conformer = sample_exists
        failed = False
        try:
            next(molecule.residues).add_atom(new_atom)
        except ValueError:
            failed = True
        assert(failed)

        new_bond = struct.Bond()
        new_bond.kinds = sample_kinds
        failed = False
        try:
            next(molecule.residues).add_bond(new_bond)
        except ValueError:
            failed = True
        assert(failed)

        new_bond = struct.Bond()
        new_bond.in_conformer = sample_exists
        failed = False
        try:
            next(molecule.residues).add_bond(new_bond)
        except ValueError:
            failed = True
        assert(failed)

    def test_wholistic(self):
        original = create_mixed_tree()
        unique_names(original)
        conf = conformer.convert_to_conformers(original, True)
        copy = conformer.convert_to_frames(conf)
        sort_bonds(original)
        sort_bonds(copy)
        assert_equal(original, copy, options)
        total_bonds1 = 0
        total_bonds2 = 0

        for res1, res2 in zip(original.residues, copy.residues):
            total_bonds1 += len(res1._bonds)
            total_bonds2 += len(res2._bonds)
        assert(total_bonds1 == total_bonds2)

    def test_to_conformer(self):
        molecule_count = 5
        original = create_conformer_tree(molecule_count)
        unique_names(original)
        mc1, cc1, rc1, bc1, ac1 = count_structures(original)
        conformer_copy = conformer.convert_to_conformers(original, True)
        mc2, cc2, rc2, bc2, ac2 = count_structures(conformer_copy)
        sort_bonds(original)
        sort_bonds(conformer_copy)

        # check the numbers
        assert(mc2 == 1)
        for molecule in conformer_copy.molecules:
            assert(molecule._conformer_count == mc1)
            assert(len(molecule._names) == mc1)
            assert(len(molecule._associateds) == mc1)
        assert (cc2 == cc1 / mc1)
        assert (rc2 == rc1 / mc1)
        assert (bc2 == bc1 / mc1)
        for bond in conformer_copy.bonds:
            assert(bond._conformer_count == mc1)
            assert(len(bond._kinds) == mc1)
            assert(len(bond._in_conformer) == mc1)

        assert (ac2 == ac1 / mc1)
        for atom in conformer_copy.atoms:
            assert(atom._conformer_count == mc1)
            assert(len(atom._positions) == mc1)
            assert(len(atom._in_conformer) == mc1)

        # check the values
        k = 0
        first_molecule = next(conformer_copy.molecules)
        for molecule, conf in zip(original.molecules, range(first_molecule._conformer_count)):
            k += 1
            molecule._name = first_molecule._names[conf]
            for atom1, atom2 in zip(molecule.atoms, first_molecule.atoms):
                assert_equal(atom1, atom2, conformer_blind)
                assert(atom1._position.equals(atom2._positions[conf]))
                assert(atom1._in_conformer[0] == atom2._in_conformer[conf])
            for bond1, bond2 in zip(molecule.bonds, first_molecule.bonds):
                assert(bond1._kind == bond2._kinds[conf])
                assert(bond1._in_conformer[0] == bond2._in_conformer[conf])
        assert (k == molecule_count)
