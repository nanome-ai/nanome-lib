from nanome._internal._util._serializers import _StringSerializer, _CharSerializer, _ColorSerializer, _Vector3Serializer, _ArraySerializer, _BoolSerializer, _DictionarySerializer
from .. import _Atom
from nanome._internal._util._serializers import _TypeSerializer
from nanome.util import Logs


class _AtomSerializer(_TypeSerializer):
    def __init__(self):
        self.color = _ColorSerializer()
        self.string = _StringSerializer()
        self.char = _CharSerializer()
        self.vector = _Vector3Serializer()
        self.array = _ArraySerializer()
        self.bool = _BoolSerializer()
        self.dict = _DictionarySerializer()
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
        # type: (_Atom, _ContextDeserialization) -> _Atom
        atom = _Atom._create()
        index = context.read_long()
        if index >= 0:
            atom._index = index
        atom._selected = context.read_bool()
        atom._atom_mode = _Atom.AtomRenderingMode.safe_cast(context.read_int())
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
