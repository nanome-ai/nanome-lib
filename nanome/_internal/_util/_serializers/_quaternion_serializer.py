from nanome.util import Quaternion

from nanome._internal._util._serializers import _TypeSerializer

class _QuaternionSerializer(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "Quaternion"

    def serialize(self, version, value, context):
        context.write_float(value._w)
        context.write_float(value._x)
        context.write_float(value._y)
        context.write_float(value._z)

    def deserialize(self, version, context):
        quaternion = Quaternion()
        w = context.read_float()
        x = context.read_float()
        y = context.read_float()
        z = context.read_float()
        quaternion.set(w,x,y,z)
        return quaternion
