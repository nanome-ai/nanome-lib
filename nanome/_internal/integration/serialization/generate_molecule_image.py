from nanome._internal.util.type_serializers import TypeSerializer, ArraySerializer, DictionarySerializer, LongSerializer, ByteArraySerializer
from nanome._internal.structure.serialization import _ComplexSerializer, _AtomSerializer


class _GenerateMoleculeImage(TypeSerializer):
    def __init__(self):
        self.complex_array = ArraySerializer()
        self.complex_array.set_type(_ComplexSerializer())

        self.image_array = ArraySerializer()
        self.image_array.set_type(ByteArraySerializer())

        self.dict = DictionarySerializer()
        self.dict.set_types(LongSerializer(), _AtomSerializer())

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
