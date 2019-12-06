from nanome._internal._util._serializers import _TypeSerializer
from nanome.util.enums import SetShapeResult

class _SetArbitraryVolumeResult(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "SetArbitraryVolumeResult"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        id = context.read_int()
        result = SetShapeResult(context.read_byte())
        return (id, result)