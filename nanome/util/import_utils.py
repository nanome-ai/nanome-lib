import sys

if sys.version_info >= (3, 1) or sys.version_info == (2, 7):
    from importlib import util

class ImportUtils(object):
    @staticmethod
    def check_import_exists(lib_name):
        # type: (str) -> bool
        if sys.version_info >= (3, 1) or sys.version_info == (2, 7):
            spec = util.find_spec(lib_name)
            return spec != None
        else:
            try:
                __import__(spec)
                return True
            except:
                return False