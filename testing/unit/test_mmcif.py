import os
import tempfile
import unittest

from nanome.api import structure as struct
from testing.unit.utilities import assert_equal, assert_not_equal, TestOptions


test_assets = os.getcwd() + ("/testing/test_assets")
test_output_dir = os.getcwd() + ("/testing/test_outputs")
options = TestOptions(ignore_vars=["_serial", "_unique_identifier", "_remarks", "_associateds", "_positions", "_alt_loc"])


def count_structures(complex):
    molecule_counter = sum(1 for i in complex.molecules)
    chain_counter = sum(1 for i in complex.chains)
    residue_counter = sum(1 for i in complex.residues)
    bond_counter = sum(1 for i in complex.bonds)
    atom_counter = sum(1 for i in complex.atoms)
    return molecule_counter, chain_counter, residue_counter, bond_counter, atom_counter


def compare_atom_positions(complex1, complex2):
    a1 = complex1.atoms
    a2 = complex2.atoms
    for a, _ in enumerate(complex1.atoms):
        atom1 = next(a1)
        atom2 = next(a2)
        difference = atom1.position.x - atom2.position.x
        assert(difference < .001)
        assert(difference > -.001)


class MmcifTestCase(unittest.TestCase):
    # Testing save load
    # MMCIF
    def test_1fsv(self):
        input_dir = test_assets + ("/mmcif/1fsv.cif")
        output_cif = tempfile.NamedTemporaryFile(suffix='.cif').name

        complex1 = struct.Complex.io.from_mmcif(path=input_dir)
        complex1.io.to_mmcif(output_cif)

        # fact checks
        counters = count_structures(complex1)
        (molecule_count, chain_count, residue_count, bond_count, atom_count) = counters
        assert(molecule_count == 1)
        assert(chain_count == 1)
        assert(residue_count == 28)
        assert(bond_count == 0)
        assert(atom_count == 504)

        complex2 = struct.Complex.io.from_mmcif(path=output_cif)
        compare_atom_positions(complex1, complex2)
        assert_equal(complex1, complex2, options)
        assert_not_equal(complex2, struct.Complex(), options)

    # weird cif from CCDC
    def test_tebgit(self):
        input_dir = test_assets + ("/mmcif/tebgit.cif")
        output_cif = tempfile.NamedTemporaryFile(suffix='.cif').name

        complex1 = struct.Complex.io.from_mmcif(path=input_dir)
        # fact checks
        counters = count_structures(complex1)
        (molecule_count, chain_count, residue_count, bond_count, atom_count) = counters
        assert(molecule_count == 1)
        assert(chain_count == 1)
        assert(residue_count == 1)
        assert(bond_count == 0)
        assert(atom_count == 28)
        complex1.io.to_mmcif(output_cif)

        complex2 = struct.Complex.io.from_mmcif(path=output_cif)

        compare_atom_positions(complex1, complex2)
        assert_equal(complex1, complex2, options)
        assert_not_equal(complex2, struct.Complex(), options)
