import nanome
from nanome.util import Vector3, Color
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
        self._polar_hydrogen = False
        #Rendering
        #API
        self._selected = False
        self._atom_mode = _Atom.AtomRenderingMode.BallStick
        self._labeled = False
        self._label_text = ""
        self._atom_color = Color.Clear()
        self._atom_scale = 0.5
        self._surface_rendering = False
        self._surface_color = Color.Clear()
        self._surface_opacity = 1.0
        #No API
        self._display_mode = 0xFFFFFFFF
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
    
    @property
    def _atom_rendering(self):
        return self._display_mode & 1

    @_atom_rendering.setter
    def _atom_rendering(self, value):
        if value:
            self._display_mode |= 1
        else:
            self._display_mode &= 0xFFFFFFFE

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
    def _vdw_radius(self):
        if len(_Atom._vdw_radii) < 1:
            _Atom._fill_atom_table()
        if self._symbol in _Atom._vdw_radii:
            return _Atom._vdw_radii[self._symbol]
        #unknown type
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
        atom._polar_hydrogen = self._polar_hydrogen
        atom._formal_charge = self._formal_charge
        atom._partial_charge = self._partial_charge
        #Rendering
        #API
        atom._selected = self._selected
        atom._atom_mode = self._atom_mode
        atom._labeled = self._labeled
        atom._label_text = self._label_text
        atom._atom_color = self._atom_color.copy()
        atom._atom_scale = self._atom_scale
        atom._surface_rendering = self._surface_rendering
        atom._surface_color = self._surface_color.copy()
        atom._surface_opacity = self._surface_opacity
        #No API
        atom._display_mode = self._display_mode
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


    @classmethod
    def _fill_atom_table(cls):
        #From NanomeAtomTable.csv
        cls._vdw_radii = {}
        cls._vdw_radii["H"] = 1.1
        cls._vdw_radii["He"] = 1.4
        cls._vdw_radii["Li"] = 1.81
        cls._vdw_radii["Be"] = 1.53
        cls._vdw_radii["B"] = 1.92
        cls._vdw_radii["C"] = 1.7
        cls._vdw_radii["N"] = 1.55
        cls._vdw_radii["O"] = 1.52
        cls._vdw_radii["F"] = 1.47
        cls._vdw_radii["Ne"] = 1.54
        cls._vdw_radii["Na"] = 2.27
        cls._vdw_radii["Mg"] = 1.73
        cls._vdw_radii["Al"] = 1.84
        cls._vdw_radii["Si"] = 2.1
        cls._vdw_radii["P"] = 1.8
        cls._vdw_radii["S"] = 1.8
        cls._vdw_radii["Cl"] = 1.75
        cls._vdw_radii["Ar"] = 1.88
        cls._vdw_radii["K"] = 2.75
        cls._vdw_radii["Ca"] = 2.31
        cls._vdw_radii["Sc"] = 2.3
        cls._vdw_radii["Ti"] = 2.15
        cls._vdw_radii["V"] = 2.05
        cls._vdw_radii["Cr"] = 2.05
        cls._vdw_radii["Mn"] = 2.05
        cls._vdw_radii["Fe"] = 2.05
        cls._vdw_radii["Co"] = 2
        cls._vdw_radii["Ni"] = 2
        cls._vdw_radii["Cu"] = 2
        cls._vdw_radii["Zn"] = 2.1
        cls._vdw_radii["Ga"] = 1.87
        cls._vdw_radii["Ge"] = 2.11
        cls._vdw_radii["As"] = 1.85
        cls._vdw_radii["Se"] = 1.9
        cls._vdw_radii["Br"] = 1.83
        cls._vdw_radii["Kr"] = 2.02
        cls._vdw_radii["Rb"] = 3.03
        cls._vdw_radii["Sr"] = 2.49
        cls._vdw_radii["Y"] = 2.4
        cls._vdw_radii["Zr"] = 2.3
        cls._vdw_radii["Nb"] = 2.15
        cls._vdw_radii["Mo"] = 2.1
        cls._vdw_radii["Tc"] = 2.05
        cls._vdw_radii["Ru"] = 2.05
        cls._vdw_radii["Rh"] = 2
        cls._vdw_radii["Pd"] = 2.05
        cls._vdw_radii["Ag"] = 2.1
        cls._vdw_radii["Cd"] = 2.2
        cls._vdw_radii["In"] = 2.2
        cls._vdw_radii["Sn"] = 1.93
        cls._vdw_radii["Sb"] = 2.17
        cls._vdw_radii["Te"] = 2.06
        cls._vdw_radii["I"] = 1.98
        cls._vdw_radii["Xe"] = 2.16
        cls._vdw_radii["Cs"] = 3.43
        cls._vdw_radii["Ba"] = 2.68
        cls._vdw_radii["La"] = 2.5
        cls._vdw_radii["Ce"] = 2.48
        cls._vdw_radii["Pr"] = 2.47
        cls._vdw_radii["Nd"] = 2.45
        cls._vdw_radii["Pm"] = 2.43
        cls._vdw_radii["Sm"] = 2.42
        cls._vdw_radii["Eu"] = 2.4
        cls._vdw_radii["Gd"] = 2.38
        cls._vdw_radii["Tb"] = 2.37
        cls._vdw_radii["Dy"] = 2.35
        cls._vdw_radii["Ho"] = 2.33
        cls._vdw_radii["Er"] = 2.32
        cls._vdw_radii["Tm"] = 2.3
        cls._vdw_radii["Yb"] = 2.28
        cls._vdw_radii["Lu"] = 2.27
        cls._vdw_radii["Hf"] = 2.25
        cls._vdw_radii["Ta"] = 2.2
        cls._vdw_radii["W"] = 2.1
        cls._vdw_radii["Re"] = 2.05
        cls._vdw_radii["Os"] = 2
        cls._vdw_radii["Ir"] = 2
        cls._vdw_radii["Pt"] = 2.05
        cls._vdw_radii["Au"] = 2.1
        cls._vdw_radii["Hg"] = 2.05
        cls._vdw_radii["Tl"] = 1.96
        cls._vdw_radii["Pb"] = 2.02
        cls._vdw_radii["Bi"] = 2.07
        cls._vdw_radii["Po"] = 1.97
        cls._vdw_radii["At"] = 2.02
        cls._vdw_radii["Rn"] = 2.2
        cls._vdw_radii["Fr"] = 3.48
        cls._vdw_radii["Ra"] = 2.83
        cls._vdw_radii["Ac"] = 2
        cls._vdw_radii["Th"] = 2.4
        cls._vdw_radii["Pa"] = 2
        cls._vdw_radii["U"] = 2.3
        cls._vdw_radii["Np"] = 2
        cls._vdw_radii["Pu"] = 2
        cls._vdw_radii["Am"] = 2
        cls._vdw_radii["Cm"] = 2
        cls._vdw_radii["Bk"] = 2
        cls._vdw_radii["Cf"] = 2
        cls._vdw_radii["Es"] = 2
        cls._vdw_radii["Fm"] = 2
        cls._vdw_radii["Md"] = 2
        cls._vdw_radii["No"] = 2
        cls._vdw_radii["Lr"] = 2
        cls._vdw_radii["Rf"] = 2
        cls._vdw_radii["Db"] = 2
        cls._vdw_radii["Sg"] = 2
        cls._vdw_radii["Bh"] = 2
        cls._vdw_radii["Hs"] = 2
        cls._vdw_radii["Mt"] = 2
        cls._vdw_radii["Ds"] = 2
        cls._vdw_radii["Rg"] = 2
        cls._vdw_radii["Cn"] = 2
        cls._vdw_radii["Nh"] = 2
        cls._vdw_radii["Fl"] = 2
        cls._vdw_radii["Mc"] = 2
        cls._vdw_radii["Lv"] = 2
        cls._vdw_radii["Ts"] = 2
        cls._vdw_radii["Og"] = 2
