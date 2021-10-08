import nanome
from nanome._internal._structure import _Complex, _Molecule, _Chain, _Residue, _Atom, _Bond
from nanome.util import Logs

Options = nanome.util.complex_save_options.SDFSaveOptions


class Results(object):
    def __init__(self):
        self.saved_atoms = []
        self.saved_bonds = []

    class SavedAtom(object):
        def __init(self):
            self.serial = 0
            self.atom = None
            self.model_number = 0

    class SavedBond(object):
        def __init(self):
            self.serial_atom1 = 0
            self.serial_atom2 = 0
            self.bond = None


def to_file(path, complex, options=None):
    # type: (str, _Complex, Options) -> Results
    complex = complex._convert_to_frames()
    if options is None:
        options = Options()
    lines = []
    molecule_number = 1
    result = None
    for molecule in complex._molecules:
        result = Results()
        if molecule_number != 1:
            lines.append("$$$$")
        number_atoms = 0
        number_bonds = 0
        serial_by_atom_unique = {}  # <long, int>
        atom_serial = 1

        chains = molecule._chains
        chains_count = len(chains)
        if (chains == None) or (chains_count == 0) or chains_count > 80:
            print("Illegal chain data", chains_count)
            return None
        for chain in chains:
            for residue in chain._residues:
                for atom in residue._atoms:
                    serial_by_atom_unique[atom._unique_identifier] = atom_serial
                    saved_atom = Results.SavedAtom()
                    saved_atom.serial = atom_serial
                    saved_atom.atom = atom
                    saved_atom.model_number = molecule_number
                    result.saved_atoms.append(saved_atom)
                    atom_serial += 1
                    number_atoms += 1
        for chain in chains:
            if (options.write_all_bonds) or (options.write_het_bonds and chain._name[0] == 'H'):
                for residue in chain._residues:
                    for bond in residue._bonds:
                        if bond.atom1._unique_identifier in serial_by_atom_unique and bond.atom2._unique_identifier in serial_by_atom_unique:
                            saved_bond = Results.SavedBond()
                            saved_bond.serial_atom1 = serial_by_atom_unique[bond.atom1._unique_identifier]
                            saved_bond.serial_atom2 = serial_by_atom_unique[bond.atom2._unique_identifier]
                            saved_bond.bond = bond
                            result.saved_bonds.append(saved_bond)
                            number_bonds += 1
        add_header(lines, molecule._name, number_atoms, number_bonds)
        add_atoms(lines, result.saved_atoms)
        add_bonds(lines, result.saved_bonds)
        add_footer(lines)
        molecule_number += 1
    file_text = '\n'.join(lines)
    f = open(path, "w")
    f.write(file_text)
    f.close()
    return result


def add_header(lines, name, atom_count, bond_count):
    lines.append(name)
    lines.append("Nanome Inc. SDF Saver")
    lines.append("")
    lines.append("  0  0  0     0  0            999 V3000")
    lines.append("M  V30 BEGIN CTAB")
    lines.append("M  V30 COUNTS " + str(atom_count) + " " + str(bond_count) + " 0 0 0")


def add_atoms(lines, saved_atoms):
    lines.append("M  V30 BEGIN ATOM")
    for saved_atom in saved_atoms:
        serial = saved_atom.serial
        atom = saved_atom.atom
        new_line = "M  V30"
        new_line += " "
        new_line += str(serial)
        new_line += " "
        new_line += atom.symbol
        new_line += " "
        new_line += float_to_string(atom._position.x, 4)
        new_line += " "
        new_line += float_to_string(atom._position.y, 4)
        new_line += " "
        new_line += float_to_string(atom._position.z, 4)
        new_line += " "
        new_line += "0"
        new_line += " "
        if atom._formal_charge != 0:
            new_line += "CHG=" + str(atom._formal_charge)
        lines.append(new_line)
    lines.append("M  V30 END ATOM")


def add_bonds(lines, saved_bonds):
    linked = {}  # <long,bool>
    idx = 0
    lines.append("M  V30 BEGIN BOND")
    for saved_bond in saved_bonds:
        serial1 = saved_bond.serial_atom1
        serial2 = saved_bond.serial_atom2
        key1 = (serial1 << 32) + serial2
        key2 = (serial2 << 32) + serial1
        if not key1 in linked and not key2 in linked and serial1 != serial2:
            linked[key1] = True
            bond = saved_bond.bond
            idx += 1
            new_line = "M  V30"
            new_line += " "
            new_line += str(idx)
            new_line += " "
            new_line += str(int(bond.kind))
            new_line += " "
            new_line += str(serial1)
            new_line += " "
            new_line += str(serial2)
            lines.append(new_line)
    lines.append("M  V30 END BOND")


def float_to_string(value, digits):
    int_comp = int(value)
    string_val = str(round(value, digits))
    float_digits = len(string_val) - len(str(int_comp)) - 1
    if (int_comp == 0 and value < 0):
        float_digits -= 1
    for i in range(digits - float_digits):
        string_val += '0'
    return string_val


def add_footer(lines):
    lines.append("M  V30 END CTAB")
    lines.append("M  END")
