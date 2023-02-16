from nanome._internal.serializer_fields import TypeSerializer, StringField, UnityPositionField, ColorField, ArrayField
import os
import tempfile
import logging
from nanome.util.enums import ShapeType
from .anchor import Anchor
from . import Label, Line, Mesh, Sphere

logger = logging.getLogger(__name__)


class AnchorSerializer(TypeSerializer):
    def __init__(self):
        self._offset = UnityPositionField()

    def version(self):
        return 0

    def name(self):
        return "ShapeAnchor"

    def serialize(self, version, value, context):
        context.write_long(value._target)
        context.write_byte(int(value._anchor_type))
        context.write_using_serializer(self._offset, value._local_offset)
        context.write_using_serializer(self._offset, value._global_offset)
        context.write_using_serializer(self._offset, value._viewer_offset)

    def deserialize(self, version, context):
        result = Anchor()
        result._target = context.read_long()
        result._anchor_type = ShapeType.safe_cast(context.read_byte())
        result._local_offset = context.read_using_serializer(self._offset)
        result._global_offset = context.read_using_serializer(self._offset)
        result._viewer_offset = context.read_using_serializer(self._offset)
        return result


class LabelSerializer(TypeSerializer):
    def __init__(self):
        self._string = StringField()

    def version(self):
        return 0

    def name(self):
        return "LabelShape"

    def serialize(self, version, value, context):
        context.write_using_serializer(self._string, value._text)
        context.write_float(value._font_size)

    def deserialize(self, version, context):
        result = Label()
        result._text = context.read_using_serializer(self._string)
        result._font_size = context.read_float()
        return result


class LineSerializer(TypeSerializer):

    def version(self):
        return 0

    def name(self):
        return "LineShape"

    def serialize(self, version, value, context):
        context.write_float(value._thickness)
        context.write_float(value._dash_length)
        context.write_float(value._dash_distance)

    def deserialize(self, version, context):
        result = Line._create()
        result._thickness = context.read_float()
        result._dash_length = context.read_float()
        result._dash_distance = context.read_float()
        return result


class MeshSerializer(TypeSerializer):

    def version(self):
        return 1

    def name(self):
        return "MeshShape"

    def read_texture(self, value):
        if value.texture_path != "":
            filename, ext = os.path.splitext(value.texture_path)
            if ext.lower() in [".jpeg", ".jpg", ".png"]:
                path = value.texture_path.replace("\\", "/")
                if os.path.isfile(path):
                    try:
                        with open(path, "rb") as f:
                            texture_bytes = bytearray(f.read())
                            return texture_bytes
                    except Exception as e:
                        logger.error("Error reading texture file: " + e)
                else:
                    logger.error("Texture file does not exist")
            else:
                logger.error("Texture file should be a png or a jpg file")
        return []

    def serialize(self, version, value, context):
        context.write_float_array(value.vertices)
        context.write_float_array(value.normals)
        context.write_float_array(value.colors)
        context.write_int_array(value.triangles)
        context.write_float_array(value.uv)

        texture_bytes = self.read_texture(value)
        context.write_byte_array(texture_bytes)
        if len(texture_bytes) > 0:
            logger.debug("Sending texture: {}".format(value.texture_path))

        if version >= 1:
            context.write_bool(value.unlit)

    def create_texture_file(self, texture_path, texture_bytes):
        with open(texture_path, "wb") as f:
            f.write(texture_bytes)

    def deserialize(self, version, context):
        result = Mesh._create()
        result.vertices = context.read_float_array()
        result.normals = context.read_float_array()
        result.colors = context.read_float_array()
        result.triangles = context.read_int_array()
        result.uv = context.read_float_array()
        texture_bytes = context.read_byte_array()

        if version >= 1:
            result.unlit = context.read_bool()

        if len(texture_bytes) > 0:
            temp_texture = tempfile.NamedTemporaryFile(
                delete=False, suffix='png')
            self.create_texture_file(temp_texture.name, texture_bytes)
            result.texture_path = temp_texture.name
        return result


class ShapeSerializer(TypeSerializer):
    def __init__(self):
        self._position = UnityPositionField()
        self._color = ColorField()
        self._sphere = SphereSerializer()
        self._line = LineSerializer()
        self._label = LabelSerializer()
        self._mesh = MeshSerializer()
        self._anchor_array = ArrayField()
        self._anchor_array.set_type(AnchorSerializer())

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
        from nanome.util.enums import ShapeType
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


class SphereSerializer(TypeSerializer):

    def version(self):
        return 0

    def name(self):
        return "SphereShape"

    def serialize(self, version, value, context):
        context.write_float(value.radius)

    def deserialize(self, version, context):
        result = Sphere._create()
        result.radius = context.read_float()
        return result
