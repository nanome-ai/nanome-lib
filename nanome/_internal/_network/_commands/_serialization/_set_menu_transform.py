from nanome._internal._util._serializers import _Vector3Serializer, _QuaternionSerializer, _TypeSerializer

class _SetMenuTransform(_TypeSerializer):
    def __init__(self):
        self.vector = _Vector3Serializer()
        self.quat = _QuaternionSerializer()

    def version(self):
        return 0

    def name(self):
        return "SetMenuTransform"

    def serialize(self, version, value, data):
        data.write_using_serializer(self.vector, value[0])
        data.write_using_serializer(self.quat, value[1])

    def deserialize(self, version, data):
        return None