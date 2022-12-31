from nanome._internal._util._serializers import _ArraySerializer, _StringSerializer
from nanome._internal._util._serializers import _TypeSerializer


class _LoadFileInfo(_TypeSerializer):
    def __init__(self):
        self.string = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "LoadFileInfo"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.string, value[0])
        context.write_byte_array(value[1])

    def deserialize(self, version, context):
        raise NotImplementedError


class _LoadFile(_TypeSerializer):
    def __init__(self):
        self.array = _ArraySerializer()
        self.array.set_type(_LoadFileInfo())

    def version(self):
        return 0

    def name(self):
        return "LoadFile"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.array, value[0])
        context.write_bool(value[1])
        context.write_bool(value[2])

    def deserialize(self, version, context):
        raise NotImplementedError
