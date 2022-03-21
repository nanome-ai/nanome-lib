from nanome._internal._util._serializers import _ArraySerializer, _DictionarySerializer, _LongSerializer, _StringSerializer
from nanome._internal._structure._serialization import _ComplexSerializer, _AtomSerializer
from nanome._internal._util._serializers import _TypeSerializer


class _ImportSmiles(_TypeSerializer):
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
        return "ImportSmiles"

    def serialize(self, version, value, context):
        subcontext = context.create_sub_context()
        subcontext.payload["Atom"] = {}
        subcontext.write_using_serializer(self.complex_array, value)
        context.write_using_serializer(self.dict, subcontext.payload["Atom"])
        context.write_bytes(subcontext.to_array())

    def deserialize(self, version, context):
        strings = context.read_using_serializer(self.string_array)
        return strings
