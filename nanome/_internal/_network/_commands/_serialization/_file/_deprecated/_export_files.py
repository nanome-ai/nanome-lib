from nanome._internal._util._serializers import _ArraySerializer, _TypeSerializer, _ByteSerializer


class _ExportFiles(_TypeSerializer):
    def __init__(self):
        self.__array = _ArraySerializer()
        self.__array.set_type(_ByteSerializer())

    def version(self):
        return 0

    def name(self):
        return "ExportFiles"

    def serialize(self, version, value, context):
        return

    def deserialize(self, version, context):
        return context.read_using_serializer(self.__array)