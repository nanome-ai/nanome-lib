from . import _Base
from nanome.util import IntEnum

class _Bond(_Base):
    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_Bond, self).__init__()
        self._molecular = _Bond.Molecular._create()
        self._atom1 = None
        self._atom2 = None

    class Molecular(object):
        @classmethod
        def _create(cls):
            return cls()

        def __init__(self):
            self._kind = _Bond.Kind.CovalentSingle

    class Kind(IntEnum):
        CovalentSingle = 1
        CovalentDouble = 2
        CovalentTriple = 3
        Hydrogen = 4
        HydrogenWater = 5