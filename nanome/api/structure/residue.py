import nanome
from nanome.util import Logs
from nanome._internal._structure._residue import _Residue
from . import Base

class Residue(_Residue, Base):

    RibbonMode = nanome.util.enums.RibbonMode
    SecondaryStructure = nanome.util.enums.SecondaryStructure

    def __init__(self):
        super(Residue, self).__init__()
        self._rendering = Residue.Rendering(self)
        self._molecular = Residue.Molecular(self)

    def add_atom(self, atom):
        if (self.molecule != None and len(atom.in_conformer) > self.molecule.conformer_count):
            raise ValueError("Length of in_conformer must match the conformer count of the parent molecule.")
        if (self.molecule != None and len(atom.positions) > self.molecule.conformer_count):
            raise ValueError("Length of positions must match the conformer count of the parent molecule.")
        atom.index = -1
        self._add_atom(atom)

    def remove_atom(self, atom):
        atom.index = -1
        self._remove_atom(atom)
    
    def add_bond(self, bond):
        if (self.molecule != None and len(bond.in_conformer) > self.molecule.conformer_count):
            raise ValueError("Length of in_conformer must match the conformer count of the parent molecule.")
        if (self.molecule != None and len(bond.kinds) > self.molecule.conformer_count):
            raise ValueError("Length of kinds must match the conformer count of the parent molecule.")
        bond.index = -1
        self._add_bond(bond)

    def remove_bond(self, bond):
        bond.index = -1
        self._remove_bond(bond)

    #region Generators
    @property
    def atoms(self):
        for atom in self._atoms:
            yield atom

    @property
    def bonds(self):
        for bond in self._bonds:
            yield bond
    #endregion

    #region connections
    @property
    def chain(self):
        return self._chain

    @property
    def molecule(self):
        return  self._molecule

    @property
    def complex(self):
        return self._complex
    #endregion

    #region all fields
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

    @property
    def labeled(self):
        return self._labeled
    @labeled.setter
    def labeled(self, value):
        self._labeled = value

    @property
    def label_text(self):
        return self._label_text
    @label_text.setter
    def label_text(self, value):
        if type(value) is not str:
            value = str(value)
        self._label_text = value

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
        if type(value) is not str:
            value = str(value)
        self._name = value

    @property
    def secondary_structure(self):
        return self._secondary_structure
    @secondary_structure.setter
    def secondary_structure(self, value):
        self._secondary_structure = value
    #endregion

    #region deprecated
    @property
    @Logs.deprecated()
    def rendering(self):
        return self._rendering

    @property
    @Logs.deprecated()
    def molecular(self):
        return self._molecular

    class Rendering(object):
        def __init__(self, parent):
            self.parent = parent

        @property
        def ribboned(self):
            return self.parent.ribboned
        @ribboned.setter
        def ribboned(self, value):
            self.parent.ribboned = value
        
        @property
        def ribbon_size(self):
            return self.parent.ribbon_size
        @ribbon_size.setter
        def ribbon_size(self, value):
            self.parent.ribbon_size = value
        
        @property
        def ribbon_mode(self):
            return self.parent.ribbon_mode
        @ribbon_mode.setter
        def ribbon_mode(self, value):
            self.parent.ribbon_mode = value
        
        @property
        def ribbon_color(self):
            return self.parent.ribbon_color
        @ribbon_color.setter
        def ribbon_color(self, value):
            self.parent.ribbon_color = value

        @property
        def labeled(self):
            return self.parent.labeled
        @labeled.setter
        def labeled(self, value):
            self.parent.labeled = value

        @property
        def label_text(self):
            return self.parent.label_text
        @label_text.setter
        def label_text(self, value):
            self.parent.label_text = value

    class Molecular(object):
        def __init__(self, parent):
            self.parent = parent

        @property
        def type(self):
            return self.parent.type
        @type.setter
        def type(self, value):
            self.parent.type = value
        
        @property
        def serial(self):
            return self.parent.serial
        @serial.setter
        def serial(self, value):
            self.parent.serial = value
        
        @property
        def name(self):
            return self.parent.name
        @name.setter
        def name(self, value):
            self.parent.name = value

        @property
        def secondary_structure(self):
            return self.parent.secondary_structure
        @secondary_structure.setter
        def secondary_structure(self, value):
            self.parent.secondary_structure = value
    #endregion
_Residue._create = Residue