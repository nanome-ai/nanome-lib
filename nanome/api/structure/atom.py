import nanome
from nanome._internal._structure._atom import _Atom
from nanome.util import Vector3, Color, Logs
from . import Base

class Atom(_Atom, Base):
    """    
    Represents an Atom

    """
    AtomRenderingMode = nanome.util.enums.AtomRenderingMode

    def __init__(self):
        super(Atom, self).__init__()
        self._rendering = Atom.Rendering(self)
        self._molecular = Atom.Molecular(self)

    #region connections
    @property
    def bonds(self):
        for bond in self._bonds:
            yield bond

    @property
    def residue(self):
        return self._residue

    @property
    def chain(self):
        return self._chain

    @property
    def molecule(self):
        return self._molecule

    @property
    def complex(self):
        return self._complex
    #endregion

    #region all fields
    def set_visible(self, value):
        self._atom_rendering = value
        self._hydrogened = value
        self._watered = value
        self._hetatomed = value

    @property
    def selected(self):
        return self._selected
    @selected.setter
    def selected(self, value):
        self._selected = value
    
    @property
    def atom_mode(self):
        return self._atom_mode
    @atom_mode.setter
    def atom_mode(self, value):
        self._atom_mode = value
    
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
    def atom_rendering(self):
        return self._atom_rendering
    @atom_rendering.setter
    def atom_rendering(self, value):
        self._atom_rendering = value
    
    @property
    def atom_color(self):
        return self._atom_color
    @atom_color.setter
    def atom_color(self, value):
        self._atom_color = value

    @property
    def atom_scale(self):
        return self._atom_scale
    @atom_scale.setter
    def atom_scale(self, value):
        self._atom_scale = value
    
    @property
    def surface_rendering(self):
        return self._surface_rendering
    @surface_rendering.setter
    def surface_rendering(self, value):
        self._surface_rendering = value
    
    @property
    def surface_color(self):
        return self._surface_color
    @surface_color.setter
    def surface_color(self, value):
        self._surface_color = value
    
    @property
    def surface_opacity(self):
        return self._surface_opacity
    @surface_opacity.setter
    def surface_opacity(self, value):
        self._surface_opacity = value

    @property
    def symbol(self):
        return self._symbol
    @symbol.setter
    def symbol(self, value):
        if type(value) is not str:
            value = str(value)
        self._symbol = value

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
    def position(self):
        return self._position
    @position.setter
    def position(self, value):
        self._position = value

    @property
    def exists(self):
        return self._exists
    
    @exists.setter
    def exists(self, value):
        self._exists = value

    @property
    def is_het(self):
        return self._is_het
    @is_het.setter
    def is_het(self, value):
        self._is_het = value
    #endregion

    #region conformer stuff
    @property
    def current_conformer(self):
        return self._current_conformer

    @property
    def conformer_count(self):
        return self._conformer_count

    @property
    def positions(self):
        return self._positions
    
    @positions.setter
    def positions(self, value):
        if self.molecule != None:
            if len(value) != self.conformer_count:
                raise ValueError("Length of positions must match the conformer count of the parent molecule.")
        self._positions = value

    @property
    def in_conformer(self):
        return self._in_conformer
    
    @in_conformer.setter
    def in_conformer(self, value):
        if self.molecule != None:
            if len(value) != self.conformer_count:
                raise ValueError("Length of in_conformer must match the conformer count of the parent molecule.")
        self._in_conformer = value

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

        def set_visible(self, value):
            self.parent.atom_rendering = value
            self.parent.hydrogened = value
            self.parent.watered = value
            self.parent.hetatomed = value

        @property
        def selected(self):
            return self.parent.selected
        @selected.setter
        def selected(self, value):
            self.parent.selected = value
        
        @property
        def atom_mode(self):
            return self.parent.atom_mode
        @atom_mode.setter
        def atom_mode(self, value):
            self.parent.atom_mode = value
        
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

        @property
        def atom_rendering(self):
            return self.parent.atom_rendering
        @atom_rendering.setter
        def atom_rendering(self, value):
            self.parent.atom_rendering = value
        
        @property
        def atom_color(self):
            return self.parent.atom_color
        @atom_color.setter
        def atom_color(self, value):
            self.parent.atom_color = value
        
        @property
        def surface_rendering(self):
            return self.parent.surface_rendering
        @surface_rendering.setter
        def surface_rendering(self, value):
            self.parent.surface_rendering = value
        
        @property
        def surface_color(self):
            return self.parent.surface_color
        @surface_color.setter
        def surface_color(self, value):
            self.parent.surface_color = value
        
        @property
        def surface_opacity(self):
            return self.parent.surface_opacity
        @surface_opacity.setter
        def surface_opacity(self, value):
            self.parent.surface_opacity = value

    class Molecular(object):
        def __init__(self, parent):
            self.parent = parent

        @property
        def symbol(self):
            return self.parent.symbol
        @symbol.setter
        def symbol(self, value):
            self.parent.symbol = value

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
        def position(self):
            return self.parent.position
        @position.setter
        def position(self, value):
            self.parent.position = value

        @property
        def is_het(self):
            return self.parent.is_het
        @is_het.setter
        def is_het(self, value):
            self.parent.is_het = value
    #endregion
_Atom._create = Atom