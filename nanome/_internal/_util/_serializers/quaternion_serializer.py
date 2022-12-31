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
        context.write_float(value._x)
        context.write_float(value._y)
        context.write_float(value._z)
        context.write_float(value._w)

    def deserialize(self, version, context):
        quaternion = Quaternion()
        x = context.read_float()
        y = context.read_float()
        z = context.read_float()
        w = context.read_float()
        quaternion.set(x, y, z, w)
        return quaternion


class _UnityRotationSerializer(_TypeSerializer):
    def __init__(self):
        self._Quat = _QuaternionSerializer()

    def version(self):
        return 0

    def name(self):
        return "UnityRotation"

    def serialize(self, version, value, context):
        context.write_using_serializer(self._Quat, value)

    def deserialize(self, version, context):
        return context.read_using_serializer(self._Quat)
