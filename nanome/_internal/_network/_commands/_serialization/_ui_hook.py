from nanome._internal._util._serializers import _TypeSerializer
from nanome.util import Enum

class _UIHook(_TypeSerializer):
    class Type(Enum):
        button_hover = 0

    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "UIHook"

    def serialize(self, version, value, context):
        context.write_byte(value[0])
        context.write_int(value[1])

    def deserialize(self, version, context):
        raise NotImplementedError
