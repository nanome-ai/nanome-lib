import sys
import functools
from .enum import IntEnum, auto


class Logs(object):
    """
    | Allows for easy message logging without buffer issues.
    | Possible log types are Debug, Warning, and Error.
    """
    class _LogType(IntEnum):
        debug = auto()
        warning = auto()
        error = auto()
        info = auto()

    _is_windows_cmd = False
    __verbose = None
    __pipe = None

    @classmethod
    def _set_verbose(cls, value):
        cls.__verbose = value

    @classmethod
    def _set_pipe(cls, value):
        cls.__pipe = value

    @classmethod
    def _is_verbose(cls):
        return cls.__verbose

    @classmethod
    def _print(cls, log_type, *args):
        arr = []
        for arg in args:
            arr.append(str(arg))
        msg = ' '.join(arr)
        if cls.__pipe is not None:
            from nanome._internal._util import _DataType, _ProcData
            to_send = _ProcData()
            to_send._type = _DataType.log
            to_send._data = msg
            cls.__pipe.send(to_send)
        else:
            from nanome._internal._process import _LogsManager
            _LogsManager.received_request(log_type, msg)

    @classmethod
    def error(cls, *args):
        """
        | Prints an error

        :param args: Variable length argument list
        :type args: Anything printable
        """
        log_type = Logs._LogType.error.name
        cls._print(log_type, *args)

    @classmethod
    def warning(cls, *args):
        """
        | Prints a warning

        :param args: Variable length argument list
        :type args: Anything printable
        """
        log_type = log_type = Logs._LogType.warning.name
        cls._print(log_type, *args)

    @classmethod
    def message(cls, *args):
        """
        | Prints a message

        :param args: Variable length argument list
        :type args: Anything printable
        """
        log_type = Logs._LogType.info.name
        cls._print(log_type, *args)

    @classmethod
    def debug(cls, *args):
        """
        | Prints a debug message
        | Prints only if plugin started in verbose mode (with -v argument)

        :param args: Variable length argument list
        :type args: Anything printable
        """
        log_type = log_type = Logs._LogType.debug.name
        if cls.__verbose is None:
            Logs.warning("Debug used before plugin start.")
            cls._print(log_type, *args)
        elif cls.__verbose is True:
            cls._print(log_type, *args)

    @classmethod
    def _init(cls):
        if sys.platform == 'win32' and sys.stdout.isatty():
            cls._is_windows_cmd = True

    @staticmethod
    def deprecated(new_func=None, msg=""):
        def deprecated_decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if not wrapper.used:
                    warning = "Function " + func.__name__ + " is deprecated. "
                    if new_func is not None:
                        warning += "Try using " + new_func + " instead. "
                    warning += msg
                    Logs.warning(warning)
                    wrapper.used = True
                return func(*args, **kwargs)
            wrapper.used = False
            return wrapper
        return deprecated_decorator


Logs._init()
