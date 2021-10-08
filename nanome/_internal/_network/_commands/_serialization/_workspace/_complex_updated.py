from nanome._internal._util._serializers import _TypeSerializer, _ArraySerializer, _DictionarySerializer, _LongSerializer
from nanome._internal._structure._serialization import _ComplexSerializer, _AtomSerializer


class _ComplexUpdated(_TypeSerializer):
    def __init__(self):
        self.complex_serializer = _ComplexSerializer()
        atom_serializer = _AtomSerializer()
        long_serializer = _LongSerializer()
        self.dict = _DictionarySerializer()
        self.dict.set_types(long_serializer, atom_serializer)

    def version(self):
        return 0

    def name(self):
        return "ComplexUpdated"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        index = context.read_long()
        has_complex = context.read_bool()

        if has_complex:
            context.payload["Atom"] = context.read_using_serializer(self.dict)
            complex = context.read_using_serializer(self.complex_serializer)
        else:
            complex = None
        return (index, complex)
