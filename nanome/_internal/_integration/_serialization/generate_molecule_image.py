from nanome._internal._util._serializers import _ArraySerializer, _DictionarySerializer, _LongSerializer, _ByteArraySerializer
from nanome._internal._structure._serialization import _ComplexSerializer, _AtomSerializer
from nanome._internal._util._serializers import _TypeSerializer


class _GenerateMoleculeImage(_TypeSerializer):
    def __init__(self):
        self.complex_array = _ArraySerializer()
        self.complex_array.set_type(_ComplexSerializer())

        self.image_array = _ArraySerializer()
        self.image_array.set_type(_ByteArraySerializer())

        self.dict = _DictionarySerializer()
        self.dict.set_types(_LongSerializer(), _AtomSerializer())

    def version(self):
        return 0

    def name(self):
        return "GenerateMoleculeImage"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.image_array, value)

    def deserialize(self, version, context):
        context.payload["Atom"] = context.read_using_serializer(self.dict)
        ligands = context.read_using_serializer(self.complex_array)
        x = context.read_int()
        y = context.read_int()
        return ligands, (x, y)
