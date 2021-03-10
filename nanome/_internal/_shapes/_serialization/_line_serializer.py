from nanome._internal._util._serializers import _TypeSerializer, _StringSerializer
from nanome._internal._shapes._line import _Line

class _LineSerializer(_TypeSerializer):
    def __init__(self):
        self.string = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "LineShape"

    def serialize(self, version, value, context):
        context.write_float(value._thickness)
        context.write_float(value._dash_length)
        context.write_float(value._dash_distance)
        context.write_using_serializer(self.string, value._label)

    def deserialize(self, version, context):
        result = _Line._create()
        result._thickness = context.read_float()
        result._dash_length = context.read_float()
        result._dash_distance = context.read_float()
        print(result._dash_distance)
        result._label = context.read_using_serializer(self.string)
        return result
