class Content(object):
    def __init__(self):
        self.raw = []
        self.records = []
        self._remarks = {}
        self.compnds = []
        self.crysts = []
        self.mtrixs = []
        self.origxs = []
        self.scales = []
        self.helixs = []
        self.sheets = []
        self.ters = []
        self.atoms = []
        self.model_count = 0

    class Record(object):
        def __init__(self):
            type = ""
            line_number = 0
    class MtrixRecord(Record):
        def __init__(self):
            self.row = 0
            self.serial = 0
            self.mn1 = 0
            self.mn2 = 0
            self.mn3 = 0
            self.vn = 0
            self.iGiven = 0
    class OrigxRecord(Record):
        def __init__(self):
            self.row = 0
            self.on1 = 0
            self.on2 = 0
            self.on3 = 0
            self.tn = 0
    class ScaleRecord(Record):
        def __init__(self):
            self.row = 0
            self.sn1 = 0
            self.sn2 = 0
            self.un = 0
    class CrystRecord(Record):
        def __init__(self):
            self.row = 0
            self.a = 0
            self.b = 0
            self.c = 0
            self.alpha = 0
            self.beta = 0
            self.gamma = 0
            self.space_group = 0
            self.z_value = 0
    class HelixRecord(Record):
        def __init__(self):
            self.helix_serial_number = 0
            self.helix_id = ""
            self.residue1_name = ""
            self.residue1_chain_id = ""
            self.residue1_serial_number = 0
            self.residue1_insertion_code = ""
            self.residue2_name = ""
            self.residue2_chain_id = ""
            self.residue2_serial_number = 0
            self.residue2_insertion_code = ""
            self.helix_class = 0
            self.helix_comment = ""
            self.helix_length = 0
    class SheetRecord(Record):
        def __init__(self):
            self.strand_id = 0
            self.sheet_id = ""
            self.strand_count = 0
    class AtomRecord(Record):
        def __init__(self):
            self.atom_serial_number = 0
            self.atom_name = ""
            self.atom_alternate_location = ""
            self.residue_name = ""
            self.chain_identifier = ""
            self.model_number = 0
            self.residue_serial_number = 0
            self.residue_insertion_code = ""
            self.atom_x = 0
            self.atom_y = 0
            self.atom_z = 0
            self.occupancy = 0
            self.bfactor = 0
            self.segment_identifier = ""
            self.element_symbol = ""
            self.formal_charge = 0
            self.is_het_atom = False
    class TerRecord(Record):
        def __init__(self):
            self.atom_serial_number = 0
            self.residue_name = ""
            self.chain_identifier = ""
            self.residue_serial_number = 0
            self.residue_insertion_code = ""
    class RemarkRecord(Record):
        def __init__(self):
            self.num = ""
            self.text = ""
    class CompndRecord(Record):
        def __init__(self):
            self.num = 0
            self.text = ""
