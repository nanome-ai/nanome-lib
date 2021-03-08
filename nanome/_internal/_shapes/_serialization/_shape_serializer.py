from nanome._internal._util._serializers import _TypeSerializer, _UnityPositionSerializer, _ColorSerializer, _ArraySerializer
from nanome._internal._shapes._serialization import _SphereSerializer, _AnchorSerializer
from nanome._internal._shapes import _Shape

from nanome.util.enums import ShapeType

class _SetShape(_TypeSerializer):
    def __init__(self):
        self._position = _UnityPositionSerializer()
        self._color = _ColorSerializer()
        self._sphere = _SphereSerializer()
        self._anchor_array = _ArraySerializer()
        self._anchor_array.set_type(_AnchorSerializer)

    def version(self):
        return 1

    def name(self):
        return "SetShape"

    def serialize(self, version, value, context):
        context.write_byte(int(value.ShapeType))
        if value.shape_type == ShapeType.Sphere:
            context.write_using_serializer(self._sphere, value)
        if value.shape_type == ShapeType.Line:
            pass
            # context.write_using_serializer(_Line, (Line)value)
        context.write_int(value.Index)
        context.write_using_serializer(self._anchor_array, value.Anchors)
        context.write_using_serializer(self._color, value.Color)

    def deserialize(self, version, context):
        shapeType = ShapeType.safe_cast(context.read_byte())
        result = None
        if shapeType == ShapeType.Sphere:
            result = context.read_using_serializer(self._sphere)
        if shapeType == ShapeType.Line:
            pass
            # result = context.read_using_serializer(self._line)
        result._Index = context.read_int()
        result._Anchors = context.read_using_serializer(self._anchor_array)
        result._Color = context.read_using_serializer(self._color)

        return (context.read_int(), context.read_bool())