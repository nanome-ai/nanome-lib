from nanome._internal._util._serializers import _TypeSerializer, _StringSerializer
from nanome._internal._shapes._label import _Label

class _LabelSerializer(_TypeSerializer):
    def __init__(self):
        self._string = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "LabelShape"

    def serialize(self, version, value, context):
        context.write_using_serializer(self._string, value._text)
        context.write_float(value._font_size)

    def deserialize(self, version, context):
        result = _Label._create()
        result._text = context.read_using_serializer(self._string)
        result._font_size = context.read_float()
        return result
