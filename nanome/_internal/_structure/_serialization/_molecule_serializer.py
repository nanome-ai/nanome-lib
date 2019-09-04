from . import _ChainSerializer
from .. import _Molecule

from nanome._internal._util._serializers import _ArraySerializer, _DictionarySerializer, _StringSerializer
from nanome._internal._util._serializers import _TypeSerializer

class _MoleculeSerializer(_TypeSerializer):
    def __init__(self, shallow = False):
        self.shallow = shallow
        self.array = _ArraySerializer()
        self.array.set_type(_ChainSerializer())
        self.string = _StringSerializer()
        self.dictionary = _DictionarySerializer()
        self.dictionary.set_types(self.string, self.string)
        self.array = _ArraySerializer()

    def version(self):
        #Version 0 corresponds to Nanome release 1.13
        return 1

    def name(self):
        return "Molecule"

    def serialize(self, version, value, context):
        context.write_long(value._index)

        if (self.shallow):
            context.write_using_serializer(self.array, [])
        else:
            context.write_using_serializer(self.array, value._chains)
        context.write_using_serializer(self.string, value._name)
        
        context.write_using_serializer(self.dictionary, value._associated)

        if self.version >= 1:
            context.write_int(value._current_conformer)
            context.write_int(value._max_conformer)
            self.array.set_type(self.string)
            context.write_using_serializer(self.array, value._names)
            context.write_using_serializer(self.array, value._associateds)

    def deserialize(self, version, context):
        molecule = _Molecule._create()
        molecule._index = context.read_long()

        molecule._set_chains(context.read_using_serializer(self.array))
        molecule._name = context.read_using_serializer(self.string)

        molecule._associated = context.read_using_serializer(self.dictionary)

        if self.version >= 1:
            molecule._current_conformer = context.read_int()
            molecule._max_conformer = context.read_int()
            self.array.set_type(self.string)
            molecule._names = context.read_using_serializer(self.array)
            molecule._associateds = context.read_using_serializer(self.array)

        return molecule
