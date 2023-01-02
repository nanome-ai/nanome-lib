from nanome._internal.util.type_serializers import TypeSerializer, StringSerializer
from nanome._internal.shapes.label import _Label


class _LabelSerializer(TypeSerializer):
    def __init__(self):
        self._string = StringSerializer()

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
