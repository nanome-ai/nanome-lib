from nanome._internal import serializer_fields
from nanome.api import structure

from . import serializers


class AddVolume(serializer_fields.TypeSerializer):

    def __init__(self):
        self.__complex = structure.serializers.ComplexSerializer()
        atom_serializer = structure.serializers.AtomSerializer()
        long_serializer = serializer_fields.LongField()
        self.__dict = serializer_fields.DictionaryField()
        self.__dict.set_types(long_serializer, atom_serializer)
        self.__data = serializers.VolumeDataSerializer()
        self.__properties = serializers.VolumePropertiesSerializer()

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


class AddVolumeDone(serializer_fields.TypeSerializer):
    def version(self):
        return 0

    def name(self):
        return "AddVolumeDone"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        return None
