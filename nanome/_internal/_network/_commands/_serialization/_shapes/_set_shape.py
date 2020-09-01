from nanome._internal._util._serializers import _TypeSerializer, _Vector3Serializer, _ColorSerializer
from nanome._internal._shapes._serialization import _SphereSerializer
from nanome.util.enums import ShapeType

class _SetShape(_TypeSerializer):
    def __init__(self):
        self._position = _Vector3Serializer()
        self._color = _ColorSerializer()
        self._sphere = _SphereSerializer()

    def version(self):
        return 0

    def name(self):
        return "SetShape"

    def serialize(self, version, value, context):
        context.write_byte(int(value.shape_type))
        if value.shape_type == ShapeType.Sphere:
            context.write_using_serializer(self._sphere, value)
        context.write_int(value.index)
        context.write_long(value.target)
        context.write_byte(int(value.anchor))
        context.write_using_serializer(self._position, value.position)
        context.write_using_serializer(self._color, value.color)

    def deserialize(self, version, context):
        return (context.read_int(), context.read_bool())