from . import _AtomSerializerID
from .. import _Bond

from nanome._internal._util._serializers import _TypeSerializer

class _BondSerializer(_TypeSerializer):
    def __init__(self, shallow = False):
        self.shallow = shallow
        self.atom_serializer = _AtomSerializerID()

    def version(self):
        return 0

    def name(self):
        return "Bond"

    def serialize(self, version, value, context):
        context.write_long(value._index)

        context.write_int(value._molecular._kind)
        #nothing to do with shallow yet 
        context.write_using_serializer(self.atom_serializer, value._atom1)
        context.write_using_serializer(self.atom_serializer, value._atom2)

    def deserialize(self, version, context):
        # type: (_Atom, _ContextDeserialization) -> _Bond
        bond = _Bond._create()
        bond._index = context.read_long()

        kind = context.read_int()
        bond._molecular._kind = _Bond.Kind(kind)
        bond._atom1 = context.read_using_serializer(self.atom_serializer)
        bond._atom2 = context.read_using_serializer(self.atom_serializer)
        return bond
