from nanome._internal.util.type_serializers import TypeSerializer, _StringSerializer, _ArraySerializer


class _ExportLocations(TypeSerializer):
    def __init__(self):
        self.array = _ArraySerializer()
        self.array.set_type(_StringSerializer())

    def version(self):
        return 0

    def name(self):
        return "ExportLocations"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.array, value)

    def deserialize(self, version, context):
        return None
