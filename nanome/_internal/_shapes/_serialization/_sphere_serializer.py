from nanome._internal._util._serializers import _TypeSerializer

class _SphereSerializer(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "SphereShape"

    def serialize(self, version, value, context):
        context.write_float(value.radius)

    def deserialize(self, version, context):
        raise NotImplementedError
