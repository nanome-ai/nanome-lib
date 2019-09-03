from nanome._internal._util._serializers import _TypeSerializer

class _CreateStreamResult(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 1

    def name(self):
        return "StreamCreationResult"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        err = context.read_byte()
        id = context.read_uint()
        if version > 0:
            data_type = context.read_byte()
        else:
            data_type = Stream.DataType.float
        return (err, id, data_type)
