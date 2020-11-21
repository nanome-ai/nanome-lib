from nanome._internal._util._serializers import _StringSerializer, _ArraySerializer, _DirectoryEntrySerializer
from nanome.util import DirectoryRequestResult, DirectoryErrorCode

from nanome._internal._util._serializers import _TypeSerializer

class _RM(_TypeSerializer):
    def __init__(self):
        self.__string = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "rm"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value)

    def deserialize(self, version, context):
        return DirectoryErrorCode.safe_cast(context.read_int())