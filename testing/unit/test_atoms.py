import os
import random
import time

from nanome.util import Color, Logs, Matrix, Quaternion, Vector3
from nanome.api import structure as struct
from nanome._internal._network._serialization._context import _ContextDeserialization, _ContextSerialization
from nanome._internal._network._commands._serialization import _UpdateWorkspace, _ReceiveWorkspace
from testing.unit.utilities import assert_equal, assert_not_equal, TestOptions
import unittest
import tempfile


test_assets = os.getcwd() + ("/testing/test_assets")
options = TestOptions(ignore_vars=["_unique_identifier", "_remarks", "_associateds", "_parent", "_alt_loc"])


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
    for atom1, atom2 in zip(a1, a2):
        assert(atom1.position.equals(atom2.position))
        assert_equal(atom1, atom2, options)


def build_test_workspace():
    # input_dir = test_assets + ("/sdf/Structure3D_CID_243.sdf") # withbonds
    input_dir = test_assets + ("/sdf/Thrombin_100cmpds (1).sdf")  # withbonds
    # input_dir = test_assets + ("/pdb/1fsv.pdb") # smallboy
    # input_dir = test_assets + ("/pdb/1a9l.pdb") # bigboy
    complex1 = struct.Complex.io.from_sdf(path=input_dir)
    complex2 = complex1._deep_copy()
    complex3 = complex1._deep_copy()
    complex4 = complex1._deep_copy()
    test_workspace = create_workspace()
    test_workspace.complexes = [complex1, complex2, complex3, complex4]
    return test_workspace


def count_structures(complex):
    molecule_counter = sum(1 for i in complex.molecules)
    chain_counter = sum(1 for i in complex.chains)
    residue_counter = sum(1 for i in complex.residues)
    bond_counter = sum(1 for i in complex.bonds)
    atom_counter = sum(1 for i in complex.atoms)
    print("molecule_counter:", molecule_counter)
    print("chain_counter:", chain_counter)
    print("residue_counter:", residue_counter)
    print("bond_counter:", bond_counter)
    print("atom_counter:", atom_counter)
    return molecule_counter, chain_counter, residue_counter, bond_counter, atom_counter


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
    val.type = "asdf"  # RESIDUEDATA
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
    val._associated = dict([("key1", "val1"), ("key2", "val2"), ("key3", "val3"), ("key4", "val4")])
    return val


def create_complex():
    val = struct.Complex()
    val.index = 1000
    val._molecules = [struct.Molecule(), create_molecule(), struct.Molecule(), create_molecule()]
    val.boxed = True
    val.visible = False
    val.computing = False
    val.set_current_frame(0)
    val.name = "COMPLEX_NAME"
    val._remarks = dict([("key1", "val1"), ("key2", "val2"), ("key3", "val3"), ("key4", "val4")])
    val.position = Vector3(1, 2, 3)
    val.rotation = Quaternion(1, 2, 3, 4)
    return val


def create_workspace():
    workspace = struct.Workspace()
    workspace.complexes = [struct.Complex(), create_complex(), struct.Complex(), create_complex()]
    workspace.position = Vector3(1, 2, 3)
    workspace.rotation = Quaternion(1, 2, 3, 4)
    return workspace


def assert_parents(atom, bond, residue, chain, molecule, complex):
    assert(bond.residue == residue)
    assert(bond.chain == chain)
    assert(bond.molecule == molecule)
    assert(bond.complex == complex)

    assert(atom.residue == residue)
    assert(atom.chain == chain)
    assert(atom.molecule == molecule)
    assert(atom.complex == complex)

    assert(residue.chain == chain)
    assert(residue.molecule == molecule)
    assert(residue.complex == complex)

    assert(chain.molecule == molecule)
    assert(chain.complex == complex)

    assert(molecule.complex == complex)


def assert_no_parents(atom, bond, residue, chain, molecule, complex):
    assert(bond.residue is None)
    assert(bond.chain is None)
    assert(bond.molecule is None)
    assert(bond.complex is None)

    assert(atom.residue is None)
    assert(atom.chain is None)
    assert(atom.molecule is None)
    assert(atom.complex is None)

    assert(residue.chain is None)
    assert(residue.molecule is None)
    assert(residue.complex is None)

    assert(chain.molecule is None)
    assert(chain.complex is None)

    assert(molecule.complex is None)


class AtomTestCase(unittest.TestCase):

    def test_parent_pointers(self):
        atom = struct.Atom()
        bond = struct.Bond()
        residue = struct.Residue()
        chain = struct.Chain()
        molecule = struct.Molecule()
        complex = struct.Complex()
        assert_no_parents(atom, bond, residue, chain, molecule, complex)

        complex.add_molecule(molecule)
        molecule.add_chain(chain)
        chain.add_residue(residue)
        residue.add_atom(atom)
        residue.add_bond(bond)

        assert_parents(atom, bond, residue, chain, molecule, complex)

        complex.remove_molecule(molecule)
        molecule.remove_chain(chain)
        chain.remove_residue(residue)
        residue.remove_atom(atom)
        residue.remove_bond(bond)

        assert_no_parents(atom, bond, residue, chain, molecule, complex)

    def test_matrices(self):
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

    def test_serializer_timed(self):
        maximum_time = 1
        timed = True
        test_function = self.timed_test_serializers

        try:
            start_time = time.process_time_ns()
        except AttributeError:
            # Logs.debug("No timer module. Defaulting to untimed test")
            timed = False
            maximum_time = -1
        try:
            if timed:
                test_function()
                result_time = (time.process_time_ns() - start_time) / 1000000000.0
                # Logs.debug("\texecuted in", result_time, "seconds.", result_time, "seconds per test.", "Reference time:", maximum_time, "seconds")
            else:
                test_function()

        except Exception as e:
            Logs.error(e)
            raise e
        else:
            if maximum_time >= 0.0 and result_time > maximum_time:
                message = "\ttest successful but too slow"
                Logs.error(message)
                raise AssertionError(message)

    def timed_test_serializers(self):
        # create test data
        workspace1 = create_workspace()
        # create serializers
        update_workspace = _UpdateWorkspace()
        receive_workspace = _ReceiveWorkspace()

        context_s = _ContextSerialization(plugin_id=random.randint(0, 0xFFFFFFFF))
        update_workspace.serialize(0, workspace1, context_s)

        # deserialize stuff
        context_d = _ContextDeserialization(context_s.to_array())
        workspace2 = receive_workspace.deserialize(0, context_d)
        assert_equal(workspace1, workspace2, options)

    def test_iterators(self):
        input_dir = test_assets + ("/sdf/Thrombin_100cmpds (1).sdf")

        # complex level
        complex = struct.Complex.io.from_sdf(path=input_dir)
        complex = complex.convert_to_frames()
        a = 0
        for atom in complex.atoms:
            a += 1
        assert(a == 5721)
        a = 0
        for residue in complex.residues:
            for atom in residue.atoms:
                a += 1
        assert(a == 5721)
        a = 0
        for chain in complex.chains:
            for atom in chain.atoms:
                a += 1
        assert(a == 5721)
        a = 0
        for molecule in complex.molecules:
            for atom in molecule.atoms:
                a += 1
        assert(a == 5721)
        a = 0
        # gets first molecule
        molecule = next(complex.molecules)
        for residue in molecule.residues:
            for atom in residue.atoms:
                a += 1
        assert(a == 76)
        a = 0
        for chain in molecule.chains:
            for atom in chain.atoms:
                a += 1
        assert(a == 76)
        a = 0
        for residue in molecule.residues:
            for atom in residue.atoms:
                a += 1
        assert(a == 76)
        a = 0
        chain = next(molecule.chains)
        for residue in chain.residues:
            for atom in residue.atoms:
                a += 1
        assert(a == 76)
        b = False
        for residue in chain.residues:
            for _ in residue.bonds:
                b = True
        assert(b)

    def test_equality(self):
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

    def test_structures(self):
        create_atom()
        create_bond()
        create_residue()
        create_chain()
        create_molecule()

    def test_pdb(self):
        # Testing save load PDB
        input_dir = test_assets + ("/pdb/1fsv.pdb")
        output_file = tempfile.NamedTemporaryFile(suffix='.pdb').name

        complex1 = struct.Complex.io.from_pdb(path=input_dir)
        complex1.io.to_pdb(output_file)

        complex2 = struct.Complex.io.from_pdb(path=input_dir)

        compare_atom_positions(complex1, complex2)
        assert_equal(complex1, complex2, options)
        assert_not_equal(complex2, struct.Complex(), options)
