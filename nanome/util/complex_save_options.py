class PDBSaveOptions(object):
    def __init__(self):
        self.write_hydrogens = True
        self.write_ters = True
        self.write_bonds = False
        self.write_het_bonds = True
        self.only_save_these_atoms = None

class SDFSaveOptions(object):
    def __init__(self):
        self.write_all_bonds = True
        self.write_het_bonds = True

class MMCIFSaveOptions(object):
    def __init__(self):
        self.write_hydrogens = True
        self.only_save_these_atoms = None