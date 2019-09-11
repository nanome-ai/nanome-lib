import nanome
from nanome.util import Vector3, Color
from . import _Base

class _Atom(_Base):
    AtomRenderingMode = nanome.util.enums.AtomRenderingMode

    @classmethod
    def _create(cls):
        return cls()

    _atom_count = 0
    def __init__(self):
        super(_Atom, self).__init__()
        #Molecular
        self._symbol = "Carbon"
        self._serial = 1
        self._name = "default"
        self._is_het = False
        #No API
        self._occupancy = 0.0
        self._bfactor = 0.0
        self._acceptor = False
        self._donor = False
        #Rendering
        #API
        self._selected = False
        self._atom_mode = _Atom.AtomRenderingMode.BallStick
        self._labeled = False
        self._label_text = ""
        self._atom_rendering = True
        self._atom_color = Color.Clear()
        self._atom_scale = 0.5
        self._surface_rendering = False
        self._surface_color = Color.Clear()
        self._surface_opacity = 1.0
        #No API
        self._hydrogened = True
        self._watered = True
        self._het_atomed = True
        self._het_surfaced = True
        #conformer
        self._positions = [Vector3()]
        self._exists = [True]
        #internal
        self._unique_identifier = _Atom._atom_count
        self._bonds = []
        _Atom._atom_count += 1
    
    #region connections
    @property
    def _residue(self):
        return self._parent

    @property
    def _chain(self):
        if self._parent:
            return self._parent._chain
        else:
            return None

    @property
    def _molecule(self):
        if self._parent:
            return self._parent._molecule
        else:
            return None

    @property
    def _complex(self):
        if self._parent:
            return self._parent._complex
        else:
            return None

    @property
    def _current_conformer(self):
        if self._molecule != None:
            return self._molecule._current_conformer
        else:
            return 0

    @property
    def _conformer_count(self):
        if self._molecule != None:
            return self._molecule._conformer_count
        else:
            return 1

    def _set_positions(self, positions):
        if self._molecule != None:
            if len(positions) != self._conformer_count:
                nanome.util.Logs.error("Molecule contains", self._conformer_count, "but atom contains", len(positions), "conformers.")
        self._positions = positions
    
    @property
    def _position(self):
        return self._positions[self._current_conformer]
    
    @_position.setter
    def _position(self, value):
        self._positions[self._current_conformer] = value
    #endregion