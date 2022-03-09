import nanome
from nanome.util import Color, Logs
from . import _helpers
from . import _Base


class _Residue(_Base):
    RibbonMode = nanome.util.enums.RibbonMode
    SecondaryStructure = nanome.util.enums.SecondaryStructure

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_Residue, self).__init__()
        # molecular
        self._type = "ARG"  # RESIDUEDATA
        self._serial = 1
        self._name = "res"
        self._secondary_structure = _Residue.SecondaryStructure.Unknown
        # rendering
        self._ribboned = True
        self._ribbon_size = 1.0
        self._ribbon_mode = _Residue.RibbonMode.SecondaryStructure
        self._ribbon_color = Color.Clear()
        self._labeled = False
        self._label_text = ""
        self._ignored_alt_locs = []
        # connections
        self._atoms = []
        self._bonds = []
        self._parent = None

    def _add_atom(self, atom):
        self._atoms.append(atom)
        atom._parent = self

    def _remove_atom(self, atom):
        if atom in self._atoms:
            atom.index = -1
            self._atoms.remove(atom)
            atom._parent = None

    def _add_bond(self, bond):
        bond.index = -1
        self._bonds.append(bond)
        bond._parent = self

    def _remove_bond(self, bond):
        if bond in self._bonds:
            bond.index = -1
            self._bonds.remove(bond)
            bond._parent = None

    def _set_atoms(self, atoms):
        self._atoms = atoms
        for atom in atoms:
            atom._parent = self

    def _set_bonds(self, bonds):
        self._bonds = bonds
        for bond in bonds:
            bond._parent = self

    # region connections
    @property
    def _chain(self):
        return self._parent

    @property
    def _molecule(self):
        parent = self._parent
        if parent:
            return parent._molecule
        else:
            return None

    @property
    def _complex(self):
        parent = self._parent
        if parent:
            return parent._complex
        else:
            return None
    # endregion

    # copies the structure. If conformer_number is not None it will only copy that conformer's data
    def _shallow_copy(self, conformer_number=None):
        residue = _Residue._create()
        # molecular
        residue._type = self._type
        residue._serial = self._serial
        residue._name = self._name
        residue._secondary_structure = self._secondary_structure
        # rendering
        residue._ribboned = self._ribboned
        residue._ribbon_size = self._ribbon_size
        residue._ribbon_mode = self._ribbon_mode
        residue._ribbon_color = self._ribbon_color.copy()
        residue._labeled = self._labeled
        residue._label_text = self._label_text
        residue._ignored_alt_locs = self._ignored_alt_locs[:]
        return residue

    def _deep_copy(self, conformer_number=None):
        return _helpers._copy._deep_copy_residue(self, conformer_number)
