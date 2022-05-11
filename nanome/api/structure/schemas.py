import logging

from marshmallow import Schema, fields, post_load

from nanome.api import structure

logging = logging.getLogger(__name__)


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
    index = fields.Integer(required=True)

    @post_load
    def make_molecule(self, data, **kwargs):
        new_obj = structure.Molecule()
        for key in data:
            try:
                setattr(new_obj, key, data[key])
            except AttributeError:
                logging.warning('Could not set attribute {}'.format(key))
                pass
        return new_obj


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
        new_obj = structure.Complex()
        for key in data:
            try:
                setattr(new_obj, key, data[key])
            except AttributeError:
                logging.warning('Could not set attribute {}'.format(key))
                pass
        return new_obj
        
