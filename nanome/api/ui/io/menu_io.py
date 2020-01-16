import json
from nanome.util import Logs
from nanome._internal._ui._io._json_helper import _JsonHelper
from nanome._internal._ui._io import _menu_json
from nanome._internal import _Addon


class MenuIO(_Addon):
    def __init__(self, base_object=None):
        _Addon.__init__(self, base_object)

    def to_json(self, path):
        helper = _JsonHelper()
        _menu_json.write_json(helper, self.base_object)
        menu_string = json.dumps(helper.get_dict())
        try:
            with open(path, "w") as f:
                f.write(menu_string)
        except:
            Logs.error("Could not write to file: " + path)
            raise

    def from_json(self, path):
        try:
            with open(path, "r") as f:
                menu_string = f.read()
                menu_json = json.loads(menu_string)
        except:
            Logs.error("Could not read json file: " + path)
            raise
        try:
            json_helper = _JsonHelper(menu_json)
            return _menu_json.parse_json(json_helper)
        except:
            Logs.error("Json does not correctly represent a menu.")
            raise

    def update_json(self, path):
        """
        | Updates a menu written for an old version of the library.
        | Call once before reading and run once. Then you can remove the call.

        :param path: path to the menu you wish to update.
        :type path: str
        """
        menu = self.from_json(path)
        menu.io.to_json(path)
