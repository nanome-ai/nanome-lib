import json
from nanome.util import Logs
from nanome._internal._ui._io import _menu_json
from nanome._internal import _Addon

class MenuIO(_Addon):
    def __init__(self, base_object=None):
        _Addon.__init__(self, base_object)

    def to_json(self, path):
        menu_json = _menu_json.write_json(self.base_object)
        menu_string = json.dumps(menu_json)
        try:
            with open(path, "w") as f:
                f.write(menu_string)
        except:
            Logs.error("Could not write to file: " + path)
            raise

    def from_json(self, path):
        try:
            with open(path) as f:
                menu_string = f.read()
                menu_json = json.loads(menu_string)
        except:
            Logs.error("Could not read json file: " + path)
            raise
        try:
            return _menu_json.parse_json(menu_json)
        except:
            Logs.error("Json does not correctly represent a menu.")
            raise
