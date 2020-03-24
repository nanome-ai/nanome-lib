from nanome._internal._network._serialization import _ContextDeserialization, _ContextSerialization
from nanome._internal._volumetric._serialization import _VolumeDataSerializer, _VolumePropertiesSerializer
from nanome._internal._util._serializers import _TypeSerializer, _LongSerializer, _DictionarySerializer
from nanome._internal._structure._serialization import _ComplexSerializer, _AtomSerializer
from nanome._internal._volumetric._io._em_map._parse import parse_file

class _AddVolume(_TypeSerializer):
    def __init__(self):
        self.__complex = _ComplexSerializer()
        atom_serializer = _AtomSerializer()
        long_serializer = _LongSerializer()
        self.__dict = _DictionarySerializer()
        self.__dict.set_types(long_serializer, atom_serializer)
        self.__data = _VolumeDataSerializer()
        self.__properties = _VolumePropertiesSerializer()

    def version(self):
        return 0

    def name(self):
        return "AddVolume"

    def serialize(self, version, value, context):
        subcontext = context.create_sub_context()
        subcontext.payload["Atom"] = {}
        subcontext.write_using_serializer(self.__complex, value[0])
        context.write_using_serializer(self.__dict, subcontext.payload["Atom"])
        context.write_bytes(subcontext.to_array())

        context.write_long(value[1])
        context.write_using_serializer(self.__data, value[2])
        context.write_using_serializer(self.__properties, value[3])

    def deserialize(self, version, context):
        raise NotImplementedError