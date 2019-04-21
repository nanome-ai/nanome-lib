import json
from nanome.util import Logs
from nanome._internal._ui._io import _layout_node_json
from nanome._internal import _Addon

class LayoutNodeIO(_Addon):
    def __init__(self, base_object=None):
        _Addon.__init__(self, base_object)

    def to_json(self, path):
        node_json = {}
        node_json["is_menu"] == False
        node_json["title"] == "node"
        node_json["width"] = 1
        node_json["height"] = 1
        node_json["version"] = 0

        node_json["effective_root"] = _layout_node_json.write_json(self.base_object)
        node_string = json.dumps(node_json)

        try:
            with open(path, "w") as f:
                f.write(node_string)
        except:
            Logs.error("Could not write to file: " + path)
            raise


    def from_json(self, path):
        try:
            with open(path) as f:
                node_string = f.read()
                node_json = json.loads(node_string)
        except:
            Logs.error("Could not read json file: " + path)
            raise
        try:
            assert(node_json["is_menu"] == False)
            return _layout_node_json.parse_json(node_json["effective_root"])
        except:
            Logs.error("Json does not correctly represent a layout node.")
            raise