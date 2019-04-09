import sys

def _print(cls, col_type, args):
    if cls._is_windows_cmd:
        print col_type['msg'],
    else:
        print col_type['color'],
    for arg in args:
        print arg,
    if cls._is_windows_cmd == False:
        print cls._closing
    else:
        print
    sys.stdout.flush()