from . import _ChainSerializer
from .. import _Molecule

from nanome._internal._util._serializers import _ArraySerializer, _DictionarySerializer, _StringSerializer
from nanome._internal._util._serializers import _TypeSerializer

class _MoleculeSerializer(_TypeSerializer):
    def __init__(self, shallow = False):
        self.shallow = shallow
        self.array = _ArraySerializer()
        self.string = _StringSerializer()
        self.dictionary = _DictionarySerializer()
        self.dictionary.set_types(self.string, self.string)

    def version(self):
        #Version 0 corresponds to Nanome release 1.12
        return 1

    def name(self):
        return "Molecule"

    def serialize(self, version, value, context):
        context.write_long(value._index)
        self.array.set_type(_ChainSerializer())
        if (self.shallow):
            context.write_using_serializer(self.array, [])
        else:
            context.write_using_serializer(self.array, value._chains)

        if version >= 1:
            has_conformer = value._conformer_count > 1
            context.write_bool(has_conformer)
            if has_conformer:
                context.write_int(value._current_conformer)
                context.write_int(value._conformer_count)
                self.array.set_type(self.string)
                context.write_using_serializer(self.array, value._names)
                self.array.set_type(self.dictionary)
                context.write_using_serializer(self.array, value._associateds)
            else:
                context.write_using_serializer(self.string, value._name)
                context.write_using_serializer(self.dictionary, value._associated)
        else:
            context.write_using_serializer(self.string, value._name)
            context.write_using_serializer(self.dictionary, value._associated)

    def deserialize(self, version, context):
        molecule = _Molecule._create()
        molecule._index = context.read_long()
        self.array.set_type(_ChainSerializer())
        molecule._set_chains(context.read_using_serializer(self.array))

        if version >= 1:
            has_conformer = context.read_bool()
            if has_conformer:
                molecule._current_conformer = context.read_int()
                molecule._conformer_count = context.read_int()
                self.array.set_type(self.string)
                molecule._names = context.read_using_serializer(self.array)
                self.array.set_type(self.dictionary)
                molecule._associateds = context.read_using_serializer(self.array)
            else:
                molecule._name = context.read_using_serializer(self.string)
                molecule._associated = context.read_using_serializer(self.dictionary)
        else:
            molecule._name = context.read_using_serializer(self.string)
            molecule._associated = context.read_using_serializer(self.dictionary)

        return molecule
