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

Options = nanome.util.complex_save_options.MMCIFSaveOptions

class ColumnWidths(object):
    def __init__(self):
        self.group_PDB = 0
        self.id = 0
        self.type_symbol = 0
        self.cartn_x = 0
        self.cartn_y = 0
        self.cartn_z = 0
        self.occupancy = 0
        self.b_iso_or_equiv = 0
        self.auth_seq_id = 0
        self.auth_comp_id = 0
        self.auth_asym_id = 0
        self.auth_atom_id = 0
        self.pdbx_PDB_model_num = 0


class AtomText(object):
    def __init__(self):
        self.group_PDB = ""
        self.id = ""
        self.type_symbol = ""
        self.cartn_x = ""
        self.cartn_y = ""
        self.cartn_z = ""
        self.occupancy = ""
        self.b_iso_or_equiv = ""
        self.auth_seq_id = ""
        self.auth_comp_id = ""
        self.auth_asym_id = ""
        self.auth_atom_id = ""
        self.pdbx_PDB_model_num = ""


def to_file(path, complex, options=None):
    # type: (str, _Complex, Options) -> Results
    complex = complex._convert_to_frames()
    result = Results()
    if options is None:
        options = Options()
    saved_atom_constraint = options.only_save_these_atoms

    atom_num = 1
    model_num = 1
    text_atoms = []
    column_widths = ColumnWidths()
    for molecule in complex._molecules:
        for chain in molecule._chains:
            for residue in chain._residues:
                for atom in residue._atoms:
                    if saved_atom_constraint is None or atom in saved_atom_constraint:
                        if options.write_hydrogens or atom.symbol != "H":
                            saved_atom = atom_to_saved_atom(
                                atom, atom_num, model_num)
                            result.saved_atoms.append(saved_atom)
                            text_atom = atom_to_text(atom, residue, chain,
                                                    atom_num, model_num)
                            text_atoms.append(text_atom)
                            update_column_widths(text_atom, column_widths)
                            atom_num += 1
        model_num += 1
    lines = create_header()
    for text_atom in text_atoms:
        lines.append(text_atom_to_line(text_atom, column_widths))
    lines.append("#")
    file_text = '\n'.join(lines)
    f = open(path, "w")
    f.write(file_text)
    f.close()
    return result


def create_header():
    lines = []
    lines.append("title")
    lines.append("#")
    lines.append("loop_")
    lines.append("_atom_site.group_PDB")
    lines.append("_atom_site.id")
    lines.append("_atom_site.type_symbol")
    lines.append("_atom_site.Cartn_x")
    lines.append("_atom_site.Cartn_y")
    lines.append("_atom_site.Cartn_z")
    lines.append("_atom_site.occupancy")
    lines.append("_atom_site.B_iso_or_equiv")
    lines.append("_atom_site.auth_seq_id")
    lines.append("_atom_site.auth_comp_id")
    lines.append("_atom_site.auth_asym_id")
    lines.append("_atom_site.auth_atom_id")
    lines.append("_atom_site.pdbx_PDB_model_num")
    return lines


def text_atom_to_line(text_atom, column_widths):
    # type: (AtomText, ColumnWidths) -> str
    line = ""
    line += pad_right(1 + column_widths.group_PDB, text_atom.group_PDB)
    line += pad_right(1 + column_widths.id, text_atom.id)
    line += pad_right(1 + column_widths.type_symbol, text_atom.type_symbol)
    line += pad_right(1 + column_widths.cartn_x, text_atom.cartn_x)
    line += pad_right(1 + column_widths.cartn_y, text_atom.cartn_y)
    line += pad_right(1 + column_widths.cartn_z, text_atom.cartn_z)
    line += pad_right(1 + column_widths.occupancy, text_atom.occupancy)
    line += pad_right(1 + column_widths.b_iso_or_equiv, text_atom.b_iso_or_equiv)
    line += pad_right(1 + column_widths.auth_seq_id, text_atom.auth_seq_id)
    line += pad_right(1 + column_widths.auth_comp_id, text_atom.auth_comp_id)
    line += pad_right(1 + column_widths.auth_asym_id, text_atom.auth_asym_id)
    line += pad_right(1 + column_widths.auth_atom_id,
                      add_quotes_if_needed(text_atom.auth_atom_id))
    line += pad_right(1 + column_widths.pdbx_PDB_model_num,
                      text_atom.pdbx_PDB_model_num)
    return line


def atom_to_text(atom, residue, chain, id, model):
    # type: (_Atom, _Residue, _Chain, int, int) -> AtomText
    chain_name = chain._name
    if atom.is_het and chain_name[0] == "H":
        chain_name = chain_name[1:]
    if atom.is_het:
        type_key = "HETATM"
    else:
        type_key = "ATOM"
    text = AtomText()
    text.group_PDB = type_key
    text.id = str(id)
    text.type_symbol = atom._symbol
    text.cartn_x = float_to_string(atom._position.x, 3)
    text.cartn_y = float_to_string(atom._position.y, 3)
    text.cartn_z = float_to_string(atom._position.z, 3)
    text.occupancy = float_to_string(atom._occupancy, 2)
    text.b_iso_or_equiv = float_to_string(atom._bfactor, 2)
    text.auth_seq_id = str(residue._serial)
    text.auth_comp_id = residue._name
    text.auth_asym_id = chain_name
    text.auth_atom_id = atom._name
    text.pdbx_PDB_model_num = str(model)
    return text


def atom_to_saved_atom(atom, id, model):
    # type: (_Atom, int, int) -> Results.SavedAtom
    saved_atom = Results.SavedAtom()
    saved_atom.serial = id
    saved_atom.atom = atom
    saved_atom.position = atom._position
    saved_atom.model_number = model
    return saved_atom


def update_column_widths(text_atom, column_widths):
    # type: (AtomText, ColumnWidths)
    column_widths.group_PDB = max(
        len(text_atom.group_PDB), column_widths.group_PDB)
    column_widths.id = max(len(text_atom.id), column_widths.id)
    column_widths.type_symbol = max(
        len(text_atom.type_symbol), column_widths.type_symbol)
    column_widths.cartn_x = max(len(text_atom.cartn_x), column_widths.cartn_x)
    column_widths.cartn_y = max(len(text_atom.cartn_y), column_widths.cartn_y)
    column_widths.cartn_z = max(len(text_atom.cartn_z), column_widths.cartn_z)
    column_widths.occupancy = max(
        len(text_atom.occupancy), column_widths.occupancy)
    column_widths.b_iso_or_equiv = max(
        len(text_atom.b_iso_or_equiv), column_widths.b_iso_or_equiv)
    column_widths.auth_seq_id = max(
        len(text_atom.auth_seq_id), column_widths.auth_seq_id)
    column_widths.auth_comp_id = max(
        len(text_atom.auth_comp_id), column_widths.auth_comp_id)
    column_widths.auth_asym_id = max(
        len(text_atom.auth_asym_id), column_widths.auth_asym_id)
    column_widths.auth_atom_id = max(
        len(text_atom.auth_atom_id), column_widths.auth_atom_id)
    column_widths.pdbx_PDB_model_num = max(
        len(text_atom.pdbx_PDB_model_num), column_widths.pdbx_PDB_model_num)


def float_to_string(value, digits):
    # type: (float, int) -> str
    int_comp = int(value)
    string_val = str(round(value, digits))
    float_digits = len(string_val) - len(str(int_comp)) - 1
    if (int_comp == 0 and value < 0):
        float_digits -= 1
    for i in range(digits - float_digits):
        string_val += '0'
    return string_val


def add_quotes_if_needed(text):
    # type: (str) -> str
    if "'" in text:
        return "\"" + text + "\""
    else:
        return text


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


def pad_left_int(pad, value):
    return pad_left(pad, str(value))