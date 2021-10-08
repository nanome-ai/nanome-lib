from nanome._internal._util._serializers import _TypeSerializer, _UnityPositionSerializer, _ColorSerializer, _ArraySerializer
from nanome._internal._shapes._serialization import _SphereSerializer, _AnchorSerializer, _LineSerializer, _LabelSerializer, _MeshSerializer

from nanome.util.enums import ShapeType


class _ShapeSerializer(_TypeSerializer):
    def __init__(self):
        self._position = _UnityPositionSerializer()
        self._color = _ColorSerializer()
        self._sphere = _SphereSerializer()
        self._line = _LineSerializer()
        self._label = _LabelSerializer()
        self._mesh = _MeshSerializer()
        self._anchor_array = _ArraySerializer()
        self._anchor_array.set_type(_AnchorSerializer())

    def version(self):
        return 1

    def name(self):
        return "Shape"

    def serialize(self, version, value, context):
        context.write_byte(int(value._shape_type))
        if value.shape_type == ShapeType.Sphere:
            context.write_using_serializer(self._sphere, value)
        elif value.shape_type == ShapeType.Line:
            context.write_using_serializer(self._line, value)
        elif value.shape_type == ShapeType.Label:
            context.write_using_serializer(self._label, value)
        elif value.shape_type == ShapeType.Mesh:
            context.write_using_serializer(self._mesh, value)
        context.write_int(value._index)
        context.write_using_serializer(self._anchor_array, value._anchors)
        context.write_using_serializer(self._color, value._color)

    def deserialize(self, version, context):
        shapeType = ShapeType.safe_cast(context.read_byte())
        result = None
        if shapeType == ShapeType.Sphere:
            result = context.read_using_serializer(self._sphere)
        elif shapeType == ShapeType.Line:
            result = context.read_using_serializer(self._line)
        elif shapeType == ShapeType.Label:
            result = context.read_using_serializer(self._label)
        elif shapeType == ShapeType.Mesh:
            result = context.read_using_serializer(self._mesh)
        result._index = context.read_int()
        result._anchors = context.read_using_serializer(self._anchor_array)
        result._color = context.read_using_serializer(self._color)

        return (context.read_int(), context.read_bool())
