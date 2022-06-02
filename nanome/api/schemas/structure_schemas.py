import itertools
from marshmallow import Schema, fields, post_load
from nanome.api import structure
from nanome.util import enums

from .util_schemas import ColorField, EnumField, QuaternionField, Vector3Field


def init_object(obj, data: dict):
    for key in data:
        if not hasattr(obj, key):
            continue
        try:
            setattr(obj, key, data[key])
        except AttributeError:
            raise AttributeError('Could not set attribute {}'.format(key))


class StructureSchema(Schema):
    index = fields.Integer(default=-1)


class AtomSchema(StructureSchema):
    selected = fields.Boolean()
    labeled = fields.Boolean()
    atom_rendering = fields.Boolean()
    surface_rendering = fields.Boolean()
    exists = fields.Boolean()
    is_het = fields.Boolean()
    occupancy = fields.Float()
    bfactor = fields.Float()
    acceptor = fields.Boolean()
    donor = fields.Boolean()
    polar_hydrogen = fields.Boolean()
    atom_mode = EnumField(enum=enums.AtomRenderingMode)
    serial = fields.Integer()
    current_conformer = fields.Integer(load_only=True)
    conformer_count = fields.Integer(load_only=True)
    positions = fields.List(Vector3Field())
    label_text = fields.String()
    atom_color = ColorField()
    atom_scale = fields.Float()
    surface_color = ColorField()
    surface_opacity = fields.Float()
    symbol = fields.Str()
    name = fields.Str()
    position = Vector3Field()
    formal_charge = fields.Integer()
    partial_charge = fields.Float()
    vdw_radius = fields.Float(load_only=True)
    alt_loc = fields.Str(max=1)
    is_het = fields.Boolean()
    in_conformer = fields.List(fields.Boolean())
    het_surfaced = fields.Boolean()
    display_mode = fields.Integer()

    @post_load
    def make_atom(self, data, **kwargs):
        new_obj = structure.Atom()
        init_object(new_obj, data)
        return new_obj


class BondSchema(StructureSchema):
    atom1 = AtomSchema(only=('index',))
    atom2 = AtomSchema(only=('index',))
    kind = EnumField(enum=enums.Kind)
    in_conformer = fields.List(fields.Boolean())
    kinds = fields.List(fields.Nested(EnumField(enum=enums.Kind)))

    @post_load
    def make_bond(self, data, **kwargs):
        new_obj = structure.Bond()
        init_object(new_obj, data)
        return new_obj


class ResidueSchema(StructureSchema):
    atoms = fields.List(fields.Nested(AtomSchema))
    bonds = fields.List(fields.Nested(BondSchema))
    ribboned = fields.Boolean()
    ribbon_size = fields.Float()
    ribbon_mode = EnumField(enum=enums.RibbonMode)
    ribbon_color = ColorField()
    labeled = fields.Boolean()
    label_text = fields.Str()
    type = fields.Str()
    serial = fields.Integer()
    name = fields.Str()
    secondary_structure = EnumField(enum=enums.SecondaryStructure)
    ignored_alt_locs = fields.List(fields.Str(max=1))

    @post_load
    def make_residue(self, data, **kwargs):
        new_obj = structure.Residue()
        init_object(new_obj, data)
        for child in itertools.chain(new_obj.atoms, new_obj.bonds):
            child._parent = new_obj
        return new_obj


class ChainSchema(StructureSchema):
    name = fields.Str()
    residues = fields.Nested(ResidueSchema, many=True)

    @post_load
    def make_chain(self, data, **kwargs):
        new_obj = structure.Chain()
        init_object(new_obj, data)
        for child in new_obj.residues:
            child._parent = new_obj
        return new_obj


class MoleculeSchema(StructureSchema):
    chains = fields.List(fields.Nested(ChainSchema))
    name = fields.Str()
    associated = fields.Dict()
    conformer_count = fields.Integer()
    current_conformer = fields.Integer()
    names = fields.List(fields.Str())
    associateds = fields.List(fields.Dict())

    @post_load
    def make_molecule(self, data, **kwargs):
        new_obj = structure.Molecule()
        # Set conformer specific attributes first conformer_count first
        if 'conformer_count' in data:
            new_obj._conformer_count = data.pop('conformer_count')
        init_object(new_obj, data)
        for child in new_obj.chains:
            child._parent = new_obj
        return new_obj


class ComplexSchema(StructureSchema):
    boxed = fields.Boolean()
    locked = fields.Boolean()
    visible = fields.Boolean()
    computing = fields.Boolean()
    box_label = fields.String()
    name = fields.Str()
    index_tag = fields.Integer()
    split_tag = fields.Str()
    position = Vector3Field()
    rotation = QuaternionField()
    molecules = fields.List(fields.Nested(MoleculeSchema))
    current_frame = fields.Integer()
    remarks = fields.Dict()

    @post_load
    def make_complex(self, data, **kwargs):
        new_obj = structure.Complex()
        init_object(new_obj, data)
        for child in new_obj.molecules:
            child._parent = new_obj
        return new_obj


class WorkspaceSchema(Schema):
    complexes = fields.List(fields.Nested(ComplexSchema))
    position = Vector3Field()
    rotation = QuaternionField()
    scale = Vector3Field()

    @post_load
    def make_workspace(self, data, **kwargs):
        new_obj = structure.Workspace()
        init_object(new_obj, data)
        return new_obj
