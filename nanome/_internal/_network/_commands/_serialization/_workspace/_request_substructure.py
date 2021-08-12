from nanome._internal._util._serializers import _TypeSerializer, _ArraySerializer, _DictionarySerializer, _LongSerializer
from nanome._internal._structure._serialization import _SubstructureSerializer, _AtomSerializer

class _RequestSubstructure(_TypeSerializer):
    def __init__(self):
        self.array = _ArraySerializer()
        self.array.set_type(_SubstructureSerializer())
        atom_serializer = _AtomSerializer()
        long_serializer = _LongSerializer()
        self.dict = _DictionarySerializer()
        self.dict.set_types(long_serializer, atom_serializer)

    def version(self):
        return 0

    def name(self):
        return "RequestSubstructure"

    def serialize(self, version, value, context):
        context.write_long(value[0])
        context.write_byte(int(value[1]))

    def deserialize(self, version, context):
        context.payload["Atom"] = context.read_using_serializer(self.dict)
        return context.read_using_serializer(self.array)