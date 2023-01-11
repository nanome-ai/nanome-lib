import copy
from nanome._internal.decorators import deprecated
from . import helpers
import logging

logger = logging.getLogger(__name__)


class _Base(object):
    def __init__(self):
        self._index = -1
        self._parent = None


class _Atom(_Base):
    _vdw_radii = {}

    @classmethod
    def _create(cls):
        cls._fill_atom_table()
        return cls()

    _atom_count = 0

    def __init__(self):
        from nanome.util import Vector3, Color, enums
        super(_Atom, self).__init__()
        self.AtomRenderingMode = enums.AtomRenderingMode
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
        self._atom_mode = enums.AtomRenderingMode.BallStick
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
        logger.warning("Unknown atom type '" + atomSymbolLower + "'")
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
            self._positions.extend([copy_val.get_copy()
                                    for i in range(extension)])
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
            atom._positions = [position.get_copy()
                               for position in self._positions]
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


__metaclass__ = type


class _Bond(_Base):

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        from nanome.util import enums
        super(_Bond, self).__init__()
        self.Kind = enums.Kind
        self.__atom1 = None
        self.__atom2 = None
        self._parent = None

        self._in_conformer = [True]
        self._kinds = [enums.Kind.CovalentSingle]

    @property
    def _atom1(self):
        return self.__atom1

    @_atom1.setter
    def _atom1(self, value):
        if self.__atom1 is not None:
            try:
                self.__atom1._bonds.remove(self)
            except ValueError:
                pass
        if value is not None:
            value._bonds.append(self)
        self.__atom1 = value

    @property
    def _atom2(self):
        return self.__atom2

    @_atom2.setter
    def _atom2(self, value):
        if self.__atom2 is not None:
            try:
                self.__atom2._bonds.remove(self)
            except ValueError:
                pass
        if value is not None:
            value._bonds.append(self)
        self.__atom2 = value

    # region connections
    @property
    def _residue(self):
        return self._parent

    @property
    def _chain(self):
        parent = self._parent
        if parent:
            return parent._chain
        else:
            return None

    @property
    def _molecule(self):
        parent = self._parent
        if parent:
            return parent._molecule
        else:
            return None

    @property
    def _complex(self):
        parent = self._parent
        if parent:
            return parent._complex
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

    def _resize_conformer(self, new_size):
        curr_size = len(self._kinds)
        if new_size > curr_size:
            extension = new_size - curr_size
            self._kinds.extend([self._kinds[-1]] * (extension))
            self._in_conformer.extend([self._in_conformer[-1]] * (extension))
        else:
            self._kinds = self._kinds[:new_size]
            self._in_conformer = self._in_conformer[:new_size]

    def _move_conformer(self, src, dest):
        temp = self._in_conformer[src]
        self._in_conformer.insert(dest, temp)
        temp = self._kinds[src]
        self._kinds.insert(dest, temp)
        src = src + 1 if src > dest else src
        del self._in_conformer[src]
        del self._kinds[src]

    def _delete_conformer(self, index):
        del self._kinds[index]
        del self._in_conformer[index]

    def _copy_conformer(self, src, index=None):
        if index is None:
            index = src
        value = self._in_conformer[src]
        self._in_conformer.insert(index, value)
        value = self._kinds[src]
        self._kinds.insert(index, value)

    @property
    def _kind(self):
        return self._kinds[self._current_conformer]

    @_kind.setter
    def _kind(self, value):
        self._kinds[self._current_conformer] = value

    @property
    def _exists(self):
        return self._in_conformer[self._current_conformer]

    @_exists.setter
    def _exists(self, value):
        self._in_conformer[self._current_conformer] = value
    # endregion

    # copies the structure. If conformer_number is not None it will only copy that conformer's data.
    def _shallow_copy(self, conformer_number=None):
        bond = _Bond._create()
        if conformer_number == None:
            bond._in_conformer = list(self._in_conformer)
            bond._kinds = list(self._kinds)
        else:
            bond._kind = self._kinds[conformer_number]
            # bond._exists = self._in_conformer[conformer_number]
        return bond


class _Chain(_Base):
    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_Chain, self).__init__()
        self._name = "chain"
        self._residues = []

    def _add_residue(self, residue):
        self._residues.append(residue)
        residue._parent = self

    def _remove_residue(self, residue):
        if residue in self._residues:
            self._residues.remove(residue)
            residue._parent = None

    def _set_residues(self, residues):
        self._residues = residues
        for residue in residues:
            residue._parent = self

    # region connections
    @property
    def _molecule(self):
        return self._parent

    @property
    def _complex(self):
        if self._parent:
            return self._parent._complex
        else:
            return None
    # endregion

        # copies the structure. If conformer_number is not None it will only copy that conformer's data
    def _shallow_copy(self, conformer_number=None):
        chain = _Chain._create()
        chain._name = self._name
        return chain

    def _deep_copy(self, conformer_number=None):
        return helpers.copy._deep_copy_chain(self, conformer_number)


class _Complex(_Base):

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        from nanome.util import Vector3, Quaternion
        super(_Complex, self).__init__()
        # Molecular
        self._name = "complex"
        self._index_tag = 0
        self._split_tag = ""
        self._remarks = {}
        # Rendering
        self._boxed = False
        self._locked = False
        self._visible = True
        self._computing = False
        self._current_frame = 0
        self._selected = False  # selected on live
        self._surface_dirty = False
        self._surface_refresh_rate = -1.0  # Not used yet, future auto surface refresh
        self._box_label = ""
        # Transform
        self._position = Vector3(0, 0, 0)
        self._rotation = Quaternion(0, 0, 0, 0)
        self._molecules = []
        self._parent = None

    def _add_molecule(self, molecule):
        self._molecules.append(molecule)
        molecule._parent = self

    def _remove_molecule(self, molecule):
        if molecule in self._molecules:
            self._molecules.remove(molecule)
            molecule._parent = None

    def _set_molecules(self, molecules):
        self._molecules = molecules
        for molecule in molecules:
            molecule._parent = self

    @deprecated()
    def get_atom_iterator(self):
        iterator = _Complex.AtomIterator(self)
        return iter(iterator)

    class AtomIterator(object):
        def __init__(self, complex):
            self._complex = complex

        def __iter__(self):
            self._molecule = iter(self._complex._molecules)
            self._update_iter()
            return self

        def __next__(self):
            while True:
                try:
                    return next(self._chainAtom)
                except StopIteration:
                    self._update_iter()

        def _update_iter(self):
            while True:
                molecule = next(self._molecule)
                try:
                    self._chainAtom = molecule.get_atom_iterator()
                    break
                except StopIteration:
                    pass

    def _shallow_copy(self, target=None):
        if target == None:
            complex = _Complex._create()
        else:
            complex = target
        # Molecular
        complex._name = self._name
        complex._index_tag = self._index_tag
        complex._split_tag = self._split_tag
        complex._remarks = self._remarks
        # Rendering
        complex._boxed = self._boxed
        complex._locked = self._locked
        complex._visible = self._visible
        complex._computing = self._computing
        complex._current_frame = self._current_frame
        complex._selected = self._selected
        complex._surface_dirty = self._surface_dirty
        complex._surface_refresh_rate = self._surface_refresh_rate
        complex._box_label = self._box_label
        # Transform
        complex._position = self._position.get_copy()
        complex._rotation = self._rotation.get_copy()
        return complex

    def _deep_copy(self):
        return helpers.copy._deep_copy_complex(self)

    def _convert_to_conformers(self, force_conformers=None):
        result = helpers.conformer_helper.convert_to_conformers(self, None)
        return result

    def _convert_to_frames(self, old_to_new_atoms=None):
        result = helpers.conformer_helper.convert_to_frames(
            self, old_to_new_atoms)
        return result


class _Molecule(_Base):
    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_Molecule, self).__init__()
        self._chains = []
        self._parent = None
        # conformers
        self._current_conformer = 0
        self.__conformer_count = 1
        self._names = [""]
        self._associateds = [dict()]

    def _add_chain(self, chain):
        self._chains.append(chain)
        chain._parent = self

    def _remove_chain(self, chain):
        if chain in self._chains:
            self._chains.remove(chain)
            chain._parent = None

    def _set_chains(self, chains):
        self._chains = chains
        for chain in chains:
            chain._parent = self

    # region connections

    @property
    def _residues(self):
        for chain in self._chains:
            for residue in chain._residues:
                yield residue

    @property
    def _atoms(self):
        for residue in self._residues:
            for atom in residue._atoms:
                yield atom

    @property
    def _bonds(self):
        for residue in self._residues:
            for bond in residue._bonds:
                yield bond

    @property
    def _complex(self):
        return self._parent
    # endregion

    @property
    def _name(self):
        return self._names[self._current_conformer]

    @_name.setter
    def _name(self, value):
        self._names[self._current_conformer] = value

    @property
    def _associated(self):
        return self._associateds[self._current_conformer]

    @_associated.setter
    def _associated(self, value):
        self._associateds[self._current_conformer] = value

    # region conformers
    @property
    def _conformer_count(self):
        return self.__conformer_count

    @_conformer_count.setter
    def _conformer_count(self, value):
        curr_size = len(self._names)
        if value > curr_size:
            extension = value - curr_size
            self._names.extend([self._names[-1]] * (extension))
            copy_val = self._associateds[-1]
            self._associateds.extend([copy_val.copy()
                                      for i in range(extension)])
        else:
            self._names = self._names[:value]
            self._associateds = self._associateds[:value]
        self._current_conformer = min(self._current_conformer, value - 1)
        self.__conformer_count = value

        for atom in self._atoms:
            atom._resize_conformer(value)
        for bond in self._bonds:
            bond._resize_conformer(value)

    def _create_conformer(self, index):
        src = max(0, index - 1)
        self._copy_conformer(src, index)

    def _move_conformer(self, src, dest):
        temp = self._names[src]
        self._names.insert(dest, temp)

        temp = self._associateds[src]
        self._associateds.insert(dest, temp)
        crcted = src + 1 if src > dest else src
        del self._names[crcted]
        del self._associateds[crcted]

        for atom in self._atoms:
            atom._move_conformer(src, dest)
        for bond in self._bonds:
            bond._move_conformer(src, dest)

    def _delete_conformer(self, index):
        del self._names[index]
        del self._associateds[index]
        for atom in self._atoms:
            atom._delete_conformer(index)
        for bond in self._bonds:
            bond._delete_conformer(index)
        self.__conformer_count -= 1
        self._current_conformer = min(
            self._current_conformer, self.__conformer_count - 1)

    def _copy_conformer(self, src, index=None):
        if index is None:
            index = src + 1
        value = self._names[src]
        self._names.insert(index, value)
        value = self._associateds[src].copy()
        self._associateds.insert(index, value)
        for atom in self._atoms:
            atom._copy_conformer(src, index)
        for bond in self._bonds:
            bond._copy_conformer(src, index)
        self.__conformer_count += 1

    # endregion

        # copies the structure. If conformer_number is not None it will only copy that conformer's data
    def _shallow_copy(self, conformer_number=None):
        molecule = _Molecule._create()
        if conformer_number == None:
            molecule._names = list(self._names)
            molecule._associateds = copy.deepcopy(self._associateds)
            molecule.__conformer_count = self.__conformer_count
            molecule._current_conformer = self._current_conformer
        else:
            molecule._name = self._names[conformer_number]
            molecule._associated = self._associateds[conformer_number]
            molecule.__conformer_count = 1
            molecule._current_conformer = 0
        return molecule

    def _deep_copy(self, conformer_number=None, old_to_new_atoms=None):
        return helpers.copy._deep_copy_molecule(self, conformer_number, old_to_new_atoms)


class _Residue(_Base):

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        from nanome.util import Color, enums
        super(_Residue, self).__init__()
        # molecular
        self._type = "ARG"  # RESIDUEDATA
        self._serial = 1
        self._name = "res"
        self._secondary_structure = enums.SecondaryStructure.Unknown
        # rendering
        self._ribboned = True
        self._ribbon_size = 1.0
        self._ribbon_mode = enums.RibbonMode.SecondaryStructure
        self._ribbon_color = Color.Clear()
        self._labeled = False
        self._label_text = ""
        self._ignored_alt_locs = []
        # connections
        self._atoms = []
        self._bonds = []
        self._parent = None

    def _add_atom(self, atom):
        self._atoms.append(atom)
        atom._parent = self

    def _remove_atom(self, atom):
        if atom in self._atoms:
            atom.index = -1
            self._atoms.remove(atom)
            atom._parent = None

    def _add_bond(self, bond):
        bond.index = -1
        self._bonds.append(bond)
        bond._parent = self

    def _remove_bond(self, bond):
        if bond in self._bonds:
            bond.index = -1
            self._bonds.remove(bond)
            bond._parent = None

    def _set_atoms(self, atoms):
        self._atoms = atoms
        for atom in atoms:
            atom._parent = self

    def _set_bonds(self, bonds):
        self._bonds = bonds
        for bond in bonds:
            bond._parent = self

    # region connections
    @property
    def _chain(self):
        return self._parent

    @property
    def _molecule(self):
        parent = self._parent
        if parent:
            return parent._molecule
        else:
            return None

    @property
    def _complex(self):
        parent = self._parent
        if parent:
            return parent._complex
        else:
            return None
    # endregion

    # copies the structure. If conformer_number is not None it will only copy that conformer's data
    def _shallow_copy(self, conformer_number=None):
        residue = _Residue._create()
        # molecular
        residue._type = self._type
        residue._serial = self._serial
        residue._name = self._name
        residue._secondary_structure = self._secondary_structure
        # rendering
        residue._ribboned = self._ribboned
        residue._ribbon_size = self._ribbon_size
        residue._ribbon_mode = self._ribbon_mode
        residue._ribbon_color = self._ribbon_color.copy()
        residue._labeled = self._labeled
        residue._label_text = self._label_text
        residue._ignored_alt_locs = self._ignored_alt_locs[:]
        return residue

    def _deep_copy(self, conformer_number=None):
        return helpers.copy._deep_copy_residue(self, conformer_number)


class _Substructure:

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        self._name = ''
        self._residues = []
        self._structure_type = None

    @property
    def SubstructureType(self):
        from nanome.util import enums
        return enums.SubstructureTypefrom


class _Workspace(_Base):

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        from nanome.util import Vector3, Quaternion
        self._position = Vector3()
        self._rotation = Quaternion()
        self._scale = Vector3(0.02, 0.02, 0.02)
        self._complexes = []

    def _add_complex(self, complex):
        self._complexes.append(complex)
        complex._parent = self

    def _remove_complex(self, complex):
        if complex in self._complexes:
            self._complexes.remove(complex)
            complex._parent = None

    @deprecated()
    def get_atom_iterator(self):
        iterator = _Workspace.AtomIterator(self)
        return iter(iterator)

    class AtomIterator(object):
        def __init__(self, workspace):
            self._workspace = workspace

        def __iter__(self):
            self._complexes = iter(self._workspace.complexes)
            self._update_iter()
            return self

        def __next__(self):
            while True:
                try:
                    return next(self._moleculeAtom)
                except StopIteration:
                    self._update_iter()

        def _update_iter(self):
            while True:
                complex = next(self._complexes)
                try:
                    self._moleculeAtom = complex.get_atom_iterator()
                    break
                except StopIteration:
                    pass
