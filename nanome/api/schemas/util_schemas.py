from marshmallow import Schema, fields, post_load, ValidationError
from nanome.api.user import PresenterInfo
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


class PresenterInfoSchema(Schema):
    account_id = fields.Str()
    account_name = fields.Str()
    account_email = fields.Email()
    has_org = fields.Bool()
    org_id =fields.Integer()
    org_name = fields.Str()

    @post_load
    def make_presenter_info(self, data, **kwargs):
        new_obj = PresenterInfo()
        for key in data:
            try:
                setattr(new_obj, key, data[key])
            except AttributeError:
                raise AttributeError('Could not set attribute {}'.format(key))
        return new_obj