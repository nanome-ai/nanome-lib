from nanome.util.logs import Logs
from nanome._internal._util._serializers import _ArraySerializer, _TypeSerializer, _UnityPositionSerializer, _ColorSerializer, _UnityRotationSerializer
from nanome._internal._shapes._serialization import _SphereSerializer, _ShapeSerializer, _LineSerializer, _LabelSerializer, _MeshSerializer
from nanome.util.enums import ShapeType
from nanome.util import Quaternion


class _SetShape(_TypeSerializer):
    def __init__(self):
        self._position = _UnityPositionSerializer()
        self._rotation = _UnityRotationSerializer()
        self._color = _ColorSerializer()
        self._sphere = _SphereSerializer()
        self._line = _LineSerializer()
        self._label = _LabelSerializer()
        self._mesh = _MeshSerializer()
        self._shape = _ShapeSerializer()
        self._shape_array = _ArraySerializer()
        self._shape_array.set_type(self._shape)

    def version(self):
        return 2

    def name(self):
        return "SetShape"

    def serialize(self, version, value, context):
        if version == 0:
            if len(value) > 1:
                msg = "SetShape: Using a list of shapes with an old version of Nanome"
                Logs.warning(msg)
                raise TypeError(msg)
            first_elem = value[0]
            context.write_byte(int(first_elem.shape_type))
            if first_elem.shape_type == ShapeType.Sphere:
                context.write_using_serializer(self._sphere, first_elem)
            if first_elem.shape_type == ShapeType.Line:
                context.write_using_serializer(self._line, first_elem)
            if first_elem.shape_type == ShapeType.Label:
                context.write_using_serializer(self._label, first_elem)
            if first_elem.shape_type == ShapeType.Mesh:
                context.write_using_serializer(self._mesh, first_elem)
            context.write_int(first_elem.index)
            context.write_long(first_elem.target)
            context.write_byte(int(first_elem.anchor))
            context.write_using_serializer(self._position, first_elem.position)
            context.write_using_serializer(self._rotation, Quaternion())
            context.write_using_serializer(self._color, first_elem.color)
        elif version == 1:
            if len(value) > 1:
                msg = "SetShape: Using a list of shapes with an old version of Nanome"
                Logs.warning(msg)
                raise TypeError(msg)
            first_elem = value[0]
            context.write_using_serializer(self._shape, first_elem)
        elif version == 2:
            context.write_using_serializer(self._shape_array, value)

    def deserialize(self, version, context):
        if version < 2:
            return ([context.read_int()], [context.read_bool()])
        else:
            indices_arr = context.read_int_array()
            success_arr = context.read_byte_array()
            return (indices_arr, success_arr)
