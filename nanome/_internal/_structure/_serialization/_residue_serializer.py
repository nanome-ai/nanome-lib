from nanome._internal._util._serializers import _ArraySerializer, _StringSerializer, _ColorSerializer
from . import _AtomSerializerID
from . import _BondSerializer
from .. import _Residue

from nanome._internal._util._serializers import _TypeSerializer

class _ResidueSerializer(_TypeSerializer):
    def __init__(self, shallow = False):
        self.shallow = shallow
        self.array = _ArraySerializer()
        self.atom = _AtomSerializerID()
        self.bond = _BondSerializer()
        self.color = _ColorSerializer()
        self.string = _StringSerializer()

    def version(self):
        return 0

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
        context.write_bool(value._rendering._modified)
        context.write_bool(value._rendering._ribboned)
        context.write_float(value._rendering._ribbon_size)
        context.write_int(value._rendering._ribbon_mode.value)
        context.write_using_serializer(self.color, value._rendering._ribbon_color)

        context.write_using_serializer(self.string, value._molecular._type)
        context.write_int(value._molecular._serial)
        context.write_using_serializer(self.string, value._molecular._name)
        context.write_int(value._molecular._secondary_structure.value)

    def deserialize(self, version, context):
        residue = _Residue._create()
        residue._index = context.read_long()

        self.array.set_type(self.atom)
        residue._atoms = context.read_using_serializer(self.array)
        self.array.set_type(self.bond)
        residue._bonds = context.read_using_serializer(self.array)
        
        residue._rendering._modified = context.read_bool()
        residue._rendering._ribboned = context.read_bool()
        residue._rendering._ribbon_size = context.read_float()
        mode = context.read_int()
        residue._rendering._ribbon_mode = _Residue.RibbonMode(mode)
        residue._rendering._ribbon_color = context.read_using_serializer(self.color)

        residue._molecular._type = context.read_using_serializer(self.string)
        residue._molecular._serial = context.read_int()
        residue._molecular._name = context.read_using_serializer(self.string)
        secondary = context.read_int()
        residue._molecular._secondary_structure = _Residue.SecondaryStructure(secondary)
        return residue