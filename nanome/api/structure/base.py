from nanome._internal._structure._base import _Base
__metaclass__ = type

class Base(_Base):
    def __init__(self):
        super(Base, self).__init__()

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        self._index = value
