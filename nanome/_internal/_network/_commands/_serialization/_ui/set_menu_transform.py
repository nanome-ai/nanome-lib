from nanome._internal._util._serializers import _Vector3Serializer, _UnityPositionSerializer, _UnityRotationSerializer, _TypeSerializer


class _SetMenuTransform(_TypeSerializer):
    def __init__(self):
        self.pos = _UnityPositionSerializer()
        self.rot = _UnityRotationSerializer()
        self.vec3 = _Vector3Serializer()

    def version(self):
        return 0

    def name(self):
        return "SetMenuTransform"

    def serialize(self, version, value, data):
        data.write_byte(value[0])
        data.write_using_serializer(self.pos, value[1])
        data.write_using_serializer(self.rot, value[2])
        data.write_using_serializer(self.vec3, value[3])

    def deserialize(self, version, data):
        return None
