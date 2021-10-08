import math
from nanome.util import Vector3
from nanome._internal._structure import _Complex, _Molecule, _Chain, _Residue, _Bond, _Atom
from .content import Content
MaxCategorySize = 40


def structure(content):
    remarks = StructureRemarks(content.remarks)
    complex = _Complex._create()
    complex._remarks = remarks
    # All structured infos
    all_atoms = {}
    all_residues = {}
    all_chains = {}
    all_molecules = {}

    helper = None
    if content.cell != None:
        helper = UnitCellHelper(content.cell)

    # Read all atoms
    for c_atom in content.atoms:
        chain_name = c_atom.chain
        if c_atom.is_het:
            chain_name = "H" + chain_name

        molecule_id = str(c_atom.model)
        chain_id = molecule_id + ":" + chain_name
        residue_id = chain_id + ":" + str(c_atom.residue_serial)
        atom_id = residue_id + ":" + str(c_atom.atom_serial)
        if not atom_id in all_atoms:
            if not residue_id in all_residues:
                if not chain_id in all_chains:
                    if not molecule_id in all_molecules:
                        molecule = _Molecule._create()
                        molecule._name = str(c_atom.model)
                        all_molecules[molecule_id] = molecule
                        complex._add_molecule(molecule)
                    chain = _Chain._create()
                    chain._name = chain_name
                    all_chains[chain_id] = chain
                    all_molecules[molecule_id]._add_chain(chain)
                residue = _Residue._create()
                residue._name = c_atom.residue_name
                residue._type = residue._name
                residue.serial = c_atom.residue_serial
                all_residues[residue_id] = residue
                all_chains[chain_id]._add_residue(residue)
            atom = StructureAtom(c_atom, helper)
            all_atoms[atom_id] = None
            all_residues[residue_id]._add_atom(atom)
    # Done
    return complex._convert_to_conformers()


def StructureAtom(c_atom, helper):
    atom = _Atom._create()
    atom._serial = c_atom.atom_serial
    atom._occupancy = c_atom.occupancy
    atom._bfactor = c_atom.bfactor
    atom._position = Vector3(c_atom.x, c_atom.y, c_atom.z)
    atom._symbol = c_atom.symbol
    atom._name = c_atom.atom_name
    atom._is_het = c_atom.is_het
    if (atom._symbol == ""):
        atom._symbol = atom._name[0]
    if (c_atom.fract and helper != None):
        helper.Orthogonalize(c_atom.x, c_atom.y, c_atom.z, atom._position)
    return atom


def StructureRemarks(remarks):
    results = {}
    for category_name in remarks:
        # eliminating remarks that would be too long.
        category = remarks[category_name]
        category_size = len(category) * len(category[0])
        if (category_size <= MaxCategorySize):
            category_data = category
            object_number = 1
            for data_object in category_data:
                remark_title = category_name
                if len(category_data) > 0:
                    remark_title += " " + str(object_number)
                remark_value = ""
                for data_point_name in data_object:
                    data_point_value = data_object[data_point_name]
                    remark_value += data_point_name + ": " + data_point_value + "\n"
                results[remark_title] = remark_value
                object_number += 1
    return results


class UnitCellHelper():
    def __init__(self, cell):
        a = cell.length_a
        b = cell.length_b
        c = cell.length_c
        alpha = cell.angle_alpha
        beta = cell.angle_beta
        gamma = cell.angle_gamma
        cos_alpha = math.cos(math.radians(alpha))  # float
        cos_beta = math.cos(math.radians(beta))  # float
        cos_gamma = math.cos(math.radians(gamma))  # float
        sin_alpha = math.sin(math.radians(alpha))  # float
        sin_beta = math.sin(math.radians(beta))  # float
        sin_gamma = math.sin(math.radians(gamma))  # float
        if (sin_alpha == 0 or sin_beta == 0 or sin_gamma == 0):
            raise Exception("Impossible Unit Cell Angle")
        cos_alpha_star_sin_beta = (cos_beta * cos_gamma - cos_alpha) / sin_gamma  # float
        cos_alpha_star = cos_alpha_star_sin_beta / sin_beta  # float
        s1rca2 = math.sqrt(1.0 - cos_alpha_star * cos_alpha_star)  # float

        self.orth = [
            a, b * cos_gamma, c * cos_beta,
            0.0, b * sin_gamma, -c * cos_alpha_star_sin_beta,
            0.0, 0.0, c * sin_beta * s1rca2]

    def Orthogonalize(self, x, y, z, orth):

        orth.x = self.orth[0] * x + self.orth[1] * y + self.orth[2] * z
        orth.y = self.orth[4] * y + self.orth[5] * z
        orth.z = self.orth[8] * z
