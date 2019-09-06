from nanome._internal._util._serializers import _StringSerializer, _ArraySerializer, _DirectoryEntrySerializer
from nanome.util import DirectoryRequestResult, DirectoryErrorCode

from nanome._internal._util._serializers import _TypeSerializer

class _DirectoryRequest(_TypeSerializer):
    def __init__(self):
        self.__string = _StringSerializer()
        self.__directory_entry_array = _ArraySerializer()
        self.__directory_entry_array.set_type(_DirectoryEntrySerializer())

    def version(self):
        return 0

    def name(self):
        return "Directory"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value._directory_name)
        context.write_using_serializer(self.__string, value._pattern)

    def deserialize(self, version, context):
        result = DirectoryRequestResult()
        result.entry_array = context.read_using_serializer(self.__directory_entry_array)
        result.error_code = DirectoryErrorCode(context.read_int())
        return result