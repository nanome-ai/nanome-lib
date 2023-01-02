from nanome._internal.util.serializers import _StringSerializer

from nanome._internal.util.serializers import TypeSerializer


class _ExportFile(TypeSerializer):
    _String = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "ExportFile"

    def serialize(self, version, value, context):
        context.write_bool(value)

    def deserialize(self, version, context):
        location = context.read_using_serializer(_ExportFile._String)
        filename = context.read_using_serializer(_ExportFile._String)
        data = context.read_byte_array()
        return (location, filename, data)
