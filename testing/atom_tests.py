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

test_assets = os.getcwd() + ("/testing/test_assets")
test_output_dir = os.getcwd() + ("/testing/test_outputs")
options = TestOptions(ignore_vars=["_serial", "_remarks", "_associated"])

def run(counter):
    run_test(test_structures, counter)
    run_test(test_equality, counter)
    run_test(test_pdb, counter)
    run_test(test_iterators, counter)
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
                    atom.molecular.position.x = -atom.molecular.position.x
    return complex

def compare_atom_positions(complex1, complex2):
    a1 = complex1.atoms
    a2 = complex2.atoms
    for a,_ in enumerate(complex1.atoms):
        atom1 = next(a1)
        atom2 = next(a2)
        assert_equal(atom1.molecular.position.x, atom2.molecular.position.x, options)
        assert_equal(atom1, atom2, options)

#Testing save load
#PDB
def test_pdb():
    input_dir = test_assets + ("/pdb/1fsv.pdb")
    output_dir = test_output_dir + ("/testOutput.pdb")

    complex1 = struct.Complex.io.from_pdb(input_dir)
    complex1.io.to_pdb(output_dir)

    complex2 = struct.Complex.io.from_pdb(output_dir)

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
    complex1 = struct.Complex.io.from_sdf(input_dir)
    complex2 = struct.Complex.io.from_sdf(input_dir)
    complex3 = struct.Complex.io.from_sdf(input_dir)
    complex4 = struct.Complex.io.from_sdf(input_dir)
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

    context_s = _ContextSerialization()
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

    context_s = _ContextSerialization()
    update_workspace.serialize(workspace1, context_s)

    #deserialize stuff
    context_d = _ContextDeserialization(context_s.to_array())
    workspace2 = receive_workspace.deserialize(context_d)
    assert_equal(workspace1, workspace2, options)
    
def test_iterators():
    input_dir = test_assets + ("/sdf/Thrombin_100cmpds (1).sdf")
    output_dir = test_output_dir + ("/testOutput.sdf")

    #complex level
    complex = struct.Complex.io.from_sdf(input_dir)
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
    val.rendering.selected = True
    val.rendering.atom_mode = 1  # BALLSTICK
    val.rendering.labeled = True
    val.rendering.atom_rendering = True
    val.rendering.atom_color = Color.White()
    val.rendering.surface_rendering = True
    val.rendering.surface_color = Color.White()
    val.rendering._surface_opacity = 1
    val.rendering._hydrogened = False
    val.rendering._watered = False
    val.rendering._het_atomed = False
    val.rendering._het_surfaced = False
    val.molecular.symbol = "Carbon"
    val.molecular.serial = 0
    val.molecular.name = "default"
    val.molecular.position = Vector3()
    val.molecular.is_het = False
    val.molecular._occupancy = 0
    val.molecular._bfactor = 0
    val.molecular._acceptor = False
    val.molecular._donor = False
    return val

def create_bond():
    val = struct.Bond()
    val.index = 1000
    val.molecular = struct.Bond.Molecular()
    val.atom1 = create_atom()
    val.atom2 = create_atom()
    val.molecular.kind = struct.Bond.Kind.CovalentDouble
    return val

def create_residue():
    val = struct.Residue()
    val.index = 1000
    val._atoms = [struct.Atom(), create_atom(), struct.Atom(), create_atom()]
    val._bonds = [create_bond(), create_bond(), create_bond(), create_bond()]
    val.rendering.ribboned = True
    val.rendering.ribbon_size = 1
    val.rendering.ribbon_mode = struct.Residue.RibbonMode.Coil 
    val.rendering.ribbon_color = Color.White() 
    val.molecular.type = "asdf" #RESIDUEDATA
    val.molecular.serial = 1
    val.molecular.name = "asdf1234"
    val.molecular.secondary_structure = struct.Residue.SecondaryStructure.Sheet
    return val

def create_chain():
    val = struct.Chain()
    val.index = 1000
    val._residues = [struct.Residue(), create_residue(), struct.Residue(), create_residue()]
    val.molecular.name = "fdasa1234"
    return val

def create_molecule():
    val = struct.Molecule()
    val.index = 1000
    val._chains = [struct.Chain(), create_chain(), struct.Chain(), create_chain()]
    val.molecular.name = "MIOLECASDFULE"
    val.molecular._associated = dict([("key1", "val1"), ("key2","val2"),("key3", "val3"), ("key4","val4")])
    return val

def create_complex():
    val = struct.Complex()
    val.index = 1000
    val._molecules = [struct.Molecule(), create_molecule(), struct.Molecule(), create_molecule()]
    val.rendering.boxed = True
    val.rendering.visible = False
    val.rendering.computing = False
    val.rendering.current_frame = 0
    val.molecular.name = "COMPLEX_NAME"
    val.molecular._remarks = dict([("key1", "val1"), ("key2","val2"),("key3", "val3"), ("key4","val4")])
    val.transform.position = Vector3(1,2,3)
    val.transform.rotation = Quaternion(1,2,3,4)
    return val

def create_workspace():
    workspace = struct.Workspace()
    workspace.complexes = [struct.Complex(), create_complex(), struct.Complex(), create_complex()]
    workspace.transform.position = Vector3(1,2,3)
    workspace.transform.rotation = Quaternion(1,2,3,4)
    return workspace