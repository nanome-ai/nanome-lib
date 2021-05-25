import sys


def _print(cls, col_type, args):
    if cls._is_windows_cmd:
        print(col_type['msg'], end="")
    else:
        print(col_type['color'], end="")
    print(*args, end="")
    if cls._is_windows_cmd is False:
        print(cls._closing)
    else:
        print("")
    sys.stdout.flush()
