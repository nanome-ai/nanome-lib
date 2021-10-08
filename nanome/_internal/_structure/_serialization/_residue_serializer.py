from nanome._internal._util._serializers import _ArraySerializer, _StringSerializer, _ColorSerializer, _CharSerializer
from . import _AtomSerializerID
from . import _BondSerializer
from .. import _Residue
from nanome.util import Logs

from nanome._internal._util._serializers import _TypeSerializer


class _ResidueSerializer(_TypeSerializer):
    def __init__(self, shallow=False):
        self.shallow = shallow
        self.array = _ArraySerializer()
        self.atom = _AtomSerializerID()
        self.bond = _BondSerializer()
        self.color = _ColorSerializer()
        self.string = _StringSerializer()
        self.char = _CharSerializer()

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
        residue = _Residue._create()
        residue._index = context.read_long()

        self.array.set_type(self.atom)
        residue._set_atoms(context.read_using_serializer(self.array))
        self.array.set_type(self.bond)
        residue._set_bonds(context.read_using_serializer(self.array))

        residue._ribboned = context.read_bool()
        residue._ribbon_size = context.read_float()
        residue._ribbon_mode = _Residue.RibbonMode.safe_cast(context.read_int())
        residue._ribbon_color = context.read_using_serializer(self.color)
        if (version > 0):
            residue._labeled = context.read_bool()
            residue._label_text = context.read_using_serializer(self.string)

        residue._type = context.read_using_serializer(self.string)
        residue._serial = context.read_int()
        residue._name = context.read_using_serializer(self.string)
        residue._secondary_structure = _Residue.SecondaryStructure.safe_cast(context.read_int())

        if (version >= 2):
            self.array.set_type(self.char)
            residue._ignored_alt_locs = context.read_using_serializer(self.array)

        return residue
