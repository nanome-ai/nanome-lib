from nanome._internal._util._serializers import _StringSerializer, _ColorSerializer, _Vector3Serializer
from .. import _Atom
from nanome._internal._util._serializers import _TypeSerializer

class _AtomSerializer(_TypeSerializer):
    def __init__(self):
        self.color = _ColorSerializer()
        self.string = _StringSerializer()
        self.vector = _Vector3Serializer()

    def version(self):
        return 0

    def name(self):
        return "Atom"

    def serialize(self, version, value, context):
        context.write_long(value._index)
        context.write_bool(value._rendering._selected)
        context.write_int(value._rendering._atom_mode)
        context.write_bool(value._rendering._labeled)
        context.write_bool(value._rendering._atom_rendering)
        context.write_using_serializer(self.color, value._rendering._atom_color)
        context.write_bool(value._rendering.surface_rendering)
        context.write_using_serializer(self.color, value._rendering._surface_color)
        context.write_float(value._rendering._surface_opacity)

        context.write_bool(value._rendering._hydrogened)
        context.write_bool(value._rendering._watered)
        context.write_bool(value._rendering._het_atomed)
        context.write_bool(value._rendering._het_surfaced)
        context.write_using_serializer(self.string, value.molecular._symbol)
        context.write_int(value.molecular._serial)
        context.write_using_serializer(self.string, value.molecular._name)
        context.write_using_serializer(self.vector, value.molecular._position)
        context.write_bool(value.molecular._is_het)

        context.write_float(value.molecular._occupancy)
        context.write_float(value.molecular._bfactor)
        context.write_bool(value.molecular._acceptor)
        context.write_bool(value.molecular._donor)

    def deserialize(self, version, context):
        # type: (_Atom, _ContextDeserialization) -> _Atom
        atom = _Atom._create()
        index = context.read_long()
        if index >= 0:
            atom._index = index
        atom._rendering._selected = context.read_bool()
        atom_mode = context.read_int()
        atom._rendering._atom_mode = _Atom.AtomRenderingMode(atom_mode)
        atom._rendering._labeled = context.read_bool()
        atom._rendering._atom_rendering = context.read_bool()
        atom._rendering._atom_color = context.read_using_serializer(self.color)
        atom._rendering._surface_rendering = context.read_bool()
        atom._rendering._surface_color = context.read_using_serializer(
            self.color)
        atom._rendering._surface_opacity = context.read_float()

        atom._rendering._hydrogened = context.read_bool()
        atom._rendering._watered = context.read_bool()
        atom._rendering._het_atomed = context.read_bool()
        atom._rendering._het_surfaced = context.read_bool()

        atom._molecular._symbol = context.read_using_serializer(self.string)
        atom._molecular._serial = context.read_int()
        atom._molecular._name = context.read_using_serializer(self.string)
        atom._molecular._position = context.read_using_serializer(self.vector)
        atom._molecular._is_het = context.read_bool()

        atom._molecular._occupancy = context.read_float()
        atom._molecular._bfactor = context.read_float()
        atom._molecular._acceptor = context.read_bool()
        atom._molecular._donor = context.read_bool()
        return atom
