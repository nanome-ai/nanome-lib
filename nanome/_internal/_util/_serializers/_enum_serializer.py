from nanome.util import Enum
from nanome._internal._util._serializers import _TypeSerializer

class _EnumSerializer(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "enum"

    def serialize(self, version, value, context):
        if version >= 1:
            context.write_byte(value)
        else:
            context.write_int(value)

    def deserialize(self, version, context):
        if version >= 1:
            return self._enum.safe_cast(context.read_byte())
        else:
            return self._enum.safe_cast(context.read_int())

    def set_type(self, enum):
        self._enum = enum