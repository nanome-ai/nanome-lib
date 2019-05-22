import nanome
import os
from testing import utilities as util

from nanome.api import structure as struct
from nanome._internal._structure import _serialization as _seri
from testing.utilities import *

from nanome.util import Logs

test_assets = os.getcwd() + ("/testing/test_assets")
test_output_dir = os.getcwd() + ("/testing/test_outputs")
options = TestOptions(ignore_vars=["_serial", "_remarks", "_associated"])


def run(counter):
    run_test(test_thrombin, counter)


# Testing save load
# MMCIF
def test_thrombin():
    input_dir = test_assets + ("/sdf/small_thrombin.sdf")
    output_dir = test_output_dir + ("/testOutput.sdf")

    complex1 = struct.Complex.io.from_sdf(input_dir)
    complex1.io.to_sdf(output_dir)

    #fact checks
    counters = count_structures(complex1)
    (molecule_count, chain_count, residue_count, bond_count, atom_count) = counters
    assert(molecule_count == 3)
    assert(chain_count == 3)
    assert(residue_count == 3)
    assert(bond_count == 237)
    assert(atom_count == 228)
    #

    complex2 = struct.Complex.io.from_sdf(output_dir)
    counters = count_structures(complex2)
    (molecule_count, chain_count, residue_count, bond_count, atom_count) = counters
    assert(molecule_count == 3)
    assert(chain_count == 3)
    assert(residue_count == 3)
    assert(bond_count == 237)
    assert(atom_count == 228)

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
        difference = atom1.molecular.position.x - atom2.molecular.position.x
        assert(difference <.001)
        assert(difference > -.001)
        options2 = TestOptions(ignore_vars=["_serial", "_remarks", "_associated", "_position"])
        assert_equal(atom1, atom2, options2)
