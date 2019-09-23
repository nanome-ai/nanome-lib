from .enum import IntEnum

class StreamCreationError(IntEnum):
    NoError = 0
    AtomNotFound = 1
    UnsupportedStream = 2

class StreamInterruptReason(IntEnum):
    StreamNotFound = 0
    Crashed = 1