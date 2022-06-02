from marshmallow import Schema, fields, post_load, ValidationError
from nanome.util import Vector3, Quaternion, Color


class EnumField(fields.Field):
    """Marshmallow field for enum type"""

    def __init__(self, *args, enum=None, **kwargs):
        super().__init__(*args, **kwargs)
        if not enum:
            raise ValueError("Must specify enum")
        self.enum = enum

    def _deserialize(self, value, attr, data, **kwargs):
        return self.enum(value)

    def _serialize(self, enum_opt, attr, data, **kwargs):
        return enum_opt.value


class QuaternionField(fields.Field):

    def _serialize(self, value: Vector3, attr, obj, **kwargs):
        return [value.x, value.y, value.z, value.w]

    def _deserialize(self, value, attr, data, **kwargs):
        if len(value) != 4:
            raise ValidationError("Quaternion must contain 4 values")
        return Quaternion(*value)


class Vector3Field(fields.Field):

    def _serialize(self, value, attr, obj, **kwargs):
        output = list(value.unpack())
        return output

    def _deserialize(self, value, attr, data, **kwargs):
        return Vector3(*value)


class ColorField(fields.Field):

    def _serialize(self, value: Color, attr, obj, **kwargs):
        return [value.r, value.g, value.b, value.a]

    def _deserialize(self, value, attr, data, **kwargs):
        if len(value) != 4:
            raise ValidationError("Quaternion must contain 4 values")
        return Color(*value)
