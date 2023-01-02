from nanome._internal.util.serializers import TypeSerializer


class _IntSerializer(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "int"

    def serialize(self, version, value, context):
        context.write_int(value)

    def deserialize(self, version, context):
        return context.read_int()
