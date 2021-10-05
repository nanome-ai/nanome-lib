from nanome._internal._util._serializers import _StringSerializer, _ArraySerializer, _FileDataSerializer
from nanome._internal._util._serializers import _TypeSerializer


class _FileRequest(_TypeSerializer):
    def __init__(self):
        self.__string_array = _ArraySerializer()
        self.__string_array.set_type(_StringSerializer())
        self.__file_data_array = _ArraySerializer()
        self.__file_data_array.set_type(_FileDataSerializer())

    def version(self):
        return 0

    def name(self):
        return "FileRequest"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string_array, value)

    def deserialize(self, version, context):
        return context.read_using_serializer(self.__file_data_array)
