from nanome._internal.util.type_serializers import TypeSerializer, StringSerializer
from nanome._internal.shapes.line import _Line


class _LineSerializer(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "LineShape"

    def serialize(self, version, value, context):
        context.write_float(value._thickness)
        context.write_float(value._dash_length)
        context.write_float(value._dash_distance)

    def deserialize(self, version, context):
        result = _Line._create()
        result._thickness = context.read_float()
        result._dash_length = context.read_float()
        result._dash_distance = context.read_float()
        return result
