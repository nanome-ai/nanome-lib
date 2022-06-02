from marshmallow import fields, Schema


class StreamSchema(Schema):
    id = fields.Integer(required=True)
