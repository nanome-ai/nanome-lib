from . import _Base

class _Molecule(_Base):
    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_Molecule, self).__init__()
        self._molecular = _Molecule.Molecular._create()
        self._chains = []
        
    class Molecular(object):
        @classmethod
        def _create(cls):
            return cls()

        def __init__(self):
            self._name = ""
            self._associated = {}

    def get_atom_iterator(self):
        iterator = _Molecule.AtomIterator(self)
        return iter(iterator)

    class AtomIterator(object):
        def __init__(self, molecule):
            self._molecule = molecule

        def __iter__(self):
            self._chain = iter(self._molecule._chains)
            self._update_iter()
            return self

        def __next__(self):
            while True:
                try:
                    return next(self._residueAtom)
                except StopIteration:
                    self._update_iter()

        def _update_iter(self):
            while True:
                chain = next(self._chain)
                try:
                    self._residueAtom = chain.get_atom_iterator()
                    break
                except StopIteration:
                    pass