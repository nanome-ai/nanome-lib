from nanome._internal.network.serialization import _ContextSerialization, _ContextDeserialization
from nanome._internal.structure.serialization import _ComplexSerializer, _AtomSerializer
from nanome._internal.util.serializers import TypeSerializer, _ArraySerializer, _DictionarySerializer, _LongSerializer


class _AddBonds(TypeSerializer):
    def __init__(self):
        self.__array = _ArraySerializer()
        self.__array.set_type(_ComplexSerializer())
        self.__dict = _DictionarySerializer()
        self.__dict.set_types(_LongSerializer(), _AtomSerializer())

    def version(self):
        return 0

    def name(self):
        return "AddBonds"

    def serialize(self, version, value, context):
        subcontext = context.create_sub_context()
        subcontext.payload["Atom"] = {}

        subcontext.write_using_serializer(self.__array, value)

        context.write_using_serializer(self.__dict, subcontext.payload["Atom"])
        context.write_bytes(subcontext.to_array())

    def deserialize(self, version, context):
        context.payload["Atom"] = context.read_using_serializer(self.__dict)
        complexes = context.read_using_serializer(self.__array)
        return complexes
