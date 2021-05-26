class PDBSaveOptions(object):
    """
    | Options for saving PDB files.
    | Includes options for writing:
    | - hydrogens
    | - TER records
    | - bonds
    | - heterogen bonds
    | - only selected atoms
    """

    def __init__(self):
        self.write_hydrogens = True
        self.write_ters = True
        self.write_bonds = False
        self.write_het_atoms = True
        self.write_het_bonds = True
        self.only_save_these_atoms = None


class SDFSaveOptions(object):
    """
    | Options for saving SDF files.
    | Includes options for writing:
    | - all bonds
    | - heterogen bonds
    """

    def __init__(self):
        self.write_all_bonds = True
        self.write_het_bonds = True


class MMCIFSaveOptions(object):
    """
    | Options for saving MMCIF files.
    | Includes options for writing:
    | - hydrogens
    | - only selected atoms
    """

    def __init__(self):
        self.write_hydrogens = True
        self.only_save_these_atoms = None
