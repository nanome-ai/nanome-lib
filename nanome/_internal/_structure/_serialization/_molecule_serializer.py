from nanome._internal._util._serializers import _ArraySerializer, _DictionarySerializer, _StringSerializer
from . import _ChainSerializer
from .. import _Molecule

from nanome._internal._util._serializers import _TypeSerializer

class _MoleculeSerializer(_TypeSerializer):
    def __init__(self, shallow = False):
        self.shallow = shallow
        self.array = _ArraySerializer()
        self.array.set_type(_ChainSerializer())
        self.string = _StringSerializer()
        self.dictionary = _DictionarySerializer()
        self.dictionary.set_types(self.string, self.string)

    def version(self):
        return 0

    def name(self):
        return "Molecule"

    def serialize(self, version, value, context):
        context.write_long(value._index)

        if (self.shallow):
            context.write_using_serializer(self.array, [])
        else:
            context.write_using_serializer(self.array, value._chains)
        context.write_using_serializer(self.string, value._molecular._name)
        
        context.write_using_serializer(self.dictionary, value._molecular._associated)

    def deserialize(self, version, context):
        molecule = _Molecule._create()
        molecule._index = context.read_long()

        molecule._chains = context.read_using_serializer(self.array)
        molecule._molecular._name = context.read_using_serializer(self.string)

        molecule._molecular._associated = context.read_using_serializer(self.dictionary)
        return molecule
