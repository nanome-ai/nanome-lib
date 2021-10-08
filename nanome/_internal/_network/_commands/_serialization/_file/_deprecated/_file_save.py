from nanome._internal._util._serializers import _StringSerializer, _ArraySerializer, _FileSaveDataSerializer
from nanome._internal._util._serializers import _TypeSerializer


class _FileSave(_TypeSerializer):
    def __init__(self):
        self.__file_data_array = _ArraySerializer()
        self.__file_data_array.set_type(_FileSaveDataSerializer())

    def version(self):
        return 0

    def name(self):
        return "FileSave"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__file_data_array, value)

    def deserialize(self, version, context):
        return context.read_using_serializer(self.__file_data_array)
