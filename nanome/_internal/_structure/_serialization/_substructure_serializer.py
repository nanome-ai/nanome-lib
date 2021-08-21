from .. import _Substructure
from nanome._internal._util._serializers import _TypeSerializer, _StringSerializer, _ArraySerializer, _LongSerializer
from nanome.util import Logs
from nanome.util.enums import SubstructureType


class _SubstructureSerializer(_TypeSerializer):
    def __init__(self):
        self.string = _StringSerializer()
        self.array = _ArraySerializer()
        self.array.set_type(_LongSerializer())

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
        result = _Substructure._create()
        result._name = context.read_using_serializer(self.string)
        result._residues = context.read_using_serializer(self.array)
        result._structure_type = SubstructureType.safe_cast(context.read_byte())
        return result
