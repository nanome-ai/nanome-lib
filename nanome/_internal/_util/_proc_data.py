from nanome.util import IntEnum, auto


class _DataType(IntEnum):
    process = auto()
    log = auto()


class _ProcData():
    def __init__(self):
        self._type = _DataType.process
        self._data = None
