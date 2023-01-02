from nanome._internal.util.type_serializers import TypeSerializer, ArraySerializer, DictionarySerializer, LongSerializer, StringSerializer
from nanome._internal.structure.serialization import _ComplexSerializer, _AtomSerializer


class _ExportSmiles(TypeSerializer):
    def __init__(self):
        self.complex_array = ArraySerializer()
        self.complex_array.set_type(_ComplexSerializer())
        self.string_array = ArraySerializer()
        self.string_array.set_type(StringSerializer())

        self.dict = DictionarySerializer()
        self.dict.set_types(LongSerializer(), _AtomSerializer())

    def version(self):
        return 0

    def name(self):
        return "ExportSmiles"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.string_array, value)

    def deserialize(self, version, context):
        context.payload["Atom"] = context.read_using_serializer(self.dict)
        complexes = context.read_using_serializer(self.complex_array)
        return complexes
