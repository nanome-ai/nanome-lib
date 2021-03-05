from nanome._internal._util._serializers import _StringSerializer

from nanome._internal._util._serializers import _TypeSerializer

class _ExportFile(_TypeSerializer):
    _String = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "ExportFile"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        location = context.read_using_serializer(_ExportFile._String)
        filename = context.read_using_serializer(_ExportFile._String)
        data = context.read_byte_array()
        return (location, filename, data)
