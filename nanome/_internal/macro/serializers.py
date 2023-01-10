from nanome._internal.util.type_serializers import StringSerializer, TypeSerializer
from . import _Macro


class _MacroSerializer(TypeSerializer):
    def __init__(self):
        self.string = StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "Macro"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.string, value.title)
        context.write_using_serializer(self.string, value.logic)

    def deserialize(self, version, context):
        result = _Macro._create()
        result._title = context.read_using_serializer(self.string)
        result._logic = context.read_using_serializer(self.string)
        return result
