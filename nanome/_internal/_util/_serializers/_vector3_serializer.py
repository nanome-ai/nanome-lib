from nanome.util import Vector3

from nanome._internal._util._serializers import _TypeSerializer

class _Vector3Serializer(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "Vector3"

    def serialize(self, version, value, context):
        context.write_float(value.x)
        context.write_float(value.y)
        context.write_float(value.z)

    def deserialize(self, version, context):
        x = context.read_float()
        y = context.read_float()
        z = context.read_float()
        return Vector3(x,y,z)
