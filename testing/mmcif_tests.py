import nanome
import os
from testing import utilities as util

from nanome.api import structure as struct
from nanome._internal._structure import _serialization as _seri
from testing.utilities import *

from nanome.util import Logs

test_assets = os.getcwd() + ("/testing/test_assets")
test_output_dir = os.getcwd() + ("/testing/test_outputs")
options = TestOptions(ignore_vars=["_serial", "_unique_identifier", "_remarks", "_associated", "_position"])


def run(counter):
    run_test(test_1fsv, counter)
    run_test(test_tebgit, counter)
    # run_test(test_1fsv, counter)
    # run_test(test_1fsv, counter)
    # run_test(test_1fsv, counter)


# Testing save load
# MMCIF
def test_1fsv():
    input_dir = test_assets + ("/mmcif/1fsv.cif")
    output_dir = test_output_dir + ("/testOutput.cif")

    complex1 = struct.Complex.io.from_mmcif(path=input_dir)
    complex1.io.to_mmcif(output_dir)

    #fact checks
    counters = count_structures(complex1)
    (molecule_count, chain_count, residue_count, bond_count, atom_count) = counters
    assert(molecule_count == 1)
    assert(chain_count == 1)
    assert(residue_count == 28)
    assert(bond_count == 0)
    assert(atom_count == 504)
    #

    complex2 = struct.Complex.io.from_mmcif(path=output_dir)

    compare_atom_positions(complex1, complex2)
    assert_equal(complex1, complex2, options)
    assert_not_equal(complex2, struct.Complex(), options)

#weird cif from CCDC
def test_tebgit():
    input_dir = test_assets + ("/mmcif/tebgit.cif")
    output_dir = test_output_dir + ("/testOutput.cif")

    complex1 = struct.Complex.io.from_mmcif(path=input_dir)
    #fact checks
    counters = count_structures(complex1)
    (molecule_count, chain_count, residue_count, bond_count, atom_count) = counters
    assert(molecule_count == 1)
    assert(chain_count == 1)
    assert(residue_count == 1)
    assert(bond_count == 0)
    assert(atom_count == 28)
    #

    complex1.io.to_mmcif(output_dir)

    complex2 = struct.Complex.io.from_mmcif(path=output_dir)

    compare_atom_positions(complex1, complex2)
    assert_equal(complex1, complex2, options)
    assert_not_equal(complex2, struct.Complex(), options)

def count_structures(complex):
    molecule_counter = 0
    chain_counter = 0
    residue_counter = 0
    bond_counter = 0
    atom_counter = 0
    for molecule in complex.molecules:
        molecule_counter += 1
        for chain in molecule.chains:
            chain_counter += 1
            for residue in chain.residues:
                residue_counter += 1
                for atom in residue.atoms:
                    atom_counter += 1
                for bond in residue.bonds:
                    bond_counter += 1
    return molecule_counter, chain_counter, residue_counter, bond_counter, atom_counter
    Logs.debug("molecule_counter:", molecule_counter)
    Logs.debug("chain_counter:", chain_counter)
    Logs.debug("residue_counter:", residue_counter)
    Logs.debug("bond_counter:", bond_counter)
    Logs.debug("atom_counter:", atom_counter)

def compare_atom_positions(complex1, complex2):
    a1 = complex1.atoms
    a2 = complex2.atoms
    for a,_ in enumerate(complex1.atoms):
        atom1 = next(a1)
        atom2 = next(a2)
        difference = atom1.position.x - atom2.position.x
        assert(difference <.001)
        assert(difference > -.001)
        assert_equal(atom1, atom2, options)
