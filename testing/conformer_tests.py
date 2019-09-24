import nanome
import os

from nanome.api import structure as struct
from nanome._internal._structure._io import _conformer_helper as conformer
from testing.utilities import *

from nanome.util import Logs

test_assets = os.getcwd() + ("/testing/test_assets")
test_output_dir = os.getcwd() + ("/testing/test_outputs")
options = TestOptions(ignore_vars=["_unique_identifier"])

alter_object = lambda x: x

def run(counter):
    conformer.s_ConformersAlways = True
    run_test(test_to_conformer, counter)
    run_test(test_wholistic, counter)

def test_wholistic():
    original = create_full_tree(5)
    alter_object(original)
    copy = conformer.convert_to_conformers(original)
    copy = conformer.convert_to_frames(copy)
    assert_equal(original, copy, options)

def test_to_conformer():
    molecule_count = 5
    original = alter_object(struct.Complex())
    for molecule in create_frames(molecule_count):
        original.add_molecule(molecule)

    # for i in original.molecules:
    #     print(i.name)
    # for i in original.chains:
    #     print(i.name)
    # for i in original.residues:
    #     print(i.name)
    # # for i in original.bonds:
    # #     print(i.name)
    # for i in original.atoms:
    #     print(i.name)
    mc1,cc1,rc1,bc1,ac1 = count_structures(original)
    conformer_copy = conformer.convert_to_conformers(original)
    mc2,cc2,rc2,bc2,ac2 = count_structures(conformer_copy)
    #check the numbers
    assert(mc2 == 1)
    for molecule in conformer_copy.molecules:
        assert(molecule._conformer_count == mc1)
        assert(len(molecule._names) == mc1)
        assert(len(molecule._associateds) == mc1)
    assert (cc2 == cc1/mc1)
    assert (rc2 == rc1/mc1)
    assert (bc2 == bc1/mc1)
    for bond in conformer_copy.bonds:
        assert(bond._conformer_count == mc1)
        assert(len(bond._kinds) == mc1)
        assert(len(bond._exists) == mc1)

    assert (ac2 == ac1/mc1)
    for atom in conformer_copy.atoms:
        assert(atom._conformer_count == mc1)
        assert(len(atom._positions) == mc1)
        assert(len(atom._exists) == mc1)

    #check the values
    k = 0
    first_molecule = next(conformer_copy.molecules)
    for molecule, conf in zip(original.molecules, range(first_molecule._conformer_count)):
        k += 1
        molecule._name = first_molecule._names[conf]
        for atom1, atom2 in zip(molecule.atoms, first_molecule.atoms):
            assert(atom1._position == atom2._positions[conf])
            assert(atom1._exists[0] == atom2._exists[conf])
        for bond1, bond2 in zip(molecule.bonds, first_molecule.bonds):
            assert(bond1._kind == bond2._kinds[conf])
            assert(bond1._exists[0] == bond2._exists[conf])
    assert (k==molecule_count)

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
    Logs.debug("molecule_counter:",molecule_counter)
    Logs.debug("chain_counter:",chain_counter)
    Logs.debug("residue_counter:",residue_counter)
    Logs.debug("bond_counter:",bond_counter)
    Logs.debug("atom_counter:",atom_counter)