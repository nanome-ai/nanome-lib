from nanome.util import Logs
import traceback
import time
import re
from .content import Content


class _CIF_Lines(object):
    def __init__(self, lines):
        self.lines = lines
        self.curr_index = 0
        self.end = len(lines)

    def isEnd(self):
        return self.curr_index >= self.end

    def move_next(self):
        self.curr_index += 1

    def get_line(self):
        return self.lines[self.curr_index]

    def move_next_val(self):
        while not self.isEnd():
            line = self.get_line()
            if is_section_starter(line):
                return
            self.move_next()

    def get_line_number(self):
        return self.curr_index + 1

    def set_line_number(self, line):
        self.curr_index = line - 1

# using ParsedObject = Dictionary<string, string>
# using ParsedFile = Dictionary<string, List<Dictionary<string, string>>>


def parse_lines(lines):
    try:
        return _parse_lines(lines)
    except:
        Logs.error("Could not read mmcif")
        raise


def _parse_lines(lines):
    lines = [line.rstrip() for line in lines]
    # Content structure
    lines = _CIF_Lines(lines)
    try:
        parsed_file = ParseLines(lines)
    except Exception:
        Logs.error("\tParse failed. Error on line:", lines.get_line_number())
        Logs.error(traceback.format_exc())
    content = raw_to_formatted(parsed_file)
    return content


# MMCIF CONSTANTS
atoms_key = "_atom_site"
atom_symbol_key = "type_symbol"
atom_serial_key = "id"
atom_name_key = ["auth_atom_id", "label"]
atom_residue_serial_key = "auth_seq_id"
atom_residue_name_key = "auth_comp_id"
atom_chain_key = "auth_asym_id"
atom_x_key = ["Cartn_x", "fract_x"]
atom_y_key = ["Cartn_y", "fract_y"]
atom_z_key = ["Cartn_z", "fract_z"]
atom_occupancy_key = "occupancy"
atom_bfactor_key = "B_iso_or_equiv"
atom_model_key = "pdbx_PDB_model_num"
atom_type_key = "group_PDB"

cell_length_a = "length_a"
cell_length_b = "length_b"
cell_length_c = "length_c"
cell_angle_alpha = "angle_alpha"
cell_angle_beta = "angle_beta"
cell_angle_gamma = "angle_gamma"

# Formatting the parsed data


def raw_to_formatted(parsed_file):
    content = Content()
    if (atoms_key in parsed_file):
        for parsed_object in parsed_file[atoms_key]:
            atom = raw_to_atom(parsed_object)
            if not atom is None:
                content.atoms.append(atom)
        del parsed_file[atoms_key]
    else:
        all_objects = parsed_file["Misc"]
        backup_serial = 0
        content.cell = Content.UnitCell()
        # backwards iteration so we can delete as we go
        for i in range(len(all_objects) - 1, -1, -1):
            parsed_object = all_objects[i]
            raw_to_unit_cell_messy(parsed_object, content.cell)
            atom = raw_to_atom_messy(parsed_object)
            if atom is None:
                continue
            if (atom.atom_serial == 0):
                atom.atom_serial = backup_serial
                backup_serial += 1
            content.atoms.append(atom)
            del all_objects[i]
    content.remarks = parsed_file
    return content


def raw_to_unit_cell_messy(parsed_object, cell):
    prefix = "_cell_"
    valid_key = get_valid_key(parsed_object, prefix_keys(prefix, [cell_length_a]))
    if (valid_key != None):
        cell.length_a = get_uncertain_float(parsed_object, valid_key)
    valid_key = get_valid_key(parsed_object, prefix_keys(prefix, [cell_length_b]))
    if (valid_key != None):
        cell.length_b = get_uncertain_float(parsed_object, valid_key)
    valid_key = get_valid_key(parsed_object, prefix_keys(prefix, [cell_length_c]))
    if (valid_key != None):
        cell.length_c = get_uncertain_float(parsed_object, valid_key)
    valid_key = get_valid_key(parsed_object, prefix_keys(prefix, [cell_angle_alpha]))
    if (valid_key != None):
        cell.angle_alpha = get_uncertain_float(parsed_object, valid_key)
    valid_key = get_valid_key(parsed_object, prefix_keys(prefix, [cell_angle_beta]))
    if (valid_key != None):
        cell.angle_beta = get_uncertain_float(parsed_object, valid_key)
    valid_key = get_valid_key(parsed_object, prefix_keys(prefix, [cell_angle_gamma]))
    if (valid_key != None):
        cell.angle_gamma = get_uncertain_float(parsed_object, valid_key)

# converts raw data to formatted atom for files without categories.


def raw_to_atom_messy(parsed_object):
    prefix = atoms_key + "_"
    atom = Content.Atom()
    is_atom = False

    valid_key = get_valid_key(parsed_object, prefix_keys(prefix, [atom_symbol_key]))
    if (valid_key != None):
        is_atom = True
        atom.symbol = get_string(parsed_object, valid_key)

    valid_key = get_valid_key(parsed_object, prefix_keys(prefix, [atom_serial_key]))
    if (valid_key != None):
        is_atom = True
        atom.atom_serial = get_int(parsed_object, valid_key)

    valid_key = get_valid_key(parsed_object, prefix_keys(prefix, atom_name_key))
    if (valid_key != None):
        is_atom = True
        atom.atom_name = get_string(parsed_object, valid_key)

    valid_key = get_valid_key(parsed_object, prefix_keys(prefix, [atom_residue_serial_key]))
    if (valid_key != None):
        is_atom = True
        atom.residue_serial = get_int(parsed_object, valid_key)

    valid_key = get_valid_key(parsed_object, prefix_keys(prefix, [atom_residue_name_key]))
    if (valid_key != None):
        is_atom = True
        atom.residue_name = get_string(parsed_object, valid_key)

    valid_key = get_valid_key(parsed_object, prefix_keys(prefix, [atom_chain_key]))
    if (valid_key != None):
        is_atom = True
        atom.chain = get_string(parsed_object, valid_key)

    valid_key = get_valid_key(parsed_object, prefix_keys(prefix, atom_x_key))
    if (valid_key != None):
        is_atom = True
        atom.x = get_uncertain_float(parsed_object, valid_key)

    valid_key = get_valid_key(parsed_object, prefix_keys(prefix, atom_y_key))
    if (valid_key != None):
        is_atom = True
        atom.y = get_uncertain_float(parsed_object, valid_key)

    valid_key = get_valid_key(parsed_object, prefix_keys(prefix, atom_z_key))
    if (valid_key != None):
        is_atom = True
        atom.z = get_uncertain_float(parsed_object, valid_key)

    valid_key = get_valid_key(parsed_object, prefix_keys(prefix, [atom_occupancy_key]))
    if (valid_key != None):
        is_atom = True
        atom.occupancy = get_uncertain_float(parsed_object, valid_key)

    valid_key = get_valid_key(parsed_object, prefix_keys(prefix, [atom_bfactor_key]))
    if (valid_key != None):
        is_atom = True
        atom.bfactor = get_uncertain_float(parsed_object, valid_key)

    valid_key = get_valid_key(parsed_object, prefix_keys(prefix, [atom_model_key]))
    if (valid_key != None):
        is_atom = True
        atom.model = get_int(parsed_object, valid_key)

    valid_key = get_valid_key(parsed_object, prefix_keys(prefix, [atom_type_key]))
    if (valid_key != None):
        type = get_string(parsed_object, valid_key)
        if (type == "ATOM"):
            atom.is_het = False
        if (type == "HETATM"):
            atom.is_het = True

    isCart = get_valid_key(parsed_object, prefix_keys(prefix, ["fract_x"])) == None
    atom.fract = not isCart

    if (not is_atom):
        return None

    return atom


def raw_to_atom(parsed_object):
    try:
        atom = Content.Atom()

        valid_key = get_valid_key(parsed_object, [atom_symbol_key])
        if (valid_key != None):
            atom.symbol = get_string(parsed_object, valid_key)

        valid_key = get_valid_key(parsed_object, [atom_serial_key])
        if (valid_key != None):
            atom.atom_serial = get_int(parsed_object, valid_key)

        valid_key = get_valid_key(parsed_object, atom_name_key)
        if (valid_key != None):
            atom.atom_name = get_string(parsed_object, valid_key)

        valid_key = get_valid_key(parsed_object, [atom_residue_serial_key])
        if (valid_key != None):
            atom.residue_serial = get_int(parsed_object, valid_key)

        valid_key = get_valid_key(parsed_object, [atom_residue_name_key])
        if (valid_key != None):
            atom.residue_name = get_string(parsed_object, valid_key)

        valid_key = get_valid_key(parsed_object, [atom_chain_key])
        if (valid_key != None):
            atom.chain = get_string(parsed_object, valid_key)

        valid_key = get_valid_key(parsed_object, atom_x_key)
        if (valid_key != None):
            atom.x = get_float(parsed_object, valid_key)

        valid_key = get_valid_key(parsed_object, atom_y_key)
        if (valid_key != None):
            atom.y = get_float(parsed_object, valid_key)

        valid_key = get_valid_key(parsed_object, atom_z_key)
        if (valid_key != None):
            atom.z = get_float(parsed_object, valid_key)

        valid_key = get_valid_key(parsed_object, [atom_occupancy_key])
        if (valid_key != None):
            atom.occupancy = get_float(parsed_object, valid_key)

        valid_key = get_valid_key(parsed_object, [atom_bfactor_key])
        if (valid_key != None):
            atom.bfactor = get_float(parsed_object, valid_key)

        valid_key = get_valid_key(parsed_object, [atom_model_key])
        if (valid_key != None):
            atom.model = get_int(parsed_object, valid_key)

        valid_key = get_valid_key(parsed_object, [atom_type_key])
        if (valid_key != None):
            type = get_string(parsed_object, valid_key)
            if (type == "ATOM"):
                atom.is_het = False
            if (type == "HETATM"):
                atom.is_het = True

        isCart = get_valid_key(parsed_object, "fract_x") == None
        atom.fract = not isCart
        return atom
    except:
        Logs.error("Error while parsing MMCIF atom")
        raise

# Parsing the file


def ParseLines(lines):
    parsed_file = {}

    # find first field
    lines.move_next_val()

    while not lines.isEnd():
        try:
            section_objects, category = parse_category(lines)
            if (category != None and section_objects != None):
                if category in parsed_file:
                    parsed_file[category] += section_objects
                else:
                    parsed_file[category] = section_objects
        except Exception:
            Logs.warning("Problem during parsing, skipping line. Error on line:", lines.get_line_number())
            Logs.warning(traceback.format_exc())
            lines.move_next()
    return parsed_file


def parse_category(lines):
    sections_objects = None
    category = None
    lines.move_next_val()
    if not lines.isEnd():
        line = lines.get_line()
        if (is_loop_header(line)):
            lines.move_next()
            sections_objects, category = parse_loop(lines)
        elif (is_definition(line)):
            sections_objects, category = parse_single_val(lines)
        else:
            lines.move_next()
    return sections_objects, category


def parse_loop(lines):
    keys = []
    parsed_objects = []
    category = None
    # Get all the keys
    while not lines.isEnd():
        line = lines.get_line()
        if not is_definition(line):
            break
        category, key, value = get_data_category(line)
        keys.append(key)
        lines.move_next()
    # Read values and pair them with keys
    while not lines.isEnd():
        try:
            parsed_object = {}
            line = lines.get_line()
            if (is_empty(line)):
                lines.move_next()
                continue
            if (is_section_starter(line) or
                    is_comment(line)):
                break
            lines.move_next()
            splits = split_line(line)  # split by whitespace
            while (len(splits) < len(keys)):  # multi-line case
                line = lines.get_line()
                lines.move_next()
                splits += split_line(line)
            for i in range(len(keys)):  # pair keys with line values
                key = keys[i]
                value = splits[i]
                parsed_object[key] = value
            parsed_objects.append(parsed_object)
        except:
            Logs.debug("MMCIF_Parsing")
            raise
    return parsed_objects, category


def parse_single_val(lines):
    parsed_objects = []
    line = lines.get_line()
    lines.move_next()

    category, key, value = get_data_category(line)
    if (value == None):  # value is on next line
        line = lines.get_line()
        # input is multi-line. gotta read lines until we see another ';'
        if is_multiline(line):
            value = compose_multiline_val(lines)
        # input is exactly 2 lines
        else:
            lines.move_next()
            value = line

    section_object = {}
    section_object[key] = value
    parsed_objects.append(section_object)
    return parsed_objects, category

# reads a multiline value and composes it into a single string


def compose_multiline_val(lines):
    max_lines = 10
    starting_line_number = lines.get_line_number()
    line = lines.get_line()
    lines.move_next()
    multi_line = record_chunk_string(line, 2)
    while not lines.isEnd():
        line = lines.get_line()
        lines.move_next()
        if is_multiline(line):
            break
        else:
            multi_line += line
        # Prevent unclosed multi-lines from breaking everything.
        if (lines.get_line_number() - starting_line_number > max_lines):
            lines.set_line_number(starting_line_number)
            # It will try reading each line (and fail) until it leaves the broken section.
            raise Exception("Multi-line field excedes max number of lines (" + str(max_lines) + ")")
    return multi_line

# region line checkers


def is_section_starter(line):
    return (is_loop_header(line) or is_definition(line))


def is_loop_header(line):
    first_five = record_chunk_string(line, 1, 5)
    return (first_five == "loop_")


def is_definition(line):
    first_val = record_chunk_string(line, 1, 1)
    return (first_val == "_")


def is_comment(line):
    first_val = record_chunk_string(line, 1, 1)
    return (first_val == "#")


def is_multiline(line):
    first_val = record_chunk_string(line, 1, 1)
    return (first_val == ";")


def is_empty(line):
    return (line == "")
# endregion

# Tools for parsing strings
# return the string from start to end position after excluding the white space


def record_chunk_string(line, start=1, end=2147483647):
    true_start = start - 1
    true_end = min(end, len(line))
    return line[true_start:true_end].strip()


# captures "<category>.<key> <value> "
# there must be some whitespace between <key> and <value> and there can be any amount of whitespace at the end.
# category is 1 word and optional,
# key is 1 word
# and the value can be either 1 word or any number of words wrapped in single quotes.
category_regex = re.compile(r"^(?:([^\s]+)\.)?([^\s]+)(?:\s+((?:[^\s]*)|(?:\'.*\')))?\s*$")


def get_data_category(line):
    match = re.match(category_regex, line)
    if (match == None):
        Logs.error(line)
        return
    category = match.group(1)
    key = match.group(2)
    value = match.group(3)
    if category == None:
        category = "Misc"
    return category, key, value


# splits item by space, except for those contained by quotes
split_regex = re.compile(r"(['\"])(.+?)\1|([^\s]+)")


def split_line(line):
    groups = re.findall(split_regex, line)
    result = []
    for group in groups:
        if not group[1] == "":
            result.append(group[1])
        else:
            result.append(group[2])
    return result

# Tools for reading values from the Parsed Objects


def get_valid_key(obj, keys):
    for key in keys:
        if (key in obj):
            return key
    return None


def get_string(obj, key):
    return obj[key]


def get_int(obj, key):
    return int(obj[key])


def get_float(obj, key):
    return float(obj[key])

# Tools for reading poorly formatted values from Parsed Objects


def prefix_keys(prefix, keys):
    new_keys = []
    for key in keys:
        new_keys.append(prefix + key)
    return new_keys


def get_uncertain_float(obj, key):
    return float(obj[key].split("(")[0])
