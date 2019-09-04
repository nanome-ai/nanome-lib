from . import _AtomSerializerID
from .. import _Bond

from nanome._internal._util._serializers import _TypeSerializer, _ArraySerializer, _BoolSerializer, _EnumSerializer
from nanome.util import Logs

class _BondSerializer(_TypeSerializer):
    def __init__(self, shallow = False):
        self.shallow = shallow
        self.atom_serializer = _AtomSerializerID()
        self.array = _ArraySerializer()
        self.bool = _BoolSerializer()
        self.enum = _EnumSerializer()
        self.enum.set_type(_Bond.Kind)

    def version(self):
        #Version 0 corresponds to Nanome release 1.13
        return 1

    def name(self):
        return "Bond"

    def serialize(self, version, value, context):
        context.write_long(value._index)
        if version < 1:
            context.write_using_serializer(self.enum, value._kind)
        #nothing to do with shallow yet 
        context.write_using_serializer(self.atom_serializer, value._atom1)
        context.write_using_serializer(self.atom_serializer, value._atom2)

        if version >= 1:
            self.array.set_type(self.bool)
            context.write_using_serializer(self.array, value._exists)
            self.array.set_type(self.enum)
            context.write_using_serializer(self.array, value._orders)

    def deserialize(self, version, context):
        # type: (_Atom, _ContextDeserialization) -> _Bond
        bond = _Bond._create()
        bond._index = context.read_long()

        if version < 1:
            bond._kind = context.read_using_serializer(self.enum)

        bond._atom1 = context.read_using_serializer(self.atom_serializer)
        bond._atom2 = context.read_using_serializer(self.atom_serializer)

        if version >= 1:
            self.array.set_type(self.bool)
            bond._exists = context.read_using_serializer(self.array)
            self.array.set_type(self.enum)
            bond._orders = context.read_using_serializer(self.array)
        return bond
