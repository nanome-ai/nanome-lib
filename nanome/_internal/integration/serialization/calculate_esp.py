from nanome._internal.util.type_serializers import TypeSerializer, ArraySerializer, DictionarySerializer, LongSerializer
from nanome._internal.structure.serialization import _ComplexSerializer, _AtomSerializer



class _CalculateESP(TypeSerializer):
    def __init__(self):
        self.array_serializer = ArraySerializer()
        self.array_serializer.set_type(_ComplexSerializer())
        atom_serializer = _AtomSerializer()
        long_serializer = LongSerializer()
        self.dict = DictionarySerializer()
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
