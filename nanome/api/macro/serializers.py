from nanome._internal.serializer_fields import StringField, TypeSerializer
from .macro import Macro


class MacroSerializer(TypeSerializer):
    def __init__(self):
        self.string = StringField()

    def version(self):
        return 0

    def name(self):
        return "Macro"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.string, value.title)
        context.write_using_serializer(self.string, value.logic)

    def deserialize(self, version, context):
        result = Macro._create()
        result._title = context.read_using_serializer(self.string)
        result._logic = context.read_using_serializer(self.string)
        return result
