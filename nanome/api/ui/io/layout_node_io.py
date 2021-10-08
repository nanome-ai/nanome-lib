import json
from nanome.util import Logs
from nanome._internal._ui._io._json_helper import _JsonHelper
from nanome._internal._ui._io import _layout_node_json
from nanome._internal import _Addon


class LayoutNodeIO(_Addon):
    """
    | A class for json serialization and parsing of LayoutNode objects.

    :param base_object: The LayoutNode to serialize
    :type base_object: :class:`~nanome.ui.LayoutNode`
    """

    def __init__(self, base_object=None):
        _Addon.__init__(self, base_object)

    def to_json(self, path):
        """
        | Serializes this instance's base_object to the json file specified by path.

        :param path: The path to serialize base_object's json representation to
        :type path: :class:`str`
        """
        helper = _JsonHelper()
        helper.write("is_menu", False)
        helper.write("title", "node")
        child = helper.make_instance()
        _layout_node_json.write_json(child, self.base_object)
        helper.write("effective_root", child)
        node_string = json.dumps(helper.get_dict())

        try:
            with open(path, "w") as f:
                f.write(node_string)
        except:
            Logs.error("Could not write to file: " + path)
            raise

    def from_json(self, path):
        """
        | Parses a LayoutNode json file and returns a LayoutNode.

        :param path: The path to the LayoutNode json to parse
        :type path: :class:`str`
        """
        try:
            with open(path) as f:
                node_string = f.read()
                node_json = json.loads(node_string)
        except:
            Logs.error("Could not read json file: " + path)
            raise
        try:
            json_helper = _JsonHelper(node_json)
            assert(json_helper.read("is_menu", False) == False)
            return _layout_node_json.parse_json(json_helper.read_object("effective_root"))
        except:
            Logs.error("Json does not correctly represent a layout node.")
            raise
