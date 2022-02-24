from nanome.util import IntEnum, auto


class _DataType(IntEnum):
    """Enum of types of data the ProcessNetwork Pipe can handle"""

    process = auto()


class _ProcData():

    def __init__(self):
        self._type = _DataType.process
        self._data = None
