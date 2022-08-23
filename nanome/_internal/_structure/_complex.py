from nanome.util import Vector3, Quaternion, Logs
from . import _Base
from . import _helpers


class _Complex(_Base):

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
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
        return _helpers._copy._deep_copy_complex(self)

    def _convert_to_conformers(self, force_conformers=None):
        result = _helpers._conformer_helper.convert_to_conformers(self, None)
        return result

    def _convert_to_frames(self, old_to_new_atoms=None):
        result = _helpers._conformer_helper.convert_to_frames(self, old_to_new_atoms)
        return result
