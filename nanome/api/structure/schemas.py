from datetime import date
from pprint import pprint

from marshmallow import Schema, fields, post_load

from nanome.api.structure import Complex

class QuaternionSchema(Schema):
    x = fields.Float(required=True)
    y = fields.Float(required=True)
    z = fields.Float(required=True)
    w = fields.Float(required=True)


class Vector3Schema(Schema):
    x = fields.Float(required=True)
    y = fields.Float()
    z = fields.Float()


class AtomSchema(Schema):
    index = fields.Integer(required=True)


class BondSchema(Schema):
    index = fields.Integer(required=True)


class ResidueSchema(Schema):
    index = fields.Integer(required=True)


class ChainSchema(Schema):
    index = fields.Integer(required=True)


class MoleculeSchema(Schema):
    id = fields.Integer(required=True)


class ComplexSchema(Schema):
    index = fields.Integer(required=True)
    current_frame = fields.Integer()
    boxed = fields.Boolean()
    locked = fields.Boolean()
    visible = fields.Boolean()
    computing = fields.Boolean()
    box_label = fields.String()
    name = fields.Str()
    index_tag = fields.Str()
    split_tag = fields.Str()
    position = fields.List(fields.Float, min=3, max=3)
    rotation = fields.List(fields.Float, min=4, max=4)
    molecules = fields.List(fields.Nested(MoleculeSchema))

    @post_load
    def make_complex(self, data, **kwargs):
        comp = Complex()
        for key in data:
            try:
                setattr(comp, key, data[key])
            except AttributeError:
                print(key)
                pass
        return comp
        
