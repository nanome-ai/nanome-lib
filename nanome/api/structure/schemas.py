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

    @post_load
    def make_atom(self, data, **kwargs):
        new_obj = structure.Atom()
        for key in data:
            try:
                setattr(new_obj, key, data[key])
            except AttributeError:
                raise AttributeError('Could not set attribute {}'.format(key))
        return new_obj


class BondSchema(Schema):
    index = fields.Integer(required=True)
    atom1 = fields.Integer()
    atom2 = fields.Integer()

    @post_load
    def make_bond(self, data, **kwargs):
        new_obj = structure.Bond()
        # Manually create atom objects with provided index set
        atom1 = structure.Atom()
        atom1.index = data.pop('atom1')
        atom2 = structure.Atom()
        atom2.index = data.pop('atom2')
        new_obj.atom1 = atom1
        new_obj.atom2 = atom2

        for key in data:
            try:
                setattr(new_obj, key, data[key])
            except AttributeError:
                raise AttributeError('Could not set attribute {}'.format(key))
        return new_obj

class ResidueSchema(Schema):
    index = fields.Integer(required=True)
    atoms = fields.List(fields.Nested(AtomSchema))
    bonds = fields.List(fields.Nested(BondSchema))

    @post_load
    def make_residue(self, data, **kwargs):
        new_obj = structure.Residue()
        for key in data:
            try:
                setattr(new_obj, key, data[key])
            except AttributeError:
                raise AttributeError('Could not set attribute {}'.format(key))
        return new_obj


class ChainSchema(Schema):
    index = fields.Integer(required=True)
    name = fields.Str()
    residues = fields.Nested(ResidueSchema, many=True)

    @post_load
    def make_chain(self, data, **kwargs):
        new_obj = structure.Chain()
        for key in data:
            try:
                setattr(new_obj, key, data[key])
            except AttributeError:
                raise AttributeError('Could not set attribute {}'.format(key))
        return new_obj


class MoleculeSchema(Schema):
    index = fields.Integer(default=-1)
    chains = fields.List(fields.Nested(ChainSchema))
    name = fields.Str()
    associated = fields.List(fields.Str())
    conformer_count = fields.Integer()
    current_conformer = fields.Integer()

    @post_load
    def make_molecule(self, data, **kwargs):
        new_obj = structure.Molecule()
        for key in data:
            try:
                setattr(new_obj, key, data[key])
            except AttributeError:
                raise AttributeError('Could not set attribute {}'.format(key))

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
        
