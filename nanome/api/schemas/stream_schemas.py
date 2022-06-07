from marshmallow import fields, Schema
from nanome.util import enums
from .util_schemas import EnumField


class StreamSchema(Schema):
    id = fields.Integer(required=True)
    data_type = EnumField(enum=enums.StreamDataType)
    direction = EnumField(enum=enums.StreamDirection)
