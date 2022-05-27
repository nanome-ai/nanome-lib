import nanome
import os

from nanome.api import structure as struct
from testing.unit.utilities import assert_equal, assert_not_equal, TestOptions

from nanome.util import Logs
import unittest
import tempfile

test_assets = os.getcwd() + ("/testing/test_assets")
test_output_dir = os.getcwd() + ("/testing/test_outputs")
options = TestOptions(ignore_vars=["_unique_identifier", "_remarks", "_associateds", "_alt_loc"])


i = 0


def read_write_read(filename):
    global i
    output_file = tempfile.NamedTemporaryFile(suffix='.sdf').name
    i += 1
    complex1 = struct.Complex.io.from_sdf(path=filename)
    complex1.io.to_sdf(output_file)
    complex2 = struct.Complex.io.from_sdf(path=output_file)

    compare_atom_positions(complex1, complex2)
    assert_equal(complex1, complex2, options)
    assert_not_equal(complex2, struct.Complex(), options)

    return complex1, complex2


def read_write_read_frames(filename):
    global i
    suffix = '_' + str(i) + '.sdf'
    output_file = tempfile.NamedTemporaryFile(suffix=suffix).name
    i += 1
    complex1 = struct.Complex.io.from_sdf(path=filename)
    complex1 = complex1.convert_to_frames()
    complex1.io.to_sdf(output_file)
    complex2 = struct.Complex.io.from_sdf(path=output_file)
    complex2 = complex2.convert_to_frames()

    compare_atom_positions(complex1, complex2)
    assert_equal(complex1, complex2, options)
    assert_not_equal(complex2, struct.Complex(), options)

    return complex1, complex2


def check_facts(complex, molecules, chains, residues, bonds, atoms):
    counters = count_structures(complex)
    (molecule_count, chain_count, residue_count, bond_count, atom_count) = counters
    assert(molecule_count == molecules)
    assert(chain_count == chains)
    assert(residue_count == residues)
    assert(bond_count == bonds)
    assert(atom_count == atoms)


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


def compare_atom_positions(complex1, complex2):
    a1 = complex1.atoms
    a2 = complex2.atoms
    for a, _ in enumerate(complex1.atoms):
        atom1 = next(a1)
        atom2 = next(a2)
        difference = atom1.position.x - atom2.position.x
        assert(difference < .001)
        assert(difference > -.001)


class SDFTestCase(unittest.TestCase):

    def test_aromatic(self):
        input_dir = test_assets + ("/sdf/aromatic.sdf")

        read_write_read(input_dir)
        complex1, complex2 = read_write_read_frames(input_dir)
        check_facts(complex1, 1, 1, 1, 34, 31)
        check_facts(complex2, 1, 1, 1, 34, 31)
        aromatic_bond = False
        for bond in complex2.bonds:
            if bond.kind == nanome.util.enums.Kind.Aromatic:
                aromatic_bond = True
        assert(aromatic_bond)

    def test_thrombin(self):
        input_dir = test_assets + ("/sdf/small_thrombin.sdf")

        read_write_read(input_dir)
        complex1, complex2 = read_write_read_frames(input_dir)

        check_facts(complex1, 3, 3, 3, 237, 228)
        check_facts(complex2, 3, 3, 3, 237, 228)

    def test_read_all_ways(self):
        input_dir = test_assets + ("/sdf/small_thrombin.sdf")
        # read path
        complex1 = struct.Complex.io.from_sdf(path=input_dir)
        with open(input_dir) as f:
            complex2 = struct.Complex.io.from_sdf(file=f)
        with open(input_dir) as f:
            as_string = f.read()
        with open(input_dir) as f:
            as_lines = f.readlines()
        complex3 = struct.Complex.io.from_sdf(string=as_string)
        complex4 = struct.Complex.io.from_sdf(lines=as_lines)
        assert(complex1 is not None)
        assert(complex2 is not None)
        assert(complex3 is not None)
        assert(complex4 is not None)
