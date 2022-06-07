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


class AtomSchema(Schema):
    index = fields.Integer(default=-1)
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


class BondSchema(Schema):
    index = fields.Integer(default=-1)
    atom1 = fields.Nested(AtomSchema(only=('index',)))
    atom2 = fields.Nested(AtomSchema(only=('index',)))
    kind = EnumField(enum=enums.Kind)
    in_conformer = fields.List(fields.Boolean())
    kinds = fields.List(EnumField(enum=enums.Kind))

    @post_load
    def make_bond(self, data, **kwargs):
        new_obj = structure.Bond()
        init_object(new_obj, data)
        return new_obj


class ResidueSchema(Schema):
    index = fields.Integer(default=-1)
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


class ChainSchema(Schema):
    index = fields.Integer(default=-1)
    name = fields.Str()
    residues = fields.Nested(ResidueSchema, many=True)

    @post_load
    def make_chain(self, data, **kwargs):
        new_obj = structure.Chain()
        init_object(new_obj, data)
        for child in new_obj.residues:
            child._parent = new_obj
        return new_obj


class MoleculeSchema(Schema):
    index = fields.Integer(default=-1)
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


class ComplexSchema(Schema):
    index = fields.Integer(default=-1)
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


class StructureSchema(Schema):

    structure_schema_map = {
        structure.Atom: AtomSchema(),
        structure.Bond: BondSchema(),
        structure.Residue: ResidueSchema(),
        structure.Chain: ChainSchema(),
        structure.Molecule: MoleculeSchema(),
        structure.Complex: ComplexSchema(),
    }

    def dump(self, obj, *args, **kwargs):
        obj_class = obj.__class__
        schema = self.structure_schema_map[obj_class]
        dump_data = schema.dump(obj, *args, **kwargs)
        return dump_data

    def load(self, data, *args, **kwargs):
        correct_schema = self.determine_structure_schema(data)
        return correct_schema.load(data, *args, **kwargs)

    def determine_structure_schema(self, data):
        """Use unique fields to determine schema to use for provided data."""
        complex_fields = set(ComplexSchema._declared_fields.keys())
        molecule_fields = set(MoleculeSchema._declared_fields.keys())
        chain_fields = set(ChainSchema._declared_fields.keys())
        residue_fields = set(ResidueSchema._declared_fields.keys())
        atom_fields = set(AtomSchema._declared_fields.keys())
        bond_fields = set(BondSchema._declared_fields.keys())
        unique_complex_fields = complex_fields - molecule_fields - chain_fields - residue_fields - atom_fields - bond_fields
        unique_molecule_fields = molecule_fields - complex_fields - chain_fields - residue_fields - atom_fields - bond_fields
        unique_chain_fields = chain_fields - complex_fields - molecule_fields - residue_fields - atom_fields - bond_fields
        unique_residue_fields = residue_fields - complex_fields - molecule_fields - chain_fields - atom_fields - bond_fields
        unique_bond_fields = bond_fields - complex_fields - molecule_fields - chain_fields - residue_fields - atom_fields
        unique_atom_fields = atom_fields - complex_fields - molecule_fields - chain_fields - residue_fields - bond_fields

        schema = None
        if any(data.get(key) for key in unique_complex_fields):
            schema = ComplexSchema()
        elif any(data.get(key) for key in unique_molecule_fields):
            schema = MoleculeSchema()
        # Shallow versions of chains have no unique values,
        # so if only name and possibly index is provided, assume its chain data
        elif any(data.get(key) for key in unique_chain_fields) \
                or 'name' in data and len(data) <= 2:
            schema = ChainSchema()
        elif any(data.get(key) for key in unique_residue_fields):
            schema = ResidueSchema()
        elif any(data.get(key) for key in unique_atom_fields):
            schema = AtomSchema()
        elif any(data.get(key) for key in unique_bond_fields):
            schema = BondSchema()
        if not schema:
            raise ValueError('Could not determine structure schema')
        return schema
