from nanome._internal.util.type_serializers import TypeSerializer
from nanome._internal.shapes.sphere import _Sphere


class _SphereSerializer(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "SphereShape"

    def serialize(self, version, value, context):
        context.write_float(value.radius)

    def deserialize(self, version, context):
        result = _Sphere._create()
        result.radius = context.read_float()
        return result