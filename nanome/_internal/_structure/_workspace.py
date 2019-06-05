from nanome.util import Vector3, Quaternion, Logs
from . import _Base

class _Workspace(_Base):

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        self._position = Vector3(0,0,0)
        self._rotation = Quaternion(0,0,0,0)
        self._scale = Vector3(1,1,1)
        self._complexes = []

    @Logs.deprecated()
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