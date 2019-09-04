from . import _AtomSerializerID
from .. import _Bond

from nanome._internal._util._serializers import _TypeSerializer, _ArraySerializer, _BoolSerializer, _ByteSerializer
from nanome.util import Logs

cast_failed_warning = False

class _BondSerializer(_TypeSerializer):
    def __init__(self, shallow = False):
        self.shallow = shallow
        self.atom_serializer = _AtomSerializerID()
        self.array = _ArraySerializer()
        self.bool = _BoolSerializer()
        self.byte = _ByteSerializer()

    def version(self):
        #Version 0 corresponds to Nanome release 1.13
        return 1

    def name(self):
        return "Bond"

    def serialize(self, version, value, context):
        context.write_long(value._index)

        context.write_int(value._kind)
        #nothing to do with shallow yet 
        context.write_using_serializer(self.atom_serializer, value._atom1)
        context.write_using_serializer(self.atom_serializer, value._atom2)

        if self.version >= 1:
            self.array.set_type(self.bool)
            context.write_using_serializer(self.array, value._exists)
            self.array.set_type(self.byte)
            context.write_using_serializer(self.array, value._order)

    def deserialize(self, version, context):
        # type: (_Atom, _ContextDeserialization) -> _Bond
        bond = _Bond._create()
        bond._index = context.read_long()

        kind = context.read_int()
        try:
            bond._kind = _Bond.Kind(kind)
        except ValueError:
            global cast_failed_warning
            if cast_failed_warning == False:
                cast_failed_warning = True
                Logs.warning("Received an unknown bond type. Library might outdated")
            bond._kind = _Bond.Kind(kind)
        bond._atom1 = context.read_using_serializer(self.atom_serializer)
        bond._atom2 = context.read_using_serializer(self.atom_serializer)

        if self.version >= 1:
            self.array.set_type(self.bool)
            bond._exists = context.read_using_serializer(self.array)
            self.array.set_type(self.byte)
            bond._order = context.read_using_serializer(self.array)
        return bond
