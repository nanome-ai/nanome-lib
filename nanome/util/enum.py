import sys


@classmethod
def safe_cast(cls, value):
    try:
        return cls(value)
    except ValueError:
        if cls.cast_failed_warning is False:
            cls.cast_failed_warning = True
            from . import Logs
            Logs.warning("Invalid value", value, "for enum", cls.__name__, ". Library might outdated.")
        return list(cls)[0]


if sys.version_info >= (3, 4):
    from enum import Enum, IntEnum
else:
    from .py2_enum import Enum, IntEnum

if sys.version_info >= (3, 6):
    from enum import auto

    def reset_auto():
        pass

else:
    from .py2_enum import auto, reset_auto

Enum.safe_cast = safe_cast
Enum.cast_failed_warning = False
