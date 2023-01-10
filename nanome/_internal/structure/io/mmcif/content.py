
class Content(object):
    def __init__(self):
        self.atoms = []
        self.cell = None
        # Raw file content in the mapping format
        # Dictionary<string, List<Dictionary<string, string>>>
        self.remarks = {}

    # Stores all the information of an MMCIF atom
    class Atom(object):
        def __init__(self):
            self.symbol = ""
            self.atom_serial = 0
            self.atom_name = "Carbon"
            self.residue_serial = 1
            self.residue_name = "UNK"
            self.chain = "A"
            self.x = 0.1
            self.y = 0.1
            self.z = 0.1
            self.occupancy = 0.1
            self.bfactor = 0.1
            self.is_het = False
            self.fract = False
            # model indicate structure that need to put into complex
            self.model = 1

    class UnitCell(object):
        def __init__(self):
            self.length_a = 1
            self.length_b = 1
            self.length_c = 1
            self.angle_alpha = 90
            self.angle_beta = 90
            self.angle_gamma = 90
