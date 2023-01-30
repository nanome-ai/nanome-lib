import logging
from nanome._internal import serializer_fields
from . import serializers

logger = logging.getLogger(__name__)


class DeleteShape(serializer_fields.TypeSerializer):
    def version(self):
        return 1

    def name(self):
        return "DeleteShape"

    def serialize(self, version, value, context):
        if version == 0:
            if len(value) > 1:
                msg = "SetShape: Using a list of shapes with an old version of Nanome"
                logger.warning(msg)
                raise TypeError(msg)
            context.write_int(value[0])
        elif version == 1:
            context.write_int_array(value)

    def deserialize(self, version, context):
        if version == 0:
            return [context.read_bool()]
        elif version == 1:
            return context.read_byte_array()


class SetShape(serializer_fields.TypeSerializer):

    def __init__(self):
        self._position = serializer_fields.UnityPositionField()
        self._rotation = serializer_fields.UnityRotationField()
        self._color = serializer_fields.ColorField()
        self._sphere = serializers.SphereSerializer()
        self._line = serializers.LineSerializer()
        self._label = serializers.LabelSerializer()
        self._mesh = serializers.MeshSerializer()
        self._shape = serializers.ShapeSerializer()
        self._shape_array = serializer_fields.ArrayField()
        self._shape_array.set_type(self._shape)

    def version(self):
        return 2

    def name(self):
        return "SetShape"

    def serialize(self, version, value, context):
        from nanome.util import Quaternion
        from nanome.util.enums import ShapeType
        if version == 0:
            if len(value) > 1:
                msg = "SetShape: Using a list of shapes with an old version of Nanome"
                logger.warning(msg)
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
                logger.warning(msg)
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
