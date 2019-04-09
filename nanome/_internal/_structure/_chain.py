from . import _Base

class _Chain(_Base):
    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_Chain, self).__init__()
        self._molecular = _Chain.Molecular._create()
        self._residues = []

    class Molecular(object):
        @classmethod
        def _create(cls):
            return cls()

        def __init__(self):
            self._name = ""

    def get_atom_iterator(self):
        iterator = _Chain.AtomIterator(self)
        return iter(iterator)

    class AtomIterator(object):
        def __init__(self, chain):
            self._chain = chain

        def __iter__(self):
            self._residue = iter(self._chain._residues)
            self._update_iter()
            return self

        def __next__(self):
            while True:
                try:
                    return next(self._atom)
                except StopIteration:
                    self._update_iter()

        def _update_iter(self):
            while True:
                residue = next(self._residue)
                try:
                    self._atom = residue.get_atom_iterator()
                    break
                except StopIteration:
                    pass