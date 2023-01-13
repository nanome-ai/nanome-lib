from nanome._internal.serializer_fields import (
    ArrayField, StringField, ColorField, CharField,
    UnityPositionField, Vector3Field, UnityRotationField,
    BoolField, DictionaryField, ByteField, TypeSerializer,
    LongField, QuaternionField
)
from ..._internal.structure import _Atom, _Bond, _Chain, _Complex, _Molecule, _Residue, _Substructure, _Workspace


class AtomSerializer(TypeSerializer):

    def __init__(self):
        self.color = ColorField()
        self.string = StringField()
        self.char = CharField()
        self.vector = Vector3Field()
        self.array = ArrayField()
        self.bool = BoolField()
        self.dict = DictionaryField()
        self.dict.set_types(self.string, self.string)

    def version(self):
        # Version 0 corresponds to Nanome release 1.10
        # Version 1 corresponds to Nanome release 1.11
        # Version 2 corresponds to Nanome release 1.12
        # Version 3 corresponds to Nanome release 1.13
        # Version 4 corresponds to Nanome release 1.16
        # Version 5 corresponds to Nanome release 1.19
        # Version 6 corresponds to Nanome release 1.22
        # Version 7 corresponds to Nanome release 1.22
        # Version 8 corresponds to Nanome release 1.23
        return 8

    def name(self):
        return "Atom"

    def serialize(self, version, value, context):
        context.write_long(value._index)
        context.write_bool(value._selected)
        context.write_int(value._atom_mode)
        context.write_bool(value._labeled)
        if version >= 1:
            context.write_using_serializer(self.string, value._label_text)
        if version <= 6:
            context.write_bool(value._atom_rendering)
        context.write_using_serializer(self.color, value._atom_color)
        if version >= 2:
            context.write_float(value._atom_scale)
        context.write_bool(value._surface_rendering)
        context.write_using_serializer(self.color, value._surface_color)
        context.write_float(value._surface_opacity)

        if version <= 6:
            context.write_bool(value._hydrogened)
            context.write_bool(value._watered)
            context.write_bool(value._het_atomed)
        context.write_bool(value._het_surfaced)
        context.write_using_serializer(self.string, value._symbol)
        context.write_int(value._serial)
        context.write_using_serializer(self.string, value._name)
        if version >= 3:
            has_conformer = len(value._positions) > 1
            context.write_bool(has_conformer)
            if (has_conformer):
                self.array.set_type(self.vector)
                context.write_using_serializer(self.array, value._positions)
                self.array.set_type(self.bool)
                context.write_using_serializer(self.array, value._in_conformer)
            else:
                context.write_using_serializer(self.vector, value._position)
        else:
            context.write_using_serializer(self.vector, value._position)
        context.write_bool(value._is_het)

        context.write_float(value._occupancy)
        context.write_float(value._bfactor)
        context.write_bool(value._acceptor)
        context.write_bool(value._donor)

        if version >= 6:
            context.write_bool(value._polar_hydrogen)

        if version == 4:
            try:
                atom_type = value._atom_type["IDATM"]
            except KeyError:
                atom_type = ""
            context.write_using_serializer(self.string, atom_type)

        if version >= 4:
            context.write_int(value._formal_charge)

        if version >= 5:
            context.write_float(value._partial_charge)
            context.write_using_serializer(self.dict, value._atom_type)

        if version >= 7:
            context.write_uint(value._display_mode)

        if version >= 8:
            context.write_using_serializer(self.char, value._alt_loc)

    def deserialize(self, version, context):
        from nanome.util import enums
        # type: (_Atom, ContextDeserialization) -> _Atom
        atom = _Atom._create()
        index = context.read_long()
        if index >= 0:
            atom._index = index
        atom._selected = context.read_bool()
        atom._atom_mode = enums.AtomRenderingMode.safe_cast(context.read_int())
        atom._labeled = context.read_bool()
        if version >= 1:
            atom._label_text = context.read_using_serializer(self.string)
        if version <= 6:
            atom._atom_rendering = context.read_bool()
        atom._atom_color = context.read_using_serializer(self.color)
        if version >= 2:
            atom._atom_scale = context.read_float()
        atom._surface_rendering = context.read_bool()
        atom._surface_color = context.read_using_serializer(self.color)
        atom._surface_opacity = context.read_float()

        if version <= 6:
            atom._hydrogened = context.read_bool()
            atom._watered = context.read_bool()
            atom._het_atomed = context.read_bool()
        atom._het_surfaced = context.read_bool()

        atom._symbol = context.read_using_serializer(self.string)
        atom._serial = context.read_int()
        atom._name = context.read_using_serializer(self.string)
        if version >= 3:
            has_conformer = context.read_bool()
            if has_conformer:
                self.array.set_type(self.vector)
                atom._positions = context.read_using_serializer(self.array)
                self.array.set_type(self.bool)
                atom._in_conformer = context.read_using_serializer(self.array)
            else:
                atom._position = context.read_using_serializer(self.vector)
        else:
            atom._position = context.read_using_serializer(self.vector)
        atom._is_het = context.read_bool()

        atom._occupancy = context.read_float()
        atom._bfactor = context.read_float()
        atom._acceptor = context.read_bool()
        atom._donor = context.read_bool()

        if version >= 6:
            atom._polar_hydrogen = context.read_bool()

        if version == 4:
            atom._atom_type["IDATM"] = context.read_using_serializer(
                self.string)

        if version >= 4:
            atom._formal_charge = context.read_int()

        if version >= 5:
            atom._partial_charge = context.read_float()
            atom._atom_type = context.read_using_serializer(self.dict)

        if version >= 7:
            atom._display_mode = context.read_uint()

        if version >= 8:
            atom._alt_loc = context.read_using_serializer(self.char)

        return atom


# Requires a dictionary of Atoms.
# Serializes the atoms serial instead of the whole atom but adds it to the dict
# Deserializes the ID and returns the atom from the dict with that ID.


class AtomSerializerID(TypeSerializer):
    def version(self):
        return 0

    def name(self):
        return "AtomIndex"

    def serialize(self, version, value, context):
        context.write_long(value._unique_identifier)
        payload = context.payload["Atom"]
        payload[value._unique_identifier] = value

    def deserialize(self, version, context):
        uid = context.read_long()
        payload = context.payload["Atom"]
        atom = payload[uid]
        return atom


class BondSerializer(TypeSerializer):
    def __init__(self, shallow=False):
        self.shallow = shallow
        self.atom_serializer = AtomSerializerID()
        self.array = ArrayField()
        self.bool = BoolField()
        self.byte = ByteField()

    def version(self):
        # Version 0 corresponds to Nanome release 1.12
        return 1

    def name(self):
        return "Bond"

    def serialize(self, version, value, context):
        # nothing to do with shallow yet
        context.write_long(value._index)
        if version >= 1:
            has_conformer = len(value._in_conformer) > 1
            context.write_bool(has_conformer)
            if has_conformer:
                self.array.set_type(self.byte)
                context.write_using_serializer(self.array, value._kinds)
                self.array.set_type(self.bool)
                context.write_using_serializer(self.array, value._in_conformer)
            else:
                context.write_byte(value._kind)
        else:
            context.write_int(value._kind)
        context.write_using_serializer(self.atom_serializer, value._atom1)
        context.write_using_serializer(self.atom_serializer, value._atom2)

    def deserialize(self, version, context):
        # type: (_Atom, ContextDeserialization) -> _Bond
        from nanome.util import enums
        bond = _Bond._create()
        bond._index = context.read_long()
        if version >= 1:
            has_conformer = context.read_bool()
            if has_conformer:
                self.array.set_type(self.byte)
                bond._kinds = context.read_using_serializer(self.array)
                self.array.set_type(self.bool)
                bond._in_conformer = context.read_using_serializer(self.array)
                for i in range(len(bond._kinds)):
                    bond._kinds[i] = enums.Kind.safe_cast(bond._kinds[i])
            else:
                bond._kind = enums.Kind.safe_cast(context.read_byte())
        else:
            bond._kind = enums.Kind.safe_cast(context.read_int())

        bond._atom1 = context.read_using_serializer(self.atom_serializer)
        bond._atom2 = context.read_using_serializer(self.atom_serializer)

        return bond


class ChainSerializer(TypeSerializer):
    def __init__(self, shallow=False):
        self.shallow = shallow
        self.array_serializer = ArrayField()
        self.array_serializer.set_type(ResidueSerializer())
        self.string = StringField()

    def version(self):
        return 0

    def name(self):
        return "Chain"

    def serialize(self, version, value, context):
        context.write_long(value._index)
        if (self.shallow):
            context.write_using_serializer(self.array_serializer, [])
        else:
            context.write_using_serializer(
                self.array_serializer, value._residues)
        context.write_using_serializer(self.string, value._name)

    def deserialize(self, version, context):
        chain = _Chain._create()
        chain._index = context.read_long()

        chain._set_residues(
            context.read_using_serializer(self.array_serializer))
        chain._name = context.read_using_serializer(self.string)
        return chain


class ComplexSerializer(TypeSerializer):
    def __init__(self, shallow=False):
        self.shallow = shallow
        self.array = ArrayField()
        self.array.set_type(MoleculeSerializer())
        self.string = StringField()

        self.dictionary = DictionaryField()
        self.dictionary.set_types(self.string, self.string)

        self.vector = Vector3Field()
        self.quaternion = QuaternionField()
        self.pos = UnityPositionField()
        self.rot = UnityRotationField()

    def version(self):
        return 3

    def name(self):
        return "Complex"

    def serialize(self, version, value, context):
        from nanome.util import Quaternion, Vector3
        context.write_long(value._index)
        if (self.shallow):
            context.write_using_serializer(self.array, [])
        else:
            context.write_using_serializer(self.array, value._molecules)
        context.write_bool(value._boxed)
        context.write_bool(value._locked)
        context.write_bool(value._visible)
        context.write_bool(value._computing)
        context.write_int(value._current_frame)

        context.write_using_serializer(self.string, value._name)
        if version >= 2:
            context.write_int(value._index_tag)
            context.write_using_serializer(self.string, value._split_tag)
        if version >= 3:
            context.write_using_serializer(self.pos, value._position)
            context.write_using_serializer(self.rot, value._rotation)
        else:
            position = Vector3._get_inversed_handedness(value._position)
            context.write_using_serializer(self.vector, position)
            rotation = Quaternion._get_inversed_handedness(value._rotation)
            context.write_using_serializer(self.quaternion, rotation)
        context.write_using_serializer(self.dictionary, value._remarks)

        # writing junk because selected flag is one directional.
        context.write_bool(False)
        context.write_bool(value._surface_dirty)
        context.write_float(value._surface_refresh_rate)

        if version >= 1:
            context.write_using_serializer(self.string, value._box_label)

    def deserialize(self, version, context):
        complex = _Complex._create()
        complex._index = context.read_long()

        complex._set_molecules(context.read_using_serializer(self.array))

        complex._boxed = context.read_bool()
        complex._locked = context.read_bool()
        complex._visible = context.read_bool()
        complex._computing = context.read_bool()
        complex._current_frame = context.read_int()

        complex._name = context.read_using_serializer(self.string)
        if version >= 2:
            complex._index_tag = context.read_int()
            complex._split_tag = context.read_using_serializer(self.string)
        if version >= 3:
            complex._position = context.read_using_serializer(self.vector)
            complex._rotation = context.read_using_serializer(self.quaternion)
        else:
            complex._position = context.read_using_serializer(
                self.vector)._inverse_handedness()
            complex._rotation = context.read_using_serializer(
                self.quaternion)._inverse_handedness()

        complex._remarks = context.read_using_serializer(self.dictionary)
        # true iff at least 1 atom is selected in current molecule
        complex._selected = context.read_bool()
        context.read_bool()  # Read surface dirty but ignore it
        complex._surface_dirty = False
        complex._surface_refresh_rate = context.read_float()

        if version >= 1:
            complex._box_label = context.read_using_serializer(self.string)

        return complex


class MoleculeSerializer(TypeSerializer):
    def __init__(self, shallow=False):
        self.shallow = shallow
        self.array = ArrayField()
        self.string = StringField()
        self.dictionary = DictionaryField()
        self.dictionary.set_types(self.string, self.string)

    def version(self):
        # Version 0 corresponds to Nanome release 1.12
        return 1

    def name(self):
        return "Molecule"

    def serialize(self, version, value, context):
        context.write_long(value._index)
        self.array.set_type(ChainSerializer())
        if (self.shallow):
            context.write_using_serializer(self.array, [])
        else:
            context.write_using_serializer(self.array, value._chains)

        if version >= 1:
            has_conformer = value._conformer_count > 1
            context.write_bool(has_conformer)
            if has_conformer:
                context.write_int(value._current_conformer)
                context.write_int(value._conformer_count)
                self.array.set_type(self.string)
                context.write_using_serializer(self.array, value._names)
                self.array.set_type(self.dictionary)
                context.write_using_serializer(self.array, value._associateds)
            else:
                context.write_using_serializer(self.string, value._name)
                context.write_using_serializer(
                    self.dictionary, value._associated)
        else:
            context.write_using_serializer(self.string, value._name)
            context.write_using_serializer(self.dictionary, value._associated)

    def deserialize(self, version, context):
        molecule = _Molecule._create()
        molecule._index = context.read_long()
        self.array.set_type(ChainSerializer())
        molecule._set_chains(context.read_using_serializer(self.array))

        if version >= 1:
            has_conformer = context.read_bool()
            if has_conformer:
                molecule._current_conformer = context.read_int()
                molecule._conformer_count = context.read_int()
                self.array.set_type(self.string)
                molecule._names = context.read_using_serializer(self.array)
                self.array.set_type(self.dictionary)
                molecule._associateds = context.read_using_serializer(
                    self.array)
            else:
                molecule._name = context.read_using_serializer(self.string)
                molecule._associated = context.read_using_serializer(
                    self.dictionary)
        else:
            molecule._name = context.read_using_serializer(self.string)
            molecule._associated = context.read_using_serializer(
                self.dictionary)

        return molecule


class ResidueSerializer(TypeSerializer):
    def __init__(self, shallow=False):
        self.shallow = shallow
        self.array = ArrayField()
        self.atom = AtomSerializerID()
        self.bond = BondSerializer()
        self.color = ColorField()
        self.string = StringField()
        self.char = CharField()

    def version(self):
        # Version 0 corresponds to Nanome release 1.10
        # Version 2 corresponds to Nanome release 1.23
        return 2

    def name(self):
        return "Residue"

    def serialize(self, version, value, context):
        context.write_long(value._index)

        self.array.set_type(self.atom)
        if (self.shallow):
            context.write_using_serializer(self.array, [])
        else:
            context.write_using_serializer(self.array, value._atoms)
        self.array.set_type(self.bond)
        if (self.shallow):
            context.write_using_serializer(self.array, [])
        else:
            context.write_using_serializer(self.array, value._bonds)
        context.write_bool(value._ribboned)
        context.write_float(value._ribbon_size)
        context.write_int(value._ribbon_mode)
        context.write_using_serializer(self.color, value._ribbon_color)
        if (version > 0):
            context.write_bool(value._labeled)
            context.write_using_serializer(self.string, value._label_text)

        context.write_using_serializer(self.string, value._type)
        context.write_int(value._serial)
        context.write_using_serializer(self.string, value._name)
        context.write_int(value._secondary_structure.value)

        if (version >= 2):
            self.array.set_type(self.char)
            context.write_using_serializer(self.array, value._ignored_alt_locs)

    def deserialize(self, version, context):
        from nanome.util import enums
        residue = _Residue._create()
        residue._index = context.read_long()

        self.array.set_type(self.atom)
        residue._set_atoms(context.read_using_serializer(self.array))
        self.array.set_type(self.bond)
        residue._set_bonds(context.read_using_serializer(self.array))

        residue._ribboned = context.read_bool()
        residue._ribbon_size = context.read_float()
        residue._ribbon_mode = enums.RibbonMode.safe_cast(context.read_int())
        residue._ribbon_color = context.read_using_serializer(self.color)
        if (version > 0):
            residue._labeled = context.read_bool()
            residue._label_text = context.read_using_serializer(self.string)

        residue._type = context.read_using_serializer(self.string)
        residue._serial = context.read_int()
        residue._name = context.read_using_serializer(self.string)
        residue._secondary_structure = enums.SecondaryStructure.safe_cast(
            context.read_int())

        if (version >= 2):
            self.array.set_type(self.char)
            residue._ignored_alt_locs = context.read_using_serializer(
                self.array)

        return residue


class SubstructureSerializer(TypeSerializer):
    def __init__(self):
        self.string = StringField()
        self.array = ArrayField()
        self.array.set_type(LongField())

    def version(self):
        return 0

    def name(self):
        return "Substructure"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.string, value._name)
        residue_indices = [res.index for res in value._residues]
        context.write_int(self.array, residue_indices)
        context.write_byte(int(value._structure_type))

    def deserialize(self, version, context):
        from nanome.util.enums import SubstructureType
        result = _Substructure._create()
        result._name = context.read_using_serializer(self.string)
        result._residues = context.read_using_serializer(self.array)
        result._structure_type = SubstructureType.safe_cast(
            context.read_byte())
        return result


class WorkspaceSerializer(TypeSerializer):
    def __init__(self):
        self.array = ArrayField()
        self.array.set_type(ComplexSerializer())
        self.vec = Vector3Field()
        self.pos = UnityPositionField()
        self.rot = UnityRotationField()

    def version(self):
        return 0

    def name(self):
        return "Workspace"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.array, value._complexes)

        context.write_using_serializer(self.pos, value._position)
        context.write_using_serializer(self.rot, value._rotation)
        context.write_using_serializer(self.vec, value._scale)

    def deserialize(self, version, context):
        workspace = _Workspace._create()
        workspace._complexes = context.read_using_serializer(self.array)
        workspace._position = context.read_using_serializer(self.pos)
        workspace._rotation = context.read_using_serializer(self.rot)
        workspace._scale = context.read_using_serializer(self.vec)

        return workspace
