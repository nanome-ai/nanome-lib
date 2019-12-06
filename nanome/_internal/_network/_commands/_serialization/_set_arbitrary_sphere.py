from nanome._internal._util._serializers import _TypeSerializer, _Vector3Serializer, _ColorSerializer

class _SetArbitrarySphere(_TypeSerializer):
    def __init__(self):
        self._position = _Vector3Serializer()
        self._color = _ColorSerializer()

    def version(self):
        return 0

    def name(self):
        return "SetArbitrarySphere"

    def serialize(self, version, value, context):
        context.write_int(value[0])
        context.write_using_serializer(self._position, value[1])
        context.write_float(value[2])
        context.write_using_serializer(self._color, value[3])

    def deserialize(self, version, context):
        pass