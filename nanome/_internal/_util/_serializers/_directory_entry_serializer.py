from . import _StringSerializer
from nanome.util import Logs, DirectoryEntry

from nanome._internal._util._serializers import _TypeSerializer

class _DirectoryEntrySerializer(_TypeSerializer):
    def __init__(self):
        self.__string = _StringSerializer()
    
    def version(self):
        return 0

    def name(self):
        return "DirectoryEntry"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        result = DirectoryEntry()
        result.name = context.read_using_serializer(self.__string)
        result.is_directory = context.read_bool()
        return result