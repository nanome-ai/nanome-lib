import nanome
from nanome.util import Vector3, Color
from nanome.util.logs import Logs
from . import _Base


class _Atom(_Base):
    AtomRenderingMode = nanome.util.enums.AtomRenderingMode
    _vdw_radii = {}

    @classmethod
    def _create(cls):
        _fill_atom_table()
        return cls()

    _atom_count = 0

    def __init__(self):
        super(_Atom, self).__init__()
        # Molecular
        self._symbol = "C"
        self._serial = 1
        self._name = "default"
        self._is_het = False
        self._atom_type = {}
        self._formal_charge = 0
        self._partial_charge = 0.0
        self._occupancy = 0.0
        self._bfactor = 0.0
        self._acceptor = False
        self._donor = False
        self._polar_hydrogen = False
        self._alt_loc = "."
        # Rendering
        # API
        self._selected = False
        self._atom_mode = _Atom.AtomRenderingMode.BallStick
        self._labeled = False
        self._label_text = ""
        self._atom_color = Color.Clear()
        self._atom_scale = 0.5
        self._surface_rendering = False
        self._surface_color = Color.Clear()
        self._surface_opacity = 1.0
        # No API
        self._display_mode = 0xFFFFFFFF
        self._hydrogened = True
        self._watered = True
        self._het_atomed = True
        self._het_surfaced = True
        # conformer
        self._positions = [Vector3()]
        self._in_conformer = [True]
        # internal
        self._unique_identifier = _Atom._atom_count
        self._bonds = []
        self._parent = None
        _Atom._atom_count += 1

    @property
    def _atom_rendering(self):
        return self._display_mode & 1

    @_atom_rendering.setter
    def _atom_rendering(self, value):
        if value:
            self._display_mode |= 1
        else:
            self._display_mode &= 0xFFFFFFFE

    # region connections
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
    # endregion

    # region conformer stuff
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
    def _vdw_radius(self):
        if len(_Atom._vdw_radii) < 1:
            _Atom._fill_atom_table()
        atomSymbolLower = self._symbol.lower()
        if atomSymbolLower in _Atom._vdw_radii:
            return _Atom._vdw_radii[atomSymbolLower]
        # unknown type
        Logs.warning("Unknown atom type '" + atomSymbolLower + "'")
        return 0.0

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
            self._in_conformer.extend([self._in_conformer[-1]] * (extension))
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
        src = src + 1 if src > dest else src
        del self._in_conformer[src]
        del self._positions[src]

    def _delete_conformer(self, index):
        del self._positions[index]
        del self._in_conformer[index]

    def _copy_conformer(self, src, index=None):
        if index is None:
            index = src
        value = self._in_conformer[src]
        self._in_conformer.insert(index, value)
        value = self._positions[src].get_copy()
        self._positions.insert(index, value)
    # endregion

    # copies the structure. If conformer_number is not None it will only copy that conformer's data..
    def _shallow_copy(self, conformer_number=None):
        atom = _Atom._create()
        atom._symbol = self._symbol
        atom._serial = self._serial
        atom._name = self._name
        atom._is_het = self._is_het
        atom._atom_type = self._atom_type
        # No API
        atom._occupancy = self._occupancy
        atom._bfactor = self._bfactor
        atom._acceptor = self._acceptor
        atom._donor = self._donor
        atom._polar_hydrogen = self._polar_hydrogen
        atom._formal_charge = self._formal_charge
        atom._partial_charge = self._partial_charge
        # Rendering
        # API
        atom._selected = self._selected
        atom._atom_mode = self._atom_mode
        atom._labeled = self._labeled
        atom._label_text = self._label_text
        atom._atom_color = self._atom_color.copy()
        atom._atom_scale = self._atom_scale
        atom._surface_rendering = self._surface_rendering
        atom._surface_color = self._surface_color.copy()
        atom._surface_opacity = self._surface_opacity
        # No API
        atom._display_mode = self._display_mode
        atom._hydrogened = self._hydrogened
        atom._watered = self._watered
        atom._het_atomed = self._het_atomed
        atom._het_surfaced = self._het_surfaced
        # conformer
        if conformer_number == None:
            atom._positions = [position.get_copy() for position in self._positions]
            atom._in_conformer = list(self._in_conformer)
        else:
            atom._position = self._positions[conformer_number]
            #atom._exists = self._in_conformer[conformer_number]
        return atom

    @classmethod
    def _fill_atom_table(cls):
        # From NanomeAtomTable.csv
        cls._vdw_radii = {}
        cls._vdw_radii["h"] = 1.1
        cls._vdw_radii["he"] = 1.4
        cls._vdw_radii["li"] = 1.81
        cls._vdw_radii["be"] = 1.53
        cls._vdw_radii["b"] = 1.92
        cls._vdw_radii["c"] = 1.7
        cls._vdw_radii["n"] = 1.55
        cls._vdw_radii["o"] = 1.52
        cls._vdw_radii["f"] = 1.47
        cls._vdw_radii["ne"] = 1.54
        cls._vdw_radii["na"] = 2.27
        cls._vdw_radii["mg"] = 1.73
        cls._vdw_radii["al"] = 1.84
        cls._vdw_radii["si"] = 2.1
        cls._vdw_radii["p"] = 1.8
        cls._vdw_radii["s"] = 1.8
        cls._vdw_radii["cl"] = 1.75
        cls._vdw_radii["ar"] = 1.88
        cls._vdw_radii["k"] = 2.75
        cls._vdw_radii["ca"] = 2.31
        cls._vdw_radii["sc"] = 2.3
        cls._vdw_radii["ti"] = 2.15
        cls._vdw_radii["v"] = 2.05
        cls._vdw_radii["cr"] = 2.05
        cls._vdw_radii["mn"] = 2.05
        cls._vdw_radii["fe"] = 2.05
        cls._vdw_radii["co"] = 2
        cls._vdw_radii["ni"] = 2
        cls._vdw_radii["cu"] = 2
        cls._vdw_radii["zn"] = 2.1
        cls._vdw_radii["ga"] = 1.87
        cls._vdw_radii["ge"] = 2.11
        cls._vdw_radii["as"] = 1.85
        cls._vdw_radii["se"] = 1.9
        cls._vdw_radii["br"] = 1.83
        cls._vdw_radii["kr"] = 2.02
        cls._vdw_radii["rb"] = 3.03
        cls._vdw_radii["sr"] = 2.49
        cls._vdw_radii["y"] = 2.4
        cls._vdw_radii["zr"] = 2.3
        cls._vdw_radii["nb"] = 2.15
        cls._vdw_radii["mo"] = 2.1
        cls._vdw_radii["tc"] = 2.05
        cls._vdw_radii["ru"] = 2.05
        cls._vdw_radii["rh"] = 2
        cls._vdw_radii["pd"] = 2.05
        cls._vdw_radii["ag"] = 2.1
        cls._vdw_radii["cd"] = 2.2
        cls._vdw_radii["in"] = 2.2
        cls._vdw_radii["sn"] = 1.93
        cls._vdw_radii["sb"] = 2.17
        cls._vdw_radii["te"] = 2.06
        cls._vdw_radii["i"] = 1.98
        cls._vdw_radii["xe"] = 2.16
        cls._vdw_radii["cs"] = 3.43
        cls._vdw_radii["ba"] = 2.68
        cls._vdw_radii["la"] = 2.5
        cls._vdw_radii["ce"] = 2.48
        cls._vdw_radii["pr"] = 2.47
        cls._vdw_radii["nd"] = 2.45
        cls._vdw_radii["pm"] = 2.43
        cls._vdw_radii["sm"] = 2.42
        cls._vdw_radii["eu"] = 2.4
        cls._vdw_radii["gd"] = 2.38
        cls._vdw_radii["tb"] = 2.37
        cls._vdw_radii["dy"] = 2.35
        cls._vdw_radii["ho"] = 2.33
        cls._vdw_radii["er"] = 2.32
        cls._vdw_radii["tm"] = 2.3
        cls._vdw_radii["yb"] = 2.28
        cls._vdw_radii["lu"] = 2.27
        cls._vdw_radii["hf"] = 2.25
        cls._vdw_radii["ta"] = 2.2
        cls._vdw_radii["w"] = 2.1
        cls._vdw_radii["re"] = 2.05
        cls._vdw_radii["os"] = 2
        cls._vdw_radii["ir"] = 2
        cls._vdw_radii["pt"] = 2.05
        cls._vdw_radii["au"] = 2.1
        cls._vdw_radii["hg"] = 2.05
        cls._vdw_radii["tl"] = 1.96
        cls._vdw_radii["pb"] = 2.02
        cls._vdw_radii["bi"] = 2.07
        cls._vdw_radii["po"] = 1.97
        cls._vdw_radii["at"] = 2.02
        cls._vdw_radii["rn"] = 2.2
        cls._vdw_radii["fr"] = 3.48
        cls._vdw_radii["ra"] = 2.83
        cls._vdw_radii["ac"] = 2
        cls._vdw_radii["th"] = 2.4
        cls._vdw_radii["pa"] = 2
        cls._vdw_radii["u"] = 2.3
        cls._vdw_radii["np"] = 2
        cls._vdw_radii["pu"] = 2
        cls._vdw_radii["am"] = 2
        cls._vdw_radii["cm"] = 2
        cls._vdw_radii["bk"] = 2
        cls._vdw_radii["cf"] = 2
        cls._vdw_radii["es"] = 2
        cls._vdw_radii["fm"] = 2
        cls._vdw_radii["md"] = 2
        cls._vdw_radii["no"] = 2
        cls._vdw_radii["lr"] = 2
        cls._vdw_radii["rf"] = 2
        cls._vdw_radii["db"] = 2
        cls._vdw_radii["sg"] = 2
        cls._vdw_radii["bh"] = 2
        cls._vdw_radii["hs"] = 2
        cls._vdw_radii["mt"] = 2
        cls._vdw_radii["ds"] = 2
        cls._vdw_radii["rg"] = 2
        cls._vdw_radii["cn"] = 2
        cls._vdw_radii["nh"] = 2
        cls._vdw_radii["fl"] = 2
        cls._vdw_radii["mc"] = 2
        cls._vdw_radii["lv"] = 2
        cls._vdw_radii["ts"] = 2
        cls._vdw_radii["og"] = 2
