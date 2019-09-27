import nanome
import os

from nanome.api import structure as struct
from nanome._internal._structure._helpers import _conformer_helper as conformer
from testing.utilities import *

from nanome.util import Logs

test_assets = os.getcwd() + ("/testing/test_assets")
test_output_dir = os.getcwd() + ("/testing/test_outputs")
options = TestOptions(ignore_vars=["_unique_identifier", "_serial", "_index"])
conformer_blind = TestOptions(ignore_vars = ["_Molecule__conformer_count", "_positions", "_molecules", "_kinds", "_in_conformer", "_names", "_associateds", "_unique_identifier", "_serial", "_index"])

alter_object = lambda x: x

def run(counter):
    conformer.s_ConformersAlways = True
    run_test(test_to_conformer, counter)
    run_test(test_wholistic, counter)


def get_bond_hash(bond): #StringBuilder, Data.Bond, int, int -> int
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
        atom._bonds.sort(key = lambda x: x._atom1._unique_identifier<<32 + x._atom2._unique_identifier)

def unique_names(complex):
    molecule_count = 0
    for molecule in complex.molecules:
        molecule.name = "m" + str(molecule_count)
        molecule_count+=1
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
                    atom_count +=1

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

def test_wholistic():
    original = create_mixed_tree()
    unique_names(original)
    conf = conformer.convert_to_conformers(original)
    copy = conformer.convert_to_frames(conf)
    sort_bonds(original)
    sort_bonds(copy)

    assert_equal(original, copy, options)
    total_bonds1 = 0
    total_bonds2 = 0

    for res1, res2 in zip(original.residues, copy.residues):
        assert_equal(res1, res2, options)
        total_bonds1+=len(res1._bonds)
        total_bonds2+=len(res2._bonds)
        assert_equal(res1._bonds, res2._bonds, options)
        for bond1, bond2 in zip(res1.bonds, res2.bonds):
            assert_equal(bond1, bond2, options)
            assert_equal(bond1._parent, res1)
            assert_equal(bond2._parent, res2)
    for bond1, bond2 in zip(original.bonds, copy.bonds):
        assert_equal(bond1, bond2, options)
        assert_equal(bond1._parent, bond2._parent, options)

def test_to_conformer():
    molecule_count = 5
    original = create_conformer_tree(molecule_count)
    unique_names(original)
    mc1,cc1,rc1,bc1,ac1 = count_structures(original)
    conformer_copy = conformer.convert_to_conformers(original)
    mc2,cc2,rc2,bc2,ac2 = count_structures(conformer_copy)
    sort_bonds(original)
    sort_bonds(conformer_copy)

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
        assert(len(bond._in_conformer) == mc1)

    assert (ac2 == ac1/mc1)
    for atom in conformer_copy.atoms:
        assert(atom._conformer_count == mc1)
        assert(len(atom._positions) == mc1)
        assert(len(atom._in_conformer) == mc1)

    #check the values
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