from nanome._internal._structure._base import _Base
__metaclass__ = type


class Base(_Base):
    """
    | Represents the base of a chemical structure (atom, molecule, etc)
    """

    def __init__(self):
        super(Base, self).__init__()

    @property
    def index(self):
        """
        | Index of the base (int)
        """
        return self._index

    @index.setter
    def index(self, value):
        self._index = value
