from nanome._internal.util.serializers import TypeSerializer


class _DestroyStream(TypeSerializer):
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
