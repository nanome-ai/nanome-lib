import nanome
import os
import re
import math
import random

from nanome.util import Color
from nanome.util import Vector3
from nanome.util import Quaternion
from nanome.util import Matrix

from nanome.api import structure as struct
from nanome._internal._structure import _serialization as _seri
from nanome._internal._network._serialization._context import _ContextDeserialization, _ContextSerialization
from nanome._internal._network._commands._serialization import _UpdateWorkspace, _ReceiveWorkspace
from testing.utilities import *

from nanome.util import Logs

test_assets = os.getcwd() + ("/testing/test_assets")
test_output_dir = os.getcwd() + ("/testing/test_outputs")
options = TestOptions(ignore_vars=["_unique_identifier", "_remarks", "_associated", "_index"])

def run(counter):
    run_test(test_shallow, counter)
    run_test(test_deep, counter)

#testing structures
def test_shallow():
    shallow_copy_tester(struct.Atom)
    shallow_copy_tester(struct.Bond)
    shallow_copy_tester(struct.Residue)
    shallow_copy_tester(struct.Chain)
    shallow_copy_tester(struct.Molecule)
    shallow_copy_tester(struct.Complex)

def shallow_copy_tester(constructor):
    original = constructor()
    alter_object(original)
    copy = original._shallow_copy()
    assert_equal(original, copy, options)

def test_deep():
    deep_copy_tester(2)
    deep_copy_tester(3)
    deep_copy_tester(4)
    deep_copy_tester(5)

def deep_copy_tester(height):
    original = create_full_tree(height)
    alter_object(original)
    copy = original._deep_copy()
    assert_equal(original, copy, options)

def create_full_tree(height):
    if height == 1:
        return alter_object(struct.Atom())
    if height == 2:
        residue = struct.Residue()
        for _ in range(3):
            residue.add_atom(create_full_tree(height-1))
        bond_atoms(residue._atoms[0], residue._atoms[1])
        bond_atoms(residue._atoms[1], residue._atoms[2])
        return alter_object(residue)
    if height == 3:
        chain = struct.Chain()
        for _ in range(3):
            chain.add_residue(create_full_tree(height-1))
        bond_atoms(chain._residues[0]._atoms[0], chain._residues[1]._atoms[1])
        bond_atoms(chain._residues[0]._atoms[1], chain._residues[1]._atoms[2])
        return alter_object(chain)
    if height == 4:
        molecule = struct.Molecule()
        for _ in range(3):
            molecule.add_chain(create_full_tree(height-1))
        bond_atoms(molecule._chains[0]._residues[0]._atoms[0], molecule._chains[1]._residues[1]._atoms[1])
        bond_atoms(molecule._chains[0]._residues[0]._atoms[1], molecule._chains[1]._residues[1]._atoms[2])
        return alter_object(molecule)
    if height == 5:
        complex = struct.Complex()
        for _ in range(3):
            complex.add_molecule(create_full_tree(height-1))
        return alter_object(complex)

def bond_atoms(atom1, atom2):
    bond = struct.Bond()
    bond.atom1 = atom1
    bond.atom2 = atom2
    atom1.residue._add_atom(bond)
    return alter_object(bond)

