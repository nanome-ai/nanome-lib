from nanome.util import Vector3, Quaternion
from . import _Base

class _Complex(_Base):

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_Complex, self).__init__()
        self._rendering = _Complex.Rendering._create()
        self._molecular = _Complex.Molecular._create()
        self._transform = _Complex.Transform._create()
        self._molecules = []

    class Rendering(object):
        @classmethod
        def _create(cls):
            return cls()

        def __init__(self):
            self._boxed = False
            self._locked = False
            self._visible = True
            self._computing = False
            self._current_frame = 0
            self._selected = False #selected on live
            
    class Molecular(object):
        @classmethod
        def _create(cls):
            return cls()

        def __init__(self):
            self._name = "complex"
            self._remarks = {}
    
    class Transform(object):
        @classmethod
        def _create(cls):
            return cls()

        def __init__(self):
            self._position = Vector3(0,0,0)
            self._rotation = Quaternion(0,0,0,0)

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