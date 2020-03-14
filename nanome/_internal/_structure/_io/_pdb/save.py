import nanome
from nanome._internal._structure import _Complex, _Molecule, _Chain, _Residue, _Atom, _Bond

class Results(object):
    def __init__(self):
        self.saved_atoms = []
        self.saved_bonds = []
    class SavedAtom(object):
        def __init__(self):
            self.serial = 0
            self.atom = None
            self.position = None
            self.model_number = 0
    class SavedBond(object):
        def __init__(self):
            self.serial_atom1 = 0
            self.serial_atom2 = 0
            self.bond = None

Options = nanome.util.complex_save_options.PDBSaveOptions

def to_file(path, complex, options = None):
    # type: (str, _Complex, Options) -> Results
    complex = complex._convert_to_frames()
    result = Results()
    if options is None:
        options = Options()
    serial_by_atom =  {} #<Atom, int>
    lines =  []
    line = pad_right(10, "NUMMDL")
    line += pad_right(70, str(len(complex._molecules)))
    lines.append(line)
    model_number = 1
    for molecule in complex._molecules:
        atom_serial = 1
        lines.append(start_model(model_number))
        chains = molecule._chains
        if chains is None or len(chains) == 0 or len(chains) > 80:
            print("Illegal chain data", len(chains))
            return None
        for chain in chains:
            for residue in chain._residues:
                saved_atom_constraint = options.only_save_these_atoms
                for atom in residue._atoms:
                    if saved_atom_constraint is None or atom in saved_atom_constraint:
                        if options.write_hydrogens or atom.symbol != "H":
                            serial_by_atom[atom] = atom_serial
                            lines.append(atom_to_string(atom_serial, atom, residue, chain))
                            saved_atom =  Results.SavedAtom()
                            saved_atom.serial = atom_serial
                            saved_atom.atom = atom
                            saved_atom.position = atom._position
                            saved_atom.model_number = model_number
                            result.saved_atoms.append(saved_atom)
                            atom_serial += 1
            if options.write_ters:
               lines.append(ter_to_string(atom_serial))
               atom_serial += 1
        for chain in chains:
            chain_is_het = len(chain._name) >= 2 and chain._name[0] == 'H'
            if options.write_bonds or (options.write_het_bonds and chain_is_het):
                for residue in chain._residues:
                    for bond in residue._bonds:
                        if bond._atom1 in serial_by_atom and bond._atom2 in serial_by_atom:
                            serial_atom1 = serial_by_atom[bond.atom1]
                            serial_atom2 = serial_by_atom[bond.atom2]
                            lines.append(bond_to_string(bond, serial_atom1, serial_atom2))
                            saved_bond =  Results.SavedBond()
                            saved_bond.serial_atom1 = serial_atom1
                            saved_bond.serial_atom2 = serial_atom2
                            saved_bond.bond = bond
                            result.saved_bonds.append(saved_bond)
        lines.append(end_model())
        model_number += 1
    file_text = '\n'.join(lines)
    f = open(path, "w")
    f.write(file_text)
    f.close()   
    return result
        

def start_model(model_number):
    line = pad_right(10, "MODEL")
    line += pad_left(4, str(model_number))
    line += pad_right(66, "")
    return line        

def end_model():
    return pad_right(80, "ENDMDL")

# Returns what the Atomic Coordinates for ATOM and HETATM should be in PDB

def atom_to_string(atom_serial, atom, residue, chain):
    # Prepare basic infos
    chain_name = chain._name
    if (len(chain_name) > 1):
        chain_name = chain_name[1]
    atom_element = atom.symbol
    atom_position = atom._position
    atom_name = atom._name
    if (atom_name == None):
       atom_name = atom_element
    # Choose record type
    record = "ATOM"
    if (atom.is_het):
        record = "HETATM"
    if (len(chain_name) > 1):
        chain_name = chain_name.Substring(1, 1)
    line = pad_right(6, record)
    line += pad_left_int(5, atom_serial)
    line += " "
    line += pad_left(4, pad_right(3, atom_name))
    line += pad_left(1, "")
    line += pad_left(3, residue._name)
    line += (" ")
    line += pad_left(1, chain_name)
    line += pad_left_int(4, residue.serial)
    line += (" ")
    line += ("   ")
    line += pad_left_float(8, atom_position.x, 3)
    line += pad_left_float(8, atom_position.y, 3)
    line += pad_left_float(8, atom_position.z, 3)
    line += pad_left_float(6, atom._occupancy, 2)
    line += pad_left_float(6, atom._bfactor, 2)
    line += pad_left(10, "")
    line += pad_left(2, atom_element)
    if atom._formal_charge == 0:
        line += pad_left(2, "")
    else:
        charge_str = str(abs(atom._formal_charge))
        if atom._formal_charge > 0:
            sign = "+"
        else:
            sign = "-"
        line += pad_left(2, charge_str[-1] + sign)
    line += pad_left(2, "")
    return line

def bond_to_string(bond, serial_atom1, serial_atom2):
    line = "CONECT"
    line += pad_left_int(5, serial_atom1)
    line += pad_left_int(5, serial_atom2)
    return line

def ter_to_string(serial_ter):
    line = "TER"
    line += pad_left_int(8, serial_ter)
    return line

def pad_right(pad, addition):
    base = addition
    diff = pad - len(addition)
    if diff > 0:
        for i in range(diff):
            base += ' '
    return base

def pad_left(pad, addition):
    base = ""
    diff = pad - len(addition)
    if (diff > 0):
        for i in range(diff):
            base += ' '
    base += addition
    return base

def pad_left_float(pad, value, digits):
    int_comp = int(value)
    string_val = str(round(value, digits))
    float_digits = len(string_val) - len(str(int_comp)) - 1
    if (int_comp == 0 and value < 0):
        float_digits -= 1
    for i in range(digits - float_digits):
        string_val += '0'
    return pad_left(pad, string_val)

def pad_left_int(pad, value):
    return pad_left(pad, str(value))