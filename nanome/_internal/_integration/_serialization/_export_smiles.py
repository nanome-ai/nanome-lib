from nanome._internal._util._serializers import _ArraySerializer, _DictionarySerializer, _LongSerializer, _StringSerializer
from nanome._internal._structure._serialization import _ComplexSerializer, _AtomSerializer
from nanome._internal._util._serializers import _TypeSerializer


class _ExportSmiles(_TypeSerializer):
    def __init__(self):
        self.complex_array = _ArraySerializer()
        self.complex_array.set_type(_ComplexSerializer())
        self.string_array = _ArraySerializer()
        self.string_array.set_type(_StringSerializer())

        self.dict = _DictionarySerializer()
        self.dict.set_types(_LongSerializer(), _AtomSerializer())

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
