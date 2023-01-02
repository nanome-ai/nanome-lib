from nanome.util import Color

from nanome._internal.util.serializers import TypeSerializer


class _ColorSerializer(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "Color"

    def serialize(self, version, value, context):
        context.write_uint(value._color)

    def deserialize(self, version, context):
        return Color.from_int(context.read_uint())
