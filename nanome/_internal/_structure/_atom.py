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
        self._name = "default"
        self._position = Vector3()
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
        self._surface_rendering = False
        self._surface_color = Color.Clear()
        self._surface_opacity = 1.0
        #No API
        self._hydrogened = True
        self._watered = True
        self._het_atomed = True
        self._het_surfaced = True
        #internal
        self._unique_identifier = _Atom._atom_count
        self._bonds = []
        _Atom._atom_count += 1