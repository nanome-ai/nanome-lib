from nanome._internal._util._serializers import _ArraySerializer, _DictionarySerializer, _LongSerializer
from nanome._internal._structure._serialization import _ComplexSerializer, _AtomSerializer

from nanome._internal._util._serializers import _TypeSerializer

class _CalculateESP(_TypeSerializer):
    def __init__(self):
        self.array_serializer = _ArraySerializer()
        self.array_serializer.set_type(_ComplexSerializer())
        atom_serializer = _AtomSerializer()
        long_serializer = _LongSerializer()
        self.dict = _DictionarySerializer()
        self.dict.set_types(long_serializer, atom_serializer)

    def version(self):
        return 0

    def name(self):
        return "CalculateESP"

    def serialize(self, version, value, context):
        subcontext = context.create_sub_context()
        subcontext.payload["Atom"] = {}
        subcontext.write_using_serializer(self.array_serializer, value)
        context.write_using_serializer(self.dict, subcontext.payload["Atom"])
        context.write_bytes(subcontext.to_array())

    def deserialize(self, version, context):
        context.payload["Atom"] = context.read_using_serializer(self.dict)
        complexes = context.read_using_serializer(self.array_serializer)
        return complexes
