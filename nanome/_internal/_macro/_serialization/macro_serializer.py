from nanome._internal._util._serializers import _StringSerializer
from .. import _Macro

from nanome._internal._util._serializers import _TypeSerializer


class _MacroSerializer(_TypeSerializer):
    def __init__(self):
        self.string = _StringSerializer()

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
