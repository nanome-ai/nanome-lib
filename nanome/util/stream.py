from .enum import IntEnum

class StreamCreationError(IntEnum):
    """Enumerates errors possible during stream creation.
    """
    NoError = 0
    AtomNotFound = 1
    UnsupportedStream = 2

class StreamInterruptReason(IntEnum):
    """Enumerates reasons for stream interruption.
    """
    StreamNotFound = 0
    Crashed = 1