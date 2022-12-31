from nanome._internal._util._serializers import _DictionarySerializer, _StringSerializer, _ByteSerializer
from nanome._internal._util._serializers import _TypeSerializer


class _Connect(_TypeSerializer):
    def __init__(self):
        self.__dictionary = _DictionarySerializer()
        self.__dictionary.set_types(_StringSerializer(), _ByteSerializer())

    def version(self):
        return 0

    def name(self):
        return "Connect"

    def serialize(self, version, value, data):
        data.write_byte(value[0])
        data.write_using_serializer(self.__dictionary, value[1])

    def deserialize(self, version, data):
        version_table = data.read_using_serializer(self.__dictionary)
        return version_table
