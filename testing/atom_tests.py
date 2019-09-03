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
options = TestOptions(ignore_vars=["_unique_identifier", "_remarks", "_associated"])

def run(counter):
    run_test(test_structures, counter)
    run_test(test_equality, counter)
    run_test(test_pdb, counter)
    run_test(test_iterators, counter)
    run_test(test_matrices, counter)
    prep_timer_test()
    run_timed_test(time_test_serializer, counter, 1, 10)#normally 2.9 

def test_equality():
    assert_equal(create_atom(), create_atom(), options)
    assert_equal(create_bond(), create_bond(), options)
    assert_equal(create_residue(), create_residue(), options)
    assert_equal(create_chain(), create_chain(), options)
    assert_equal(create_molecule(), create_molecule(), options)
    assert_equal(create_complex(), create_complex(), options)
    assert_equal(create_workspace(), create_workspace(), options)

    assert_not_equal(create_atom(), struct.Atom(), options)
    assert_not_equal(create_bond(), struct.Bond(), options)
    assert_not_equal(create_residue(), struct.Residue(), options)
    assert_not_equal(create_chain(), struct.Chain(), options)
    assert_not_equal(create_molecule(), struct.Molecule(), options)
    assert_not_equal(create_complex(), struct.Complex(), options)
    assert_not_equal(create_workspace(), struct.Workspace(), options)

#testing structures
def test_structures():
    create_atom()
    create_bond()
    create_residue()
    create_chain()
    create_molecule()

def flip_x_positions(complex):
    for molecule in complex.molecules:
        for chain in molecule.chains:
            for residue in chain.residues:
                for atom in residue.atoms:
                    atom.position.x = -atom.position.x
    return complex

def compare_atom_positions(complex1, complex2):
    a1 = complex1.atoms
    a2 = complex2.atoms
    for a,_ in enumerate(complex1.atoms):
        atom1 = next(a1)
        atom2 = next(a2)
        assert_equal(atom1.position.x, atom2.position.x, options)
        assert_equal(atom1, atom2, options)

#Testing save load
#PDB
def test_pdb():
    input_dir = test_assets + ("/pdb/1fsv.pdb")
    output_dir = test_output_dir + ("/testOutput.pdb")

    complex1 = struct.Complex.io.from_pdb(path=input_dir)
    complex1.io.to_pdb(output_dir)

    complex2 = struct.Complex.io.from_pdb(path=input_dir)

    compare_atom_positions(complex1, complex2)
    assert_equal(complex1, complex2, options)
    assert_not_equal(complex2, struct.Complex(), options)

#testing serializers
test_workspace = None
def prep_timer_test():
    #input_dir = test_assets + ("/sdf/Structure3D_CID_243.sdf") #withbonds
    input_dir = test_assets + ("/sdf/Thrombin_100cmpds (1).sdf") #withbonds
    #input_dir = test_assets + ("/pdb/1fsv.pdb") #smallboy
    #input_dir = test_assets + ("/pdb/1a9l.pdb") #bigboy
    complex1 = struct.Complex.io.from_sdf(path=input_dir)
    complex2 = struct.Complex.io.from_sdf(path=input_dir)
    complex3 = struct.Complex.io.from_sdf(path=input_dir)
    complex4 = struct.Complex.io.from_sdf(path=input_dir)
    global test_workspace
    test_workspace = create_workspace()
    test_workspace.complexes = [complex1, complex2, complex3, complex4]

def count_structures(complex):
    molecule_counter = 0
    chain_counter = 0
    residue_counter = 0
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
                    bond_counter +=1
    print("molecule_counter:",molecule_counter)
    print("chain_counter:",chain_counter)
    print("residue_counter:",residue_counter)
    print("residue_counter:",residue_counter)
    print("bond_counter:",bond_counter)
    print("atom_counter:",atom_counter)

def time_test_serializer():
    #create test data
    workspace1 = test_workspace
    #create serializers
    update_workspace = _UpdateWorkspace()
    receive_workspace = _ReceiveWorkspace()

    context_s = _ContextSerialization(plugin_id=random.randint(0, 0xFFFFFFFF))
    update_workspace.serialize(update_workspace.version, workspace1, context_s)

    #deserialize stuff
    context_d = _ContextDeserialization(context_s.to_array())
    workspace2 = receive_workspace.deserialize(update_workspace.version, context_d)

def test_serializers():
    #create test data
    #create test data
    workspace1 = create_workspace()
    #create serializers
    update_workspace = _UpdateWorkspace()
    receive_workspace = _ReceiveWorkspace()

    context_s = _ContextSerialization(plugin_id=random.randint(0, 0xFFFFFFFF))
    update_workspace.serialize(workspace1, context_s)

    #deserialize stuff
    context_d = _ContextDeserialization(context_s.to_array())
    workspace2 = receive_workspace.deserialize(context_d)
    assert_equal(workspace1, workspace2, options)
    
def test_iterators():
    input_dir = test_assets + ("/sdf/Thrombin_100cmpds (1).sdf")
    output_dir = test_output_dir + ("/testOutput.sdf")

    #complex level
    complex = struct.Complex.io.from_sdf(path=input_dir)
    a = 0
    for atom in complex.atoms:
        a += 1
    assert(a==5721)
    a = 0
    for residue in complex.residues:
        for atom in residue.atoms:
            a +=1
    assert(a==5721)
    a=0
    for chain in complex.chains:
        for atom in chain.atoms:
            a+=1
    assert(a==5721)
    a = 0
    for molecule in complex.molecules:
        for atom in molecule.atoms:
            a+=1
    assert(a==5721)
    a = 0
    #gets first molecule
    molecule = next(complex.molecules)
    for residue in molecule.residues:
        for atom in residue.atoms:
            a+=1
    assert(a==76)
    a=0
    for chain in molecule.chains:
        for atom in chain.atoms:
            a+=1
    assert(a==76)
    a=0
    for residue in molecule.residues:
        for atom in residue.atoms:
            a+=1
    assert(a==76)
    a=0
    chain = next(molecule.chains)
    for residue in chain.residues:
        for atom in residue.atoms:
            a+=1
    assert(a==76)
    b=False
    for residue in chain.residues:
        for _ in residue.bonds:
            b=True
    assert(b)

def create_atom():
    val = struct.Atom()
    val.index = 1000
    val.selected = True
    val.atom_mode = 1  # BALLSTICK
    val.labeled = True
    val.atom_rendering = True
    val.atom_color = Color.White()
    val.surface_rendering = True
    val.surface_color = Color.White()
    val.surface_opacity = 1
    val.symbol = "Carbon"
    val.serial = 0
    val.name = "default"
    val.position = Vector3()
    return val

def create_bond():
    val = struct.Bond()
    val.index = 1000
    val.atom1 = create_atom()
    val.atom2 = create_atom()
    val.kind = struct.Bond.Kind.CovalentDouble
    return val

def create_residue():
    val = struct.Residue()
    val.index = 1000
    val._atoms = [struct.Atom(), create_atom(), struct.Atom(), create_atom()]
    val._bonds = [create_bond(), create_bond(), create_bond(), create_bond()]
    val.ribboned = True
    val.ribbon_size = 1
    val.ribbon_mode = struct.Residue.RibbonMode.Coil 
    val.ribbon_color = Color.White() 
    val.type = "asdf" #RESIDUEDATA
    val.serial = 1
    val.name = "asdf1234"
    val.secondary_structure = struct.Residue.SecondaryStructure.Sheet
    return val

def create_chain():
    val = struct.Chain()
    val.index = 1000
    val._residues = [struct.Residue(), create_residue(), struct.Residue(), create_residue()]
    val.name = "fdasa1234"
    return val

def create_molecule():
    val = struct.Molecule()
    val.index = 1000
    val._chains = [struct.Chain(), create_chain(), struct.Chain(), create_chain()]
    val.name = "MIOLECASDFULE"
    val._associated = dict([("key1", "val1"), ("key2","val2"),("key3", "val3"), ("key4","val4")])
    return val

def create_complex():
    val = struct.Complex()
    val.index = 1000
    val._molecules = [struct.Molecule(), create_molecule(), struct.Molecule(), create_molecule()]
    val.boxed = True
    val.visible = False
    val.computing = False
    val.current_frame = 0
    val.name = "COMPLEX_NAME"
    val._remarks = dict([("key1", "val1"), ("key2","val2"),("key3", "val3"), ("key4","val4")])
    val.position = Vector3(1,2,3)
    val.rotation = Quaternion(1,2,3,4)
    return val

def create_workspace():
    workspace = struct.Workspace()
    workspace.complexes = [struct.Complex(), create_complex(), struct.Complex(), create_complex()]
    workspace.position = Vector3(1,2,3)
    workspace.rotation = Quaternion(1,2,3,4)
    return workspace

def test_matrices():
    a = Matrix(3, 4)
    b = Matrix(4, 3)
    v = Matrix(4, 1)
    v[0][0] = 12.5
    v[1][0] = 9.36
    v[2][0] = 24.1
    v[3][0] = 1.0
    result_mul = Matrix(3, 3)
    result_mul[0] = [42, 48, 54]
    result_mul[1] = [114, 136, 158]
    result_mul[2] = [186, 224, 262]
    result_mul_v = Matrix(3, 1)
    result_mul_v[0][0] = 60.56
    result_mul_v[1][0] = 248.4
    result_mul_v[2][0] = 436.24

    for i in range(12):
        a[int(i / 4)][int(i % 4)] = i
        b[int(i / 3)][int(i % 3)] = i

    assert_equal(a * b, result_mul)
    assert_equal(a * v, result_mul_v)

    res_atom_global_pos = Vector3(-20.33947, 0.1491127, -9.878754)
    complex = struct.Complex()
    atom = struct.Atom()
    atom.position.set(7.2, 2.6, -21.56)
    complex.position.set(-3.197371, -2.314157, 5.071643)
    complex.rotation.set(0.09196287, 0.4834483, 0.3486853, 0.797646)
    m = complex.get_complex_to_workspace_matrix()
    m_inv = complex.get_workspace_to_complex_matrix()
    atom_global_pos = m * atom.position

    assert_equal(atom_global_pos, res_atom_global_pos)
    assert_equal(m_inv * atom_global_pos, atom.position)