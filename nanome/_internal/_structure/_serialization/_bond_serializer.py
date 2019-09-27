from . import _AtomSerializerID
from .. import _Bond

from nanome._internal._util._serializers import _TypeSerializer, _ArraySerializer, _BoolSerializer, _ByteSerializer
from nanome.util import Logs

class _BondSerializer(_TypeSerializer):
    def __init__(self, shallow = False):
        self.shallow = shallow
        self.atom_serializer = _AtomSerializerID()
        self.array = _ArraySerializer()
        self.bool = _BoolSerializer()
        self.byte = _ByteSerializer()

    def version(self):
        #Version 0 corresponds to Nanome release 1.12
        return 1

    def name(self):
        return "Bond"

    def serialize(self, version, value, context):
        #nothing to do with shallow yet 
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
        # type: (_Atom, _ContextDeserialization) -> _Bond
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
                    bond._kinds[i] = _Bond.Kind.safe_cast(bond._kinds[i])
            else:
                bond._kind = _Bond.Kind.safe_cast(context.read_byte())
        else:
            bond._kind = _Bond.Kind.safe_cast(context.read_int())

        bond._atom1 = context.read_using_serializer(self.atom_serializer)
        bond._atom2 = context.read_using_serializer(self.atom_serializer)

        return bond
