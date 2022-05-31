from marshmallow import Schema, fields
from nanome.util import enums
from .util_schemas import EnumField, ColorField, Vector3Field


class AnchorSchema(Schema):
    anchor_type = EnumField(enum=enums.ShapeAnchorType)
    target = fields.Integer()
    local_offset = Vector3Field()
    global_offset = Vector3Field()


class ShapeSchema(Schema):
    index = fields.String()
    shape_type = EnumField(enum=enums.ShapeType)
    color = ColorField()
    anchors = fields.List(fields.Nested('AnchorSchema'))


class LabelSchema(ShapeSchema):
    text = fields.String()
    font_size = fields.Float()


class MeshSchema(ShapeSchema):
    vertices = fields.List(fields.Float())
    normals = fields.List(fields.Float())
    colors = fields.List(fields.Float())
    triangles = fields.List(fields.Int())
    uv = fields.List(fields.Float())
    unlit = fields.Boolean()
    texture_path = fields.String()


class SphereSchema(ShapeSchema):
    radius = fields.Float()
