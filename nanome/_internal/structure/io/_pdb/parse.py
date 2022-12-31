from nanome.util import Logs
from .content import Content
import re
import traceback


def parse_lines(lines):
    try:
        return _parse_lines(lines)
    except:
        Logs.error("Could not read pdb")
        raise


def _parse_lines(lines):
    lines = [line.rstrip() for line in lines]
    content = Content()
    chain_idx = 0
    chain_offset = 0
    model_number = 0
    model_done = False
    line_counter = 0
    total_lines = len(lines)
    while (line_counter < total_lines):
        line = lines[line_counter]
        try:
            record_type = record_chunk_string(line, 1, 6)
            if record_type == "MODEL":
                chain_idx = 0
                chain_offset = 0
                model_number += 1
                model_done = False
            if not model_done:
                rec = None
                if record_type == "TER":
                    ter = record_ter(line, line_counter)
                    content.records.append(ter)
                    content.ters.append(ter)
                    chain_idx += 1
                    chain_offset = 0
                if record_type == "ATOM":
                    rec = record_atom(line, line_counter)
                if record_type == "HETATM":
                    rec = record_het_atom(line, line_counter)
                if not rec == None:
                    if len(rec.chain_identifier) <= 0:
                        if rec.residue_serial_number < chain_offset:
                            chain_idx += 1
                            chain_offset = 0
                        elif rec.residue_serial_number >= chain_offset:
                            chain_offset = rec.residue_serial_number
                        rec.chain_identifier = str(chain_idx)
                    model_number = max(model_number, 1)
                    rec.model_number = model_number
                    if (not rec.residue_name == "SOL"):
                        content.records.append(rec)
                        content.atoms.append(rec)
            if (record_type == "COMPND"):
                try:
                    rec = record_compnd(line, line_counter)
                    content.records.append(rec)
                    content.compnds.append(rec)
                except:
                    Logs.warning("Error parsing COMPND:", traceback.format_exc())
            if (record_type == "REMARK"):
                rec = record_remark(line, line_counter)
                content.records.append(rec)
                if (rec.num in content._remarks):
                    content._remarks[rec.num] = content._remarks[rec.num] + "\n" + rec.text
                else:
                    content._remarks[rec.num] = rec.text
            if record_type == "CRYST":
                line = "REMARK " + line
                rec = record_cryst(line, line_counter)
                content.records.append(rec)
                content.crysts.append(rec)
            if record_type == "ORIGX":
                line = "REMARK " + line
                rec = record_origx(line, line_counter)
                content.records.append(rec)
                content.origxs.append(rec)
            if record_type == "SCALE":
                line = "REMARK " + line
                rec = record_scale(line, line_counter)
                content.records.append(rec)
                content.scales.append(rec)
            if record_type == "MTRIX":
                rec = record_mtrix(line, line_counter)
                content.records.append(rec)
                content.mtrixs.append(rec)
            if record_type == "HELIX":
                rec = record_helix(line, line_counter)
                content.records.append(rec)
                content.helixs.append(rec)
            if record_type == "SHEET":
                rec = record_sheet(line, line_counter)
                content.records.append(rec)
                content.sheets.append(rec)
            if record_type == "ENDMDL":
                model_done = True
            content.raw.append(line)
        except:
            print("LINE: " + str(line_counter))
            print("PDB Parsing error")
            raise
        line_counter += 1
    content.model_count = model_number
    return content


def record_atom(line, line_number):
    record = Content.AtomRecord()
    record.atom_serial_number = record_chunk_int(line, 6, 11)  # Sometimes atom number is on column 6
    record.atom_name = record_chunk_string(line, 12, 16)  # Sometimes atom name is on column 12
    record.atom_alternate_location = record_chunk_string(line, 17, 17)
    record.residue_name = record_chunk_string(line, 18, 20)
    record.chain_identifier = record_chunk_string(line, 22, 22)
    record.residue_serial_number = record_chunk_int(line, 23, 26)
    record.residue_insertion_code = record_chunk_string(line, 27, 27)
    record.atom_x = record_chunk_float(line, 31, 38)
    record.atom_y = record_chunk_float(line, 39, 46)
    record.atom_z = record_chunk_float(line, 47, 54)
    record.occupancy = record_chunk_float(line, 55, 60)
    record.bfactor = record_chunk_float(line, 61, 66)
    record.segment_identifier = record_chunk_string(line, 73, 76)
    record.element_symbol = record_chunk_string(line, 77, 78)
    charge_str = record_chunk_string(line, 79, 80)
    if len(charge_str) >= 1:
        record.formal_charge = int(charge_str[:1])
        if len(charge_str) >= 2 and charge_str[1] == '-':
            record.formal_charge *= -1
    # Special cases
    if (len(record.element_symbol) <= 0):
        record.element_symbol = record.atom_name
    if (len(record.residue_name) <= 0):
        record.residue_name = "LIG"
    # Extra infos
    record.type = "ATOM"
    record.line_number = line_number
    record.is_het_atom = False
    # Done
    return record


def record_het_atom(line, line_number):
    # Record object
    record = Content.AtomRecord()
    # Straight from PDB
    record.atom_serial_number = record_chunk_int(line, 7, 11)
    record.atom_name = record_chunk_string(line, 12, 16)  # Sometimes atom name is on column 12
    record.atom_alternate_location = record_chunk_string(line, 17, 17)
    record.residue_name = record_chunk_string(line, 18, 20)
    record.chain_identifier = record_chunk_string(line, 22, 22)
    record.residue_serial_number = record_chunk_int(line, 23, 26)
    record.residue_insertion_code = record_chunk_string(line, 27, 27)
    record.atom_x = record_chunk_float(line, 31, 38)
    record.atom_y = record_chunk_float(line, 39, 46)
    record.atom_z = record_chunk_float(line, 47, 54)
    record.occupancy = record_chunk_float(line, 55, 60)
    record.bfactor = record_chunk_float(line, 61, 66)
    record.segment_identifier = record_chunk_string(line, 73, 76)
    record.element_symbol = record_chunk_string(line, 77, 78)
    charge_str = record_chunk_string(line, 79, 80)
    if len(charge_str) >= 1:
        record.formal_charge = int(charge_str[:1])
        if len(charge_str) >= 2 and charge_str[1] == '-':
            record.formal_charge *= -1
    # Special cases
    if len(record.element_symbol) <= 0:
        record.element_symbol = record.atom_name

    if len(record.residue_name) <= 0:
        record.residue_name = "LIG"

    # Extra infos
    record.type = "HETATM"
    record.line_number = line_number
    record.is_het_atom = True
    # Done
    return record


def record_mtrix(line, line_number):
    # Record object
    record = Content.MtrixRecord()
    # Core record infos
    record.row = record_chunk_int(line, 6, 6)
    record.serial = record_chunk_int(line, 8, 10)
    record.mn1 = record_chunk_float(line, 11, 20)
    record.mn2 = record_chunk_float(line, 21, 30)
    record.mn3 = record_chunk_float(line, 31, 40)
    record.vn = record_chunk_float(line, 46, 55)
    record.iGiven = record_chunk_int(line, 60, 60)
    # Extra infos
    record.type = "MTRIX"
    record.line_number = line_number
    # Done
    return record


def record_origx(line, line_number):

    # Record object
    record = Content.OrigxRecord()
    # Core record infos
    record.row = record_chunk_int(line, 6, 6)
    record.on1 = record_chunk_float(line, 11, 20)
    record.on2 = record_chunk_float(line, 21, 30)
    record.on3 = record_chunk_float(line, 31, 40)
    record.tn = record_chunk_float(line, 46, 55)
    # Extra infos
    record.type = "ORIGX"
    record.line_number = line_number
    # Done
    return record


def record_scale(line, line_number):

    # Record object
    record = Content.ScaleRecord()
    # Core record infos
    record.row = record_chunk_int(line, 6, 6)
    record.sn1 = record_chunk_float(line, 11, 20)
    record.sn2 = record_chunk_float(line, 21, 30)
    record.sn3 = record_chunk_float(line, 31, 40)
    record.un = record_chunk_float(line, 46, 55)
    # Extra infos
    record.type = "SCALE"
    record.line_number = line_number
    # Done
    return record


def record_cryst(line, line_number):

    # Record object
    record = Content.CrystRecord()
    # Core record infos
    record.row = record_chunk_int(line, 6, 6)
    record.a = record_chunk_float(line, 7, 15)
    record.b = record_chunk_float(line, 16, 24)
    record.c = record_chunk_float(line, 25, 33)
    record.alpha = record_chunk_float(line, 34, 40)
    record.beta = record_chunk_float(line, 41, 47)
    record.gamma = record_chunk_float(line, 48, 54)
    record.space_group = record_chunk_string(line, 56, 66)
    record.z_value = record_chunk_int(line, 67, 70)
    # Extra infos
    record.type = "CRYST"
    record.line_number = line_number
    # Done
    return record


def record_helix(line, line_number):

    # Record object
    record = Content.HelixRecord()
    # Core record infos
    record.helix_serial_number = record_chunk_int(line, 8, 10)
    record.helix_id = record_chunk_string(line, 12, 14)
    record.residue1_name = record_chunk_string(line, 16, 18)
    record.residue1_chain_id = record_chunk_string(line, 20, 20)
    record.residue1_serial_number = record_chunk_int(line, 22, 25)
    record.residue1_insertion_code = record_chunk_string(line, 26, 26)
    record.residue2_name = record_chunk_string(line, 28, 30)
    record.residue2_chain_id = record_chunk_string(line, 32, 32)
    record.residue2_serial_number = record_chunk_int(line, 34, 37)
    record.residue2_insertion_code = record_chunk_string(line, 38, 38)
    record.helix_class = record_chunk_int(line, 39, 40)
    record.helix_comment = record_chunk_string(line, 41, 70)
    record.helix_length = record_chunk_int(line, 72, 76)
    # Extra infos
    record.type = "HELIX"
    record.line_number = line_number
    # Done
    return record


def record_sheet(line, line_number):

    # Record object
    record = Content.SheetRecord()
    # Core record infos
    record.strand_id = record_chunk_int(line, 8, 10)
    record.sheet_id = record_chunk_string(line, 12, 14)
    record.strand_count = record_chunk_int(line, 15, 16)
    # Extra infos
    record.type = "SHEET"
    record.line_number = line_number
    # Done
    return record


def record_remark(line, line_number):

    # Record object
    record = Content.RemarkRecord()
    # Core record infos
    record.num = record_chunk_string(line, 7, 10)
    record.text = record_chunk_string(line, 11, 80)
    # Extra infos
    record.type = "REMARK"
    record.line_number = line_number
    # Done
    return record


def record_compnd(line, line_number):

    # Record object
    record = Content.CompndRecord()
    # Core record infos
    record.num = record_chunk_int(line, 7, 10)
    record.text = record_chunk_string(line, 11, 80)
    # Extra infos
    record.type = "COMPND"
    record.line_number = line_number
    # Done
    return record


def record_ter(line, line_number):

    # Record object
    record = Content.TerRecord()
    # Core record infos
    record.atom_serial_number = record_chunk_int(line, 7, 11)
    record.residue_name = record_chunk_string(line, 18, 20)
    record.chain_identifier = record_chunk_string(line, 22, 22)
    record.residue_serial_number = record_chunk_int(line, 23, 26)
    record.residue_insertion_code = record_chunk_string(line, 27, 27)
    # Extra infos
    record.type = "TER"
    record.line_number = line_number
    # Done
    return record


def record_chunk_float(line, start, end):
    val = record_chunk_string(line, start, end)
    if (len(val) < 1):
        return 0
    return float(val)


def record_chunk_int(line, start, end):
    val = record_chunk_string(line, start, end)
    if (len(val) < 1):
        return 0
    return int(val)


def record_chunk_string(line, start, end):
    true_start = start - 1
    true_end = min(end, len(line))
    return line[true_start:true_end].strip()
