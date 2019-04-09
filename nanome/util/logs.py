import sys

if sys.version_info >= (3, 0):
    from ._logs_3 import _print
else:
    from ._logs_2 import _print

class Logs(object):
    _is_windows_cmd = False
    _print_type = {
        'debug': {'color': '\x1b[0m', 'msg': ''},
        'warning': {'color': '\x1b[33m', 'msg': 'Warning: '},
        'error': {'color': '\x1b[91m', 'msg': 'Error: '}
    }
    _closing = '\x1b[0m'

    @classmethod
    def _print(cls, col_type, *args):
        _print(cls, col_type, args)

    @classmethod
    def error(cls, *args):
        cls._print(cls._print_type['error'], *args)

    @classmethod
    def warning(cls, *args):
        cls._print(cls._print_type['warning'], *args)

    @classmethod
    def debug(cls, *args):
        cls._print(cls._print_type['debug'], *args)

    @classmethod
    def init(cls):
        if sys.platform == 'win32' and sys.stdout.isatty():
            cls._is_windows_cmd = True

Logs.init()