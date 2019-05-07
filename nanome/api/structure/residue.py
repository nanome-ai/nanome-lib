from nanome._internal._structure._residue import _Residue
from . import Base

class Residue(_Residue, Base):
    def __init__(self):
        super(Residue, self).__init__()
        self.rendering = self._rendering
        self.molecular = self._molecular

    def add_atom(self, atom):
        self._atoms.append(atom)

    def remove_atom(self, atom):
        self._atoms.remove(atom)
    
    def add_bond(self, bond):
        self._bonds.append(bond)

    def remove_bond(self, bond):
        self._bonds.remove(bond)

    class Rendering(_Residue.Rendering):
        @property
        def modified(self):
            return self._modified
        @modified.setter
        def modified(self, value):
            self._modified = value
        
        @property
        def ribboned(self):
            return self._ribboned
        @ribboned.setter
        def ribboned(self, value):
            self._ribboned = value
        
        @property
        def ribbon_size(self):
            return self._ribbon_size
        @ribbon_size.setter
        def ribbon_size(self, value):
            self._ribbon_size = value
        
        @property
        def ribbon_mode(self):
            return self._ribbon_mode
        @ribbon_mode.setter
        def ribbon_mode(self, value):
            self._ribbon_mode = value
        
        @property
        def ribbon_color(self):
            return self._ribbon_color
        @ribbon_color.setter
        def ribbon_color(self, value):
            self._ribbon_color = value
    _Residue.Rendering._create = Rendering

    class Molecular(_Residue.Molecular):
        @property
        def type(self):
            return self._type
        @type.setter
        def type(self, value):
            self._type = value
        
        @property
        def serial(self):
            return self._serial
        @serial.setter
        def serial(self, value):
            self._serial = value
        
        @property
        def name(self):
            return self._name
        @name.setter
        def name(self, value):
            self._name = value

        @property
        def secondary_structure(self):
            return self._secondary_structure
        @secondary_structure.setter
        def secondary_structure(self, value):
            self._secondary_structure = value
    _Residue.Molecular._create = Molecular

    @property
    def atoms(self):
        for atom in self._atoms:
            yield atom

    @property
    def bonds(self):
        for bond in self._bonds:
            yield bond

_Residue._create = Residue