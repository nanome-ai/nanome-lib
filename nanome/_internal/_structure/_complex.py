from nanome.util import Vector3, Quaternion, Logs
from . import _Base

class _Complex(_Base):

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_Complex, self).__init__()
        #Molecular
        self._name = "complex"
        self._index_tag = 0
        self._split_tag = ""
        self._remarks = {}
        #Rendering
        self._boxed = False
        self._locked = False
        self._visible = True
        self._computing = False
        self._current_frame = 0
        self._selected = False #selected on live
        self._surface_dirty = False
        self._surface_refresh_rate = -1.0  # Not used yet, future auto surface refresh
        self._box_label = ""
        #Transform
        self._position = Vector3(0,0,0)
        self._rotation = Quaternion(0,0,0,0)
        self._molecules = []
        self._parent = None

    def _add_molecule(self, molecule):
        self._molecules.append(molecule)
        molecule._parent = self

    def _remove_molecule(self, molecule):
        self._molecules.remove(molecule)
        molecule._parent = None
    
    def _set_molecules(self, molecules):
        self._molecules = molecules
        for molecule in molecules:
            molecule._parent = self

    @Logs.deprecated()
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

    def _shallow_copy(self):
        complex = _Complex._create()
        #Molecular
        self._name = "complex"
        self._index_tag = 0
        self._split_tag = ""
        self._remarks = {}
        #Rendering
        self._boxed = False
        self._locked = False
        self._visible = True
        self._computing = False
        self._current_frame = 0
        self._selected = False #selected on live
        self._surface_dirty = False
        self._surface_refresh_rate = -1.0  # Not used yet, future auto surface refresh
        self._box_label = ""
        #Transform
        self._position = Vector3(0,0,0)
        self._rotation = Quaternion(0,0,0,0)
        return complex

    def _deep_copy(self):
        complex = self._shallow_copy()
        for molecule in self._molecules:
            molecule._deep_copy()
            complex._add_molecule(molecule)
        return complex
