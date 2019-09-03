import nanome
from nanome.util import Color, Logs
from . import _Base

class _Residue(_Base):
    RibbonMode = nanome.util.enums.RibbonMode
    SecondaryStructure = nanome.util.enums.SecondaryStructure

    @classmethod
    def _create(cls):
        return cls()
    
    def __init__(self):
        super(_Residue, self).__init__()
        #molecular
        self._type = "ARG" #RESIDUEDATA
        self._serial = 1
        self._name = "res"
        self._secondary_structure = _Residue.SecondaryStructure.Unknown
        #rendering
        self._ribboned = True
        self._ribbon_size = 1.0
        self._ribbon_mode = _Residue.RibbonMode.SecondaryStructure
        self._ribbon_color = Color.Clear()
        self._labeled = False
        self._label_text = ""
        #children
        self._atoms = []
        self._bonds = []
        #Parent pointers
        self._chain = None

    @property
    def _parent(self):
        return self._chain

    @_parent.setter
    def _parent(self, value):
        self._chain = value

    def _add_atom(self, atom):
        self._atoms.append(atom)
        atom._residue = self

    def _remove_atom(self, atom):
        atom.index = -1
        self._atoms.remove(atom)
        atom._residue = None
    
    def _add_bond(self, bond):
        bond.index = -1
        self._bonds.append(bond)
        bond._residue = self

    def _remove_bond(self, bond):
        bond.index = -1
        self._bonds.remove(bond)
        bond._residue = None
    
    def _set_atoms(self, atoms):
        self._atoms = atoms
        for atom in atoms:
            atom._residue = self

    def _set_bonds(self, bonds):
        self._bonds = bonds
        for bond in bonds:
            bond._residue = self