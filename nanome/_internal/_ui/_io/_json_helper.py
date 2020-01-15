from nanome.util import Logs
from nanome.util.color import Color
from nanome.util.vector3 import Vector3

class _JsonHelper(object):
    def __init__(self, json = None):
        if json == None:
            json = {}
        assert(isinstance(json, dict))
        self.json = json

    def read(self, name, default):
        if name not in self.json:
            return default
        value = self.json[name]
        if (isinstance(default, bool)): #needs to come before int
            return bool(value)
        elif (isinstance(default, int)):
            return int(float(value))
        elif (isinstance(default, str)):
            return str(value)
        elif (isinstance(default, float)):
            return float(value)
        elif (isinstance(default, Color)):
            return Color.from_int(int(float((value))))

    def write(self, name, value):
        if (isinstance(value, Color)):
            self.json[name] = value._color
        elif (isinstance(value, Vector3)):
            self.write_vector(name, value)
        elif (isinstance(value, _JsonHelper)):
            self.json[name] = value.get_dict()
        else:
            self.json[name] = value

    def write_vector(self, name, value):
        builder = _JsonHelper()
        builder.write("x", value.x)
        builder.write("y", value.y)
        builder.write("z", value.z)
        self.write(name, builder)

    def make_child(self):
        return _JsonHelper()

    def read_child(self, name):
        if name not in self.json:
            return None
        child = self.json[name]
        if child is None:
            return None
        return _JsonHelper(child)

    def read_children(self, name):
        if name not in self.json:
            return None
        children = self.json[name]
        for (i, child) in enumerate(children):
            children[i] = _JsonHelper(child)
        return children

    def get_dict(self):
        if len(self.json) == 0:
            return None
        return self.json