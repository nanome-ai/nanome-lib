from .. import _Substructure
from nanome._internal.util.type_serializers import TypeSerializer, StringSerializer, ArraySerializer, LongSerializer

class _SubstructureSerializer(TypeSerializer):
    def __init__(self):
        self.string = StringSerializer()
        self.array = ArraySerializer()
        self.array.set_type(LongSerializer())

    def version(self):
        return 0

    def name(self):
        return "Substructure"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.string, value._name)
        residue_indices = [res.index for res in value._residues]
        context.write_int(self.array, residue_indices)
        context.write_byte(int(value._structure_type))

    def deserialize(self, version, context):
        from nanome.util.enums import SubstructureType
        result = _Substructure._create()
        result._name = context.read_using_serializer(self.string)
        result._residues = context.read_using_serializer(self.array)
        result._structure_type = SubstructureType.safe_cast(context.read_byte())
        return result
