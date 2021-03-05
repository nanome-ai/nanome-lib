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
        self._symbol = "C"
        self._serial = 1
        self._name = "default"
        self._is_het = False
        self._atom_type = {}
        self._formal_charge = 0
        self._partial_charge = 0.0
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
        self._in_conformer = [True]
        #internal
        self._unique_identifier = _Atom._atom_count
        self._bonds = []
        self._parent = None
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
    #endregion

    #region conformer stuff
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

    @property
    def _position(self):
        return self._positions[self._current_conformer]
    
    @_position.setter
    def _position(self, value):
        self._positions[self._current_conformer] = value

    @property
    def _exists(self):
        return self._in_conformer[self._current_conformer]
    
    @_exists.setter
    def _exists(self, value):
        self._in_conformer[self._current_conformer] = value

    def _resize_conformer(self, new_size):
        curr_size = len(self._in_conformer)
        if new_size > curr_size:
            extension = new_size - curr_size
            self._in_conformer.extend([self._in_conformer[-1]]*(extension))
            copy_val = self._positions[-1]
            self._positions.extend([copy_val.get_copy() for i in range(extension)])
        else:
            self._in_conformer = self._in_conformer[:new_size]
            self._positions = self._positions[:new_size]

    def _move_conformer(self, src, dest):
        temp = self._in_conformer[src]
        self._in_conformer.insert(dest, temp)
        temp = self._positions[src]
        self._positions.insert(dest, temp)
        src = src + 1 if src>dest else src
        del self._in_conformer[src]
        del self._positions[src]

    def _delete_conformer(self, index):
        del self._positions[index]
        del self._in_conformer[index]

    def _copy_conformer(self, src, index= None):
        if index is None:
            index = src
        value = self._in_conformer[src]
        self._in_conformer.insert(index, value)
        value = self._positions[src].get_copy()
        self._positions.insert(index, value)
    #endregion

    #copies the structure. If conformer_number is not None it will only copy that conformer's data..
    def _shallow_copy(self, conformer_number = None):
        atom = _Atom._create()
        atom._symbol = self._symbol
        atom._serial = self._serial
        atom._name = self._name
        atom._is_het = self._is_het
        atom._atom_type = self._atom_type
        #No API
        atom._occupancy = self._occupancy
        atom._bfactor = self._bfactor
        atom._acceptor = self._acceptor
        atom._donor = self._donor
        atom._formal_charge = self._formal_charge
        atom._partial_charge = self._partial_charge
        #Rendering
        #API
        atom._selected = self._selected
        atom._atom_mode = self._atom_mode
        atom._labeled = self._labeled
        atom._label_text = self._label_text
        atom._atom_rendering = self._atom_rendering
        atom._atom_color = self._atom_color.copy()
        atom._atom_scale = self._atom_scale
        atom._surface_rendering = self._surface_rendering
        atom._surface_color = self._surface_color.copy()
        atom._surface_opacity = self._surface_opacity
        #No API
        atom._hydrogened = self._hydrogened
        atom._watered = self._watered
        atom._het_atomed = self._het_atomed
        atom._het_surfaced = self._het_surfaced
        #conformer
        if conformer_number == None:
            atom._positions = [position.get_copy() for position in self._positions]
            atom._in_conformer = list(self._in_conformer)
        else:
            atom._position = self._positions[conformer_number]
            #atom._exists = self._in_conformer[conformer_number]
        return atom
