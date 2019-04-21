from nanome._internal._util._serializers import _TypeSerializer

class _DestroyStream(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "StreamDestruction"

    def serialize(self, version, value, context):
        context.write_uint(value)

    def deserialize(self, version, context):
        raise NotImplementedError