from nanome._internal._util._serializers import _TypeSerializer

class _FloatSerializer(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "float"

    def serialize(self, version, value, context):
        context.write_float(value)

    def deserialize(self, version, context):
        return context.read_float()
#to supress warning for unused serializer.
_FloatSerializer()
