from nanome._internal._structure._atom import _Atom
from nanome.util import Vector3, Color
from . import Base

class Atom(_Atom, Base):
    """    
    Represents an Atom

    :ivar rendering: Describes how the Atom should be rendered
    :vartype rendering: :class:`~nanome.api.structure.atom.Atom.Rendering`
    :ivar molecular: Contains molecular informations about the Atom
    :vartype molecular: :class:`~nanome.api.structure.atom.Atom.Molecular`
    """

    def __init__(self):
        super(Atom, self).__init__()
        self.rendering = self._rendering
        self.molecular = self._molecular

    class Rendering(_Atom.Rendering):
        def set_visible(self, value):
            self._atomed = value
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
    _Atom.Rendering._create = Rendering

    class Molecular(_Atom.Molecular):
        @property
        def symbol(self):
            return self._symbol
        @symbol.setter
        def symbol(self, value):
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
            self._name = value

        @property
        def position(self):
            return self._position
        @position.setter
        def position(self, value):
            self._position = value

        @property
        def is_het(self):
            return self._is_het
        @is_het.setter
        def is_het(self, value):
            self._is_het = value
    _Atom.Molecular._create = Molecular

_Atom._create = Atom