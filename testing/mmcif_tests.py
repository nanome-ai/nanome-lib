import nanome
import os
import re
import math

from nanome.util import Color
from nanome.util import Vector3
from nanome.util import Quaternion

from nanome.api import structure as struct
from nanome._internal._structure import _serialization as _seri
from nanome._internal._network._serialization._context import _ContextDeserialization, _ContextSerialization
from nanome._internal._network._commands._serialization import _UpdateWorkspace, _ReceiveWorkspace
from testing.utilities import *

from nanome.util import Logs

import tkinter as tk

test_assets = os.getcwd() + ("\\testing\\test_assets")
test_output_dir = os.getcwd() + ("\\testing\\test_outputs")
options = TestOptions(ignore_vars=["_serial", "_remarks", "_associated"])


def run(counter):
    run_test(test_1fsv, counter)
    run_test(test_tebgit, counter)
    # run_test(test_1fsv, counter)
    # run_test(test_1fsv, counter)
    # run_test(test_1fsv, counter)


# Testing save load
# MMCIF
def test_1fsv():
    input_dir = test_assets + ("\\mmcif\\1fsv.cif")
    output_dir = test_output_dir + ("\\testOutput.cif")

    complex1 = struct.Complex.io.from_mmcif(input_dir)
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

    complex2 = struct.Complex.io.from_mmcif(output_dir)

    compare_atom_positions(complex1, complex2)
    assert_equal(complex1, complex2, options)
    assert_not_equal(complex2, struct.Complex(), options)

#weird cif from CCDC
def test_tebgit():
    input_dir = test_assets + ("\\mmcif\\tebgit.cif")
    output_dir = test_output_dir + ("\\testOutput.cif")

    complex1 = struct.Complex.io.from_mmcif(input_dir)
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

    complex2 = struct.Complex.io.from_mmcif(output_dir)

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
    for m in range(len(complex1.molecules)):
        molecule1 = complex1.molecules[m]
        molecule2 = complex2.molecules[m]
        for c in range(len(molecule1.chains)):
            chain1 = molecule1.chains[c]
            chain2 = molecule2.chains[c]
            for r in range(len(chain1.residues)):
                residue1 = chain1.residues[r]
                residue2 = chain2.residues[r]
                for a in range(len(residue1.atoms)):
                    atom1 = residue1.atoms[a]
                    atom2 = residue2.atoms[a]
                    difference = atom1.molecular.position.x - atom2.molecular.position.x
                    assert(difference <.001)
                    assert(difference > -.001)
                    options2 = TestOptions(ignore_vars=["_serial", "_remarks", "_associated", "_position"])
                    assert_equal(atom1, atom2, options2)
