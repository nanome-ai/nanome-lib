from nanome._internal._util._serializers import _StringSerializer

from nanome._internal._util._serializers import _TypeSerializer

class _FileExport(_TypeSerializer):
    _String = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "ExportFile"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        filename = context.read_using_serializer(_FileExport._String)
        data = context.read_byte_array()
        return (filename, data)
