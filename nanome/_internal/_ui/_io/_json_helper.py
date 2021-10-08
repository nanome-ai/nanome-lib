from nanome.util import Logs
from nanome.util import IntEnum
from nanome.util.color import Color
from nanome.util.vector3 import Vector3


class _JsonHelper(object):
    def __init__(self, json=None):
        if json == None:
            json = {}
        assert(isinstance(json, dict))
        self.json = json

    def read(self, name, default):
        if name not in self.json:
            return default
        value = self.json[name]
        def_type = type(default)
        # using == to miss inheritance (bool, intenum)
        if def_type == int:
            return int(float(value))
        # using isinstance to catch inheritance
        elif isinstance(default, Vector3):
            return self.read_vector3(name)
        elif isinstance(default, Color):
            return Color.from_int(int(float((value))))
        else:
            return def_type(value)

    def read_vector3(self, name):
        value = self.read_object(name)
        if value == None:
            return None
        else:
            return Vector3(value.read("x", 0.0), value.read("y", 0.0), value.read("z", 0.0))

    def write(self, name, value):
        if (isinstance(value, Color)):
            self.json[name] = value._color
        elif(isinstance(value, IntEnum)):
            self.write(name, int(value))
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

    def make_instance(self):
        return _JsonHelper()

    def read_object(self, name):
        if name not in self.json:
            return None
        child = self.json[name]
        if child is None:
            return None
        return _JsonHelper(child)

    def read_objects(self, name):
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
