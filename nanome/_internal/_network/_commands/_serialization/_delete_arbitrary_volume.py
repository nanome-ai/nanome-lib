from nanome._internal._util._serializers import _TypeSerializer

class _DeleteArbitraryVolume(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "DeleteArbitraryVolume"

    def serialize(self, version, value, context):
        context.write_int(value)

    def deserialize(self, version, context):
        pass