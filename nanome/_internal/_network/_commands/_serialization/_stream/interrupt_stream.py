from nanome._internal._util._serializers import _TypeSerializer


class _InterruptStream(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "StreamInterrupt"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        err = context.read_byte()
        id = context.read_uint()
        return (err, id)
