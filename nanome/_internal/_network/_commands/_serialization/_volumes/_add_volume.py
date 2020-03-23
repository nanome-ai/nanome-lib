from nanome._internal._network._serialization import _ContextDeserialization, _ContextSerialization
from nanome._internal._volumetric._serialization import _VolumeDataSerializer, _VolumePropertiesSerializer
from nanome._internal._util._serializers import _TypeSerializer
from nanome._internal._volumetric._io._em_map._parse import parse_file

class _AddVolume(_TypeSerializer):
    def __init__(self):
        self.__data = _VolumeDataSerializer()
        self.__properties = _VolumePropertiesSerializer()

    def version(self):
        return 0

    def name(self):
        return "AddVolume"

    def serialize(self, version, value, context):
        context.write_long(value[0])
        context.write_using_serializer(self.__data, value[1])
        context.write_using_serializer(self.__properties, value[2])

    def deserialize(self, version, context):
        raise NotImplementedError