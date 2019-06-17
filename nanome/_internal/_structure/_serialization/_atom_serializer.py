from nanome._internal._util._serializers import _StringSerializer, _ColorSerializer, _Vector3Serializer
from .. import _Atom
from nanome._internal._util._serializers import _TypeSerializer

class _AtomSerializer(_TypeSerializer):
    def __init__(self):
        self.color = _ColorSerializer()
        self.string = _StringSerializer()
        self.vector = _Vector3Serializer()

    def version(self):
        #Version 0 corresponds to Nanome release 1.10
        return 1

    def name(self):
        return "Atom"

    def serialize(self, version, value, context):
        context.write_long(value._index)
        context.write_bool(value._selected)
        context.write_int(value._atom_mode)
        context.write_bool(value._labeled)
        if (version > 0):
            context.write_using_serializer(self.string, value._label_text)
        context.write_bool(value._atom_rendering)
        context.write_using_serializer(self.color, value._atom_color)
        context.write_bool(value._surface_rendering)
        context.write_using_serializer(self.color, value._surface_color)
        context.write_float(value._surface_opacity)

        context.write_bool(value._hydrogened)
        context.write_bool(value._watered)
        context.write_bool(value._het_atomed)
        context.write_bool(value._het_surfaced)
        context.write_using_serializer(self.string, value._symbol)
        if (version == 0):
            context.write_int(0)
        context.write_using_serializer(self.string, value._name)
        context.write_using_serializer(self.vector, value._position)
        context.write_bool(value._is_het)

        context.write_float(value._occupancy)
        context.write_float(value._bfactor)
        context.write_bool(value._acceptor)
        context.write_bool(value._donor)

    def deserialize(self, version, context):
        # type: (_Atom, _ContextDeserialization) -> _Atom
        atom = _Atom._create()
        index = context.read_long()
        if index >= 0:
            atom._index = index
        atom._selected = context.read_bool()
        atom_mode = context.read_int()
        atom._atom_mode = _Atom.AtomRenderingMode(atom_mode)
        atom._labeled = context.read_bool()
        if (version > 0):
            atom._label_text = context.read_using_serializer(self.string)
        atom._atom_rendering = context.read_bool()
        atom._atom_color = context.read_using_serializer(self.color)
        atom._surface_rendering = context.read_bool()
        atom._surface_color = context.read_using_serializer(self.color)
        atom._surface_opacity = context.read_float()

        atom._hydrogened = context.read_bool()
        atom._watered = context.read_bool()
        atom._het_atomed = context.read_bool()
        atom._het_surfaced = context.read_bool()

        atom._symbol = context.read_using_serializer(self.string)
        if (version == 0):
            context.read_int()
        atom._name = context.read_using_serializer(self.string)
        atom._position = context.read_using_serializer(self.vector)
        atom._is_het = context.read_bool()

        atom._occupancy = context.read_float()
        atom._bfactor = context.read_float()
        atom._acceptor = context.read_bool()
        atom._donor = context.read_bool()
        return atom
